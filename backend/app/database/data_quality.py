from sqlalchemy import text
from backend.app.database.connection import engine

def check_data_quality():
    checks = []
    with engine.connect() as conn:
        # 1. Row counts check
        tables = [
            "regions", "warehouses", "products", "customers", "suppliers",
            "transport_routes", "sales_orders", "sales_order_items",
            "shipments", "vehicle_costs", "spoilage_records",
            "monthly_financials", "weather_observations"
        ]
        print("--- Table Row Counts ---")
        for tbl in tables:
            cnt = conn.execute(text(f"SELECT COUNT(*) FROM {tbl}")).scalar()
            print(f"  {tbl:25}: {cnt} rows")
            assert cnt > 0, f"Table {tbl} is empty!"
        
        # 2. Planted North India August 2024 verification
        row = conn.execute(text("""
            SELECT year, month, region_name, gross_revenue_inr, net_profit_inr, net_margin_pct, spoilage_loss_inr, opex_logistics_inr
            FROM v_monthly_regional_performance
            WHERE region_name = 'North India' AND year = 2024 AND month = 8
        """)).mappings().first()
        
        assert row is not None, "August 2024 North India record not found!"
        print("\n--- Planted Issue Verification (North India, Aug 2024) ---")
        print(f"  Gross Revenue: ₹{row['gross_revenue_inr']:,.2f}")
        print(f"  Net Profit: ₹{row['net_profit_inr']:,.2f}")
        print(f"  Net Margin: {row['net_margin_pct']}%")
        print(f"  Spoilage Loss: ₹{row['spoilage_loss_inr']:,.2f}")
        print(f"  Logistics OpEx: ₹{row['opex_logistics_inr']:,.2f}")
        assert row['net_profit_inr'] < 0, "North India August 2024 profit should be negative!"
        
        # 3. Check August 2023 vs August 2024 YoY comparison
        row_2023 = conn.execute(text("""
            SELECT net_profit_inr, net_margin_pct
            FROM v_monthly_regional_performance
            WHERE region_name = 'North India' AND year = 2023 AND month = 8
        """)).mappings().first()
        print(f"  Aug 2023 Net Profit: ₹{row_2023['net_profit_inr']:,.2f} ({row_2023['net_margin_pct']}%)")
        print(f"  Aug 2024 Net Profit: ₹{row['net_profit_inr']:,.2f} ({row['net_margin_pct']}%)")
        
        # 4. Spoilage cause breakdown in Aug 2024
        spoilage_res = conn.execute(text("""
            SELECT cause, SUM(spoilage_cost_inr) as total_loss, COUNT(*) as incidents
            FROM spoilage_records
            WHERE strftime('%Y-%m', record_date) = '2024-08'
            GROUP BY cause
        """)).mappings().all()
        print("\n--- Aug 2024 Spoilage Causes ---")
        for s in spoilage_res:
            print(f"  {s['cause']:45}: ₹{s['total_loss']:,.2f} across {s['incidents']} records")

        # 5. Route cost analysis
        route_res = conn.execute(text("""
            SELECT route_code, avg_delay_hours, cold_chain_breaches, avg_cost_per_km_inr
            FROM v_route_transportation_costs
            ORDER BY avg_cost_per_km_inr DESC
        """)).mappings().all()
        print("\n--- Route Performance & Costs ---")
        for r in route_res:
            print(f"  Route {r['route_code']:12}: avg delay {r['avg_delay_hours']} hrs, {r['cold_chain_breaches']} breaches, ₹{r['avg_cost_per_km_inr']}/km")

    print("\nAll data quality and planted problem checks PASSED successfully!")
    return True

if __name__ == "__main__":
    check_data_quality()
