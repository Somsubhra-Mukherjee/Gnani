import pytest
from sqlalchemy import text
from backend.app.database.connection import engine
from backend.app.security.sql_validator import SQLSecurityValidator
from backend.app.security.readonly_service import ReadOnlyQueryService, run_readonly_sql

@pytest.fixture
def validator():
    return SQLSecurityValidator(max_row_limit=500, dialect="sqlite")

@pytest.fixture
def service():
    return ReadOnlyQueryService()

class TestSQLSecurityValidator:
    def test_valid_select_simple(self, validator):
        res = validator.validate("SELECT id, name FROM regions")
        assert res.is_valid is True
        assert res.error is None
        assert "regions" in res.tables_accessed

    def test_valid_select_aggregations_and_joins(self, validator):
        sql = """
        SELECT r.name, COUNT(w.id) as wh_count
        FROM regions r
        JOIN warehouses w ON r.id = w.region_id
        GROUP BY r.name
        """
        res = validator.validate(sql)
        assert res.is_valid is True
        assert "regions" in res.tables_accessed
        assert "warehouses" in res.tables_accessed

    def test_valid_readonly_cte(self, validator):
        sql = """
        WITH monthly_losses AS (
            SELECT record_date, SUM(spoilage_cost_inr) as total_loss
            FROM spoilage_records
            GROUP BY record_date
        )
        SELECT * FROM monthly_losses WHERE total_loss > 100000
        """
        res = validator.validate(sql)
        assert res.is_valid is True
        assert "spoilage_records" in res.tables_accessed

    def test_reject_delete(self, validator):
        res = validator.validate("DELETE FROM customers WHERE id = 1")
        assert res.is_valid is False
        assert "DELETE" in res.error or "Prohibited" in res.error

    def test_reject_drop(self, validator):
        res = validator.validate("DROP TABLE monthly_financials")
        assert res.is_valid is False
        assert "DROP" in res.error or "Prohibited" in res.error

    def test_reject_update(self, validator):
        res = validator.validate("UPDATE monthly_financials SET net_profit_inr = 0")
        assert res.is_valid is False
        assert "UPDATE" in res.error or "Prohibited" in res.error

    def test_reject_insert(self, validator):
        res = validator.validate("INSERT INTO regions (name, code) VALUES ('Fake', 'REG-FK')")
        assert res.is_valid is False
        assert "INSERT" in res.error or "Prohibited" in res.error

    def test_reject_truncate_and_alter(self, validator):
        res1 = validator.validate("TRUNCATE TABLE shipments")
        assert res1.is_valid is False
        res2 = validator.validate("ALTER TABLE shipments ADD COLUMN hacked TEXT")
        assert res2.is_valid is False

    def test_reject_mixed_case_and_whitespace_obfuscation(self, validator):
        attacks = [
            "  dElEtE   FROM   customers  ",
            "DrOp  table   products",
            "uPdAtE sales_orders set status = 'Free'",
            "/* inline comment */ dElEtE FROM regions"
        ]
        for att in attacks:
            res = validator.validate(att)
            assert res.is_valid is False, f"Failed to reject obfuscated attack: {att}"

    def test_reject_stacked_queries(self, validator):
        stacked = [
            "SELECT * FROM regions; DROP TABLE products;",
            "SELECT 1; SELECT 2;",
            "SELECT * FROM warehouses; DELETE FROM warehouses;"
        ]
        for query in stacked:
            res = validator.validate(query)
            assert res.is_valid is False, f"Failed to reject stacked query: {query}"
            assert "Multiple/stacked" in res.error or "Prohibited" in res.error

    def test_reject_system_tables(self, validator):
        system_queries = [
            "SELECT * FROM sqlite_master",
            "SELECT * FROM sqlite_temp_master",
            "SELECT * FROM pg_catalog.pg_tables",
            "SELECT * FROM information_schema.tables"
        ]
        for q in system_queries:
            res = validator.validate(q)
            assert res.is_valid is False, f"Failed to reject system table access: {q}"
            assert "system catalog" in res.error.lower() or "unauthorized" in res.error.lower()

    def test_reject_unauthorized_external_tables(self, validator):
        res = validator.validate("SELECT * FROM employees_passwords_shadow")
        assert res.is_valid is False
        assert "Unauthorized table" in res.error

    def test_reject_unsafe_functions(self, validator):
        res = validator.validate("SELECT load_extension('evil.so')")
        assert res.is_valid is False
        assert "Prohibited database function" in res.error or "Prohibited" in res.error

    def test_enforce_row_limit(self, validator):
        res = validator.validate("SELECT * FROM shipments")
        assert res.is_valid is True
        assert res.has_limit is True
        assert res.limit_value <= 500
        assert "LIMIT 500" in res.sanitized_query.upper()

class TestReadOnlyServiceExecution:
    def test_service_executes_valid_query(self, service):
        res = service.execute_query(
            query="SELECT id, name, code FROM regions ORDER BY id",
            business_context="Retrieve operational regions"
        )
        assert res["success"] is True
        assert res["error"] is None
        assert len(res["rows"]) == 5
        assert res["columns"] == ["id", "name", "code"]
        assert res["duration_ms"] > 0

    def test_service_blocks_destructive_query_and_database_remains_intact(self, service):
        # 1. Count rows before
        with engine.connect() as conn:
            before_count = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar()

        # 2. Attempt destructive operation
        res = service.execute_query(
            query="DELETE FROM customers",
            business_context="Adversarial deletion test"
        )
        assert res["success"] is False
        assert "Security Validation Rejected" in res["error"]
        assert res["rows"] == []

        # 3. Verify row count is unchanged
        with engine.connect() as conn:
            after_count = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar()
        assert before_count == after_count

    def test_service_blocks_sql_injection_union_attack(self, service):
        injection = "SELECT id, name FROM regions WHERE id = 1 UNION SELECT 1, sql FROM sqlite_master"
        res = service.execute_query(query=injection)
        assert res["success"] is False
        assert "system catalog" in res["error"].lower() or "unauthorized" in res["error"].lower()

    def test_tool_run_readonly_sql_wrapper(self):
        result = run_readonly_sql(
            query="SELECT COUNT(*) as total_orders FROM sales_orders",
            business_context="Order count audit"
        )
        assert result["success"] is True
        assert result["rows"][0]["total_orders"] > 1000
