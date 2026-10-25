import pytest
from backend.app.analytics.business_calculations import calculation_engine

class TestBusinessCalculations:
    def test_calculate_margin(self):
        assert calculation_engine.calculate_margin(25, 100) == 25.0
        assert calculation_engine.calculate_margin(0, 100) == 0.0
        assert calculation_engine.calculate_margin(50, 0) == 0.0

    def test_calculate_growth_rate(self):
        res = calculation_engine.calculate_growth_rate(current_val=150, baseline_val=100)
        assert res["absolute_delta"] == 50.0
        assert res["percent_change"] == 50.0
        assert res["trend"] == "increased"

        res_drop = calculation_engine.calculate_growth_rate(current_val=60, baseline_val=100)
        assert res_drop["absolute_delta"] == -40.0
        assert res_drop["percent_change"] == -40.0
        assert res_drop["trend"] == "decreased"

    def test_pnl_waterfall(self):
        pnl = calculation_engine.calculate_profitability_metrics(
            gross_revenue=1000000.0,
            discounts=50000.0,
            cogs=600000.0,
            opex_logistics=100000.0,
            opex_storage=50000.0,
            opex_other=30000.0,
            spoilage_loss=20000.0
        )
        assert pnl["net_revenue"] == 950000.0
        assert pnl["gross_profit"] == 350000.0
        assert pnl["gross_margin_pct"] == 36.84
        assert pnl["total_opex"] == 180000.0
        assert pnl["operating_profit"] == 170000.0
        assert pnl["operating_margin_pct"] == 17.89
        assert pnl["net_profit"] == 150000.0
        assert pnl["net_margin_pct"] == 15.79

    def test_loss_reconciliation(self):
        rec = calculation_engine.calculate_financial_loss_breakdown(
            actual_profit=-5000000.0,
            baseline_profit=2800000.0,
            spoilage_direct_loss=2840000.0,
            excess_logistics_cost=1850000.0,
            revenue_gap_loss=3110000.0
        )
        assert rec["total_profit_deficit"] == 7800000.0
        assert rec["reconciled_sum"] == 7800000.0
        assert rec["is_fully_reconciled"] is True

    def test_logistics_kpis(self):
        kpi = calculation_engine.calculate_logistics_kpis(
            total_shipments=100,
            delayed_shipments=25,
            breached_cold_chain_count=15,
            total_cost_inr=500000.0,
            total_distance_km=10000.0
        )
        assert kpi["on_time_delivery_rate_pct"] == 75.0
        assert kpi["cold_chain_breach_rate_pct"] == 15.0
        assert kpi["avg_cost_per_km_inr"] == 50.0
        assert kpi["avg_cost_per_shipment_inr"] == 5000.0
