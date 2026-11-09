from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text, Index, text
)
from sqlalchemy.orm import relationship
from backend.app.database.connection import Base, engine

class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # North, South, West, East, Central
    code = Column(String(10), unique=True, nullable=False)
    state_coverage = Column(String(200))
    headquarters_city = Column(String(50))

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    city = Column(String(50), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    total_capacity_sqft = Column(Integer)
    cold_storage_capacity_sqft = Column(Integer)
    chiller_operational_status = Column(String(30), default="Optimal")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(30), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)  # Dairy, Fresh Produce, Poultry, Frozen, Bakery
    subcategory = Column(String(50))
    unit_cost_inr = Column(Float, nullable=False)
    base_selling_price_inr = Column(Float, nullable=False)
    storage_temp_min_c = Column(Float)
    storage_temp_max_c = Column(Float)
    shelf_life_days = Column(Integer)
    is_perishable = Column(Boolean, default=True)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    customer_type = Column(String(50))  # Retail Chain, Quick Commerce, Supermarket, Hotel/Horeca
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    city = Column(String(50), nullable=False)
    credit_terms_days = Column(Integer, default=30)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    quality_rating = Column(Float, default=4.5)

class TransportRoute(Base):
    __tablename__ = "transport_routes"
    id = Column(Integer, primary_key=True, index=True)
    route_code = Column(String(30), unique=True, nullable=False)
    origin_city = Column(String(50), nullable=False)
    destination_city = Column(String(50), nullable=False)
    origin_warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    distance_km = Column(Float, nullable=False)
    transit_time_hours_expected = Column(Float, nullable=False)
    base_cost_per_km = Column(Float, nullable=False)
    refrigeration_required = Column(Boolean, default=True)

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(40), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    order_date = Column(Date, nullable=False, index=True)
    expected_delivery_date = Column(Date)
    actual_delivery_date = Column(Date)
    status = Column(String(30), default="Delivered")  # Delivered, Delayed, Cancelled
    total_revenue_inr = Column(Float, nullable=False)
    total_cogs_inr = Column(Float, nullable=False)
    total_discount_inr = Column(Float, default=0.0)

class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost_inr = Column(Float, nullable=False)
    unit_price_inr = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0.0)
    line_total_inr = Column(Float, nullable=False)
    line_cogs_inr = Column(Float, nullable=False)

class InventorySnapshot(Base):
    __tablename__ = "inventory_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(Date, nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_on_hand = Column(Integer, nullable=False)
    inventory_holding_cost_inr = Column(Float, nullable=False)
    days_of_inventory = Column(Float)

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    id = Column(Integer, primary_key=True, index=True)
    movement_date = Column(Date, nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    movement_type = Column(String(50))  # Transfer, Inbound, Outbound, Spoilage Write-Off
    quantity = Column(Integer, nullable=False)
    unit_cost_inr = Column(Float, nullable=False)

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    shipment_number = Column(String(40), unique=True, nullable=False)
    route_id = Column(Integer, ForeignKey("transport_routes.id"), nullable=False)
    origin_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    vehicle_id = Column(String(30), nullable=False)
    dispatch_datetime = Column(DateTime, nullable=False, index=True)
    delivery_datetime = Column(DateTime)
    delay_hours = Column(Float, default=0.0)
    cold_chain_breached = Column(Boolean, default=False)
    temperature_recorded_c = Column(Float)
    shipment_cost_inr = Column(Float, nullable=False)
    status = Column(String(30), default="Completed")  # Completed, Delayed, Disrupted
    delay_reason = Column(String(200))

class DeliveryEvent(Base):
    __tablename__ = "delivery_events"
    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    event_datetime = Column(DateTime, nullable=False)
    location_name = Column(String(100))
    event_type = Column(String(50))  # Dispatched, In-Transit, Delayed-Weather, Delivered
    note = Column(Text)

class VehicleCost(Base):
    __tablename__ = "vehicle_costs"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String(30), nullable=False)
    route_id = Column(Integer, ForeignKey("transport_routes.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    fuel_cost_inr = Column(Float, nullable=False)
    refrigeration_fuel_cost_inr = Column(Float, default=0.0)
    maintenance_cost_inr = Column(Float, default=0.0)
    driver_overtime_cost_inr = Column(Float, default=0.0)
    total_vehicle_cost_inr = Column(Float, nullable=False)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(40), unique=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    received_date = Column(Date)
    total_amount_inr = Column(Float, nullable=False)
    status = Column(String(30), default="Received")

class SpoilageRecord(Base):
    __tablename__ = "spoilage_records"
    id = Column(Integer, primary_key=True, index=True)
    record_date = Column(Date, nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_spoiled = Column(Integer, nullable=False)
    spoilage_cost_inr = Column(Float, nullable=False)
    cause = Column(String(100), nullable=False)  # Cold Chain Breach, Chiller Compressor Failure, Delivery Delay, Expiry
    notes = Column(Text)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    expense_date = Column(Date, nullable=False, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    expense_category = Column(String(50), nullable=False)  # Logistics, Storage, SG&A, Maintenance
    amount_inr = Column(Float, nullable=False)
    description = Column(String(200))

class MonthlyFinancial(Base):
    __tablename__ = "monthly_financials"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    gross_revenue_inr = Column(Float, nullable=False)
    net_revenue_inr = Column(Float, nullable=False)
    cogs_inr = Column(Float, nullable=False)
    gross_profit_inr = Column(Float, nullable=False)
    gross_margin_pct = Column(Float, nullable=False)
    opex_logistics_inr = Column(Float, nullable=False)
    opex_storage_inr = Column(Float, nullable=False)
    opex_other_inr = Column(Float, nullable=False)
    operating_profit_inr = Column(Float, nullable=False)
    operating_margin_pct = Column(Float, nullable=False)
    spoilage_loss_inr = Column(Float, default=0.0)
    net_profit_inr = Column(Float, nullable=False)
    net_margin_pct = Column(Float, nullable=False)

class WeatherObservation(Base):
    __tablename__ = "weather_observations"
    id = Column(Integer, primary_key=True, index=True)
    observation_date = Column(Date, nullable=False, index=True)
    city = Column(String(50), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    temp_max_c = Column(Float)
    temp_min_c = Column(Float)
    precipitation_mm = Column(Float, default=0.0)
    weather_condition = Column(String(50))  # Clear, Moderate Rain, Heavy Monsoon, Heatwave
    source = Column(String(50), default="Open-Meteo Historical")

# Indexes
Index("idx_orders_region_date", SalesOrder.region_id, SalesOrder.order_date)
Index("idx_shipments_route_date", Shipment.route_id, Shipment.dispatch_datetime)
Index("idx_spoilage_prod_date", SpoilageRecord.product_id, SpoilageRecord.record_date)
Index("idx_monthly_fin_yr_mo_reg", MonthlyFinancial.year, MonthlyFinancial.month, MonthlyFinancial.region_id)

VIEW_DEFINITIONS = [
    """
    CREATE VIEW IF NOT EXISTS v_monthly_regional_performance AS
    SELECT 
        mf.year,
        mf.month,
        r.name AS region_name,
        r.code AS region_code,
        mf.gross_revenue_inr,
        mf.net_revenue_inr,
        mf.cogs_inr,
        mf.gross_profit_inr,
        mf.gross_margin_pct,
        mf.opex_logistics_inr,
        mf.opex_storage_inr,
        mf.operating_profit_inr,
        mf.operating_margin_pct,
        mf.spoilage_loss_inr,
        mf.net_profit_inr,
        mf.net_margin_pct
    FROM monthly_financials mf
    JOIN regions r ON mf.region_id = r.id;
    """,
    """
    CREATE VIEW IF NOT EXISTS v_product_profitability AS
    SELECT 
        p.id AS product_id,
        p.name AS product_name,
        p.category,
        p.unit_cost_inr,
        p.base_selling_price_inr,
        SUM(soi.quantity) AS total_units_sold,
        ROUND(SUM(soi.line_total_inr), 2) AS total_revenue_inr,
        ROUND(SUM(soi.line_cogs_inr), 2) AS total_cogs_inr,
        ROUND(SUM(soi.line_total_inr - soi.line_cogs_inr), 2) AS gross_profit_inr,
        ROUND((SUM(soi.line_total_inr - soi.line_cogs_inr) * 100.0 / NULLIF(SUM(soi.line_total_inr), 0)), 2) AS gross_margin_pct
    FROM products p
    JOIN sales_order_items soi ON p.id = soi.product_id
    GROUP BY p.id, p.name, p.category, p.unit_cost_inr, p.base_selling_price_inr;
    """,
    """
    CREATE VIEW IF NOT EXISTS v_route_transportation_costs AS
    SELECT 
        tr.route_code,
        tr.origin_city,
        tr.destination_city,
        tr.distance_km,
        COUNT(s.id) AS total_shipments,
        ROUND(AVG(s.delay_hours), 2) AS avg_delay_hours,
        SUM(CASE WHEN s.cold_chain_breached = 1 THEN 1 ELSE 0 END) AS cold_chain_breaches,
        ROUND(SUM(s.shipment_cost_inr), 2) AS total_shipment_costs_inr,
        ROUND(AVG(s.shipment_cost_inr / NULLIF(tr.distance_km, 0)), 2) AS avg_cost_per_km_inr
    FROM transport_routes tr
    LEFT JOIN shipments s ON tr.id = s.route_id
    GROUP BY tr.id, tr.route_code, tr.origin_city, tr.destination_city, tr.distance_km;
    """,
    """
    CREATE VIEW IF NOT EXISTS v_spoilage_summary AS
    SELECT 
        sr.cause,
        p.category AS product_category,
        p.name AS product_name,
        w.name AS warehouse_name,
        r.name AS region_name,
        strftime('%Y-%m', sr.record_date) AS year_month,
        COUNT(sr.id) AS incidents_count,
        SUM(sr.quantity_spoiled) AS total_units_spoiled,
        ROUND(SUM(sr.spoilage_cost_inr), 2) AS total_loss_inr
    FROM spoilage_records sr
    JOIN products p ON sr.product_id = p.id
    LEFT JOIN warehouses w ON sr.warehouse_id = w.id
    LEFT JOIN regions r ON w.region_id = r.id
    GROUP BY sr.cause, p.category, p.name, w.name, r.name, strftime('%Y-%m', sr.record_date);
    """,
    """
    CREATE VIEW IF NOT EXISTS v_regional_product_profitability AS
    SELECT 
        r.name AS region_name,
        r.code AS region_code,
        p.sku,
        p.name AS product_name,
        p.category,
        p.unit_cost_inr AS production_cost_inr,
        ROUND(AVG(soi.unit_price_inr), 2) AS avg_selling_price_inr,
        SUM(soi.quantity) AS total_units_sold,
        ROUND(SUM(soi.line_total_inr), 2) AS total_revenue_inr,
        ROUND(SUM(soi.line_cogs_inr), 2) AS total_cogs_inr,
        ROUND(SUM(soi.line_total_inr - soi.line_cogs_inr), 2) AS gross_profit_inr,
        ROUND((SUM(soi.line_total_inr - soi.line_cogs_inr) * 100.0 / NULLIF(SUM(soi.line_total_inr), 0)), 2) AS gross_margin_pct
    FROM sales_order_items soi
    JOIN sales_orders so ON soi.order_id = so.id
    JOIN regions r ON so.region_id = r.id
    JOIN products p ON soi.product_id = p.id
    GROUP BY r.name, r.code, p.sku, p.name, p.category, p.unit_cost_inr;
    """
]

def init_db(target_engine=None):
    """Initializes tables and reporting views."""
    curr_engine = target_engine or engine
    Base.metadata.create_all(bind=curr_engine)
    with curr_engine.connect() as conn:
        for view_sql in VIEW_DEFINITIONS:
            conn.execute(text(view_sql))
        conn.commit()
