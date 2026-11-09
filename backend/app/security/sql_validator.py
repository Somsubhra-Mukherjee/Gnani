import re
from typing import Optional, List, Set, Tuple
import sqlglot
from sqlglot import exp
from pydantic import BaseModel

class SQLValidationResult(BaseModel):
    is_valid: bool
    error: Optional[str] = None
    sanitized_query: Optional[str] = None
    tables_accessed: List[str] = []
    has_limit: bool = False
    limit_value: Optional[int] = None

# Whitelist of permitted business tables and views
ALLOWED_TABLES: Set[str] = {
    "regions",
    "warehouses",
    "products",
    "customers",
    "suppliers",
    "transport_routes",
    "sales_orders",
    "sales_order_items",
    "inventory_snapshots",
    "inventory_movements",
    "shipments",
    "delivery_events",
    "vehicle_costs",
    "purchase_orders",
    "purchase_order_items",
    "spoilage_records",
    "expenses",
    "monthly_financials",
    "weather_observations",
    # Reporting Views
    "v_monthly_regional_performance",
    "v_product_profitability",
    "v_regional_product_profitability",
    "v_route_transportation_costs",
    "v_spoilage_summary"
}

# Forbidden system tables and catalogs
SYSTEM_TABLES: Set[str] = {
    "sqlite_master",
    "sqlite_temp_master",
    "sqlite_schema",
    "sqlite_sequence",
    "sqlite_stat1",
    "pg_catalog",
    "information_schema",
    "pg_tables",
    "pg_views",
    "pg_user",
    "pg_shadow",
    "sys_tables",
    "mysql"
}

# Forbidden functions that could execute OS commands, load libraries, or cause denial of service
UNSAFE_FUNCTIONS: Set[str] = {
    "load_extension",
    "readfile",
    "writefile",
    "edit",
    "system",
    "eval",
    "exec",
    "shell",
    "xp_cmdshell",
    "sleep",
    "benchmark",
    "pg_sleep",
    "current_user",
    "session_user",
    "current_setting"
}

# Disallowed DDL/DML AST expression classes in sqlglot
DISALLOWED_EXPRESSIONS: Tuple = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
    exp.TruncateTable,
    exp.Command,
    exp.Pragma,
    exp.Set,
    exp.Kill,
    exp.Grant,
    exp.Revoke,
    exp.Merge,
    exp.Transaction,
    exp.Commit,
    exp.Rollback
)

class SQLSecurityValidator:
    def __init__(self, max_row_limit: int = 500, dialect: str = "sqlite"):
        self.max_row_limit = max_row_limit
        self.dialect = dialect

    def validate(self, sql_query: str) -> SQLValidationResult:
        if not sql_query or not sql_query.strip():
            return SQLValidationResult(is_valid=False, error="Empty query provided.")

        clean_sql = sql_query.strip()
        
        # 1. Reject stacked queries or trailing multiple semicolons
        # Count semicolons outside string literals
        # Using sqlglot parse
        try:
            parsed_statements = sqlglot.parse(clean_sql, read=self.dialect)
        except Exception as e:
            return SQLValidationResult(
                is_valid=False,
                error=f"SQL syntax parse error: {str(e)}"
            )

        # Reject empty or multi-statement inputs
        parsed_statements = [s for s in parsed_statements if s is not None]
        if len(parsed_statements) == 0:
            return SQLValidationResult(is_valid=False, error="No valid SQL statements found.")
        if len(parsed_statements) > 1:
            return SQLValidationResult(
                is_valid=False,
                error="Multiple/stacked SQL statements are strictly prohibited."
            )

        root = parsed_statements[0]

        # 2. Accept only SELECT or CTE (WITH ... SELECT)
        if not isinstance(root, (exp.Select, exp.Union, exp.Query)):
            return SQLValidationResult(
                is_valid=False,
                error=f"Prohibited statement type '{root.__class__.__name__}'. Only read-only SELECT queries are permitted."
            )

        # 3. Check for any disallowed statement/expression classes anywhere in the AST
        for disallowed_cls in DISALLOWED_EXPRESSIONS:
            if list(root.find_all(disallowed_cls)):
                return SQLValidationResult(
                    is_valid=False,
                    error=f"Prohibited operation '{disallowed_cls.__name__}' detected. Write, schema-modifying, and administrative operations are rejected."
                )

        # 4. Collect CTE names to allow them as valid subquery identifiers
        cte_names = set()
        with_clause = root.find(exp.With)
        if with_clause:
            for cte in with_clause.expressions:
                if isinstance(cte, exp.CTE) and cte.alias:
                    cte_names.add(cte.alias.lower())

        # 5. Inspect all table references
        tables_accessed = []
        for tbl in root.find_all(exp.Table):
            t_name = tbl.name.lower() if tbl.name else ""
            if not t_name:
                continue

            # Check if system catalog
            if t_name in SYSTEM_TABLES or any(sys_t in t_name for sys_t in ["sqlite_", "pg_", "information_schema"]):
                return SQLValidationResult(
                    is_valid=False,
                    error=f"Access to system catalog/metadata table '{t_name}' is strictly prohibited."
                )

            # Check if CTE alias or in whitelist
            if t_name not in ALLOWED_TABLES and t_name not in cte_names:
                return SQLValidationResult(
                    is_valid=False,
                    error=f"Unauthorized table/view '{t_name}'. Queries may only access approved reporting tables and views."
                )

            if t_name in ALLOWED_TABLES and t_name not in tables_accessed:
                tables_accessed.append(t_name)

        # 6. Check all function calls for unsafe features
        for func in root.find_all(exp.Anonymous, exp.Func):
            func_name = (func.name if hasattr(func, "name") else func.__class__.__name__).lower()
            if func_name in UNSAFE_FUNCTIONS:
                return SQLValidationResult(
                    is_valid=False,
                    error=f"Prohibited database function '{func_name}' detected."
                )

        # 7. Check LIMIT enforcement
        limit_clause = root.find(exp.Limit)
        has_limit = False
        limit_val = None

        if limit_clause and limit_clause.expression:
            try:
                has_limit = True
                limit_val = int(limit_clause.expression.name)
            except (ValueError, AttributeError):
                has_limit = True
                limit_val = None

        # Build sanitized query string with enforced limit if needed
        sanitized = root.sql(dialect=self.dialect)
        if not has_limit or (limit_val is not None and limit_val > self.max_row_limit):
            # Enforce max row limit
            root.set("limit", exp.Limit(expression=exp.Literal.number(self.max_row_limit)))
            sanitized = root.sql(dialect=self.dialect)
            has_limit = True
            limit_val = self.max_row_limit

        return SQLValidationResult(
            is_valid=True,
            sanitized_query=sanitized,
            tables_accessed=tables_accessed,
            has_limit=has_limit,
            limit_value=limit_val
        )
