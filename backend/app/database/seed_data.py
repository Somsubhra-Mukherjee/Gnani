import random
from datetime import date, datetime, timedelta
import numpy as np
from sqlalchemy.orm import Session
from backend.app.database.connection import engine, SessionLocal
from backend.app.database.schema import (
    init_db, Region, Warehouse, Product, Customer, Supplier, TransportRoute,
    SalesOrder, SalesOrderItem, InventorySnapshot, InventoryMovement,
    Shipment, DeliveryEvent, VehicleCost, PurchaseOrder, SpoilageRecord,
    Expense, MonthlyFinancial, WeatherObservation
)

def seed_all_data(db: Session, seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)

    print("Cleaning old data...")
    db.query(DeliveryEvent).delete()
    db.query(Shipment).delete()
    db.query(VehicleCost).delete()
    db.query(SalesOrderItem).delete()
    db.query(SalesOrder).delete()
    db.query(SpoilageRecord).delete()
    db.query(InventoryMovement).delete()
    db.query(InventorySnapshot).delete()
    db.query(PurchaseOrder).delete()
    db.query(Expense).delete()
    db.query(MonthlyFinancial).delete()
    db.query(WeatherObservation).delete()
    db.query(Customer).delete()
    db.query(Supplier).delete()
    db.query(TransportRoute).delete()
    db.query(Warehouse).delete()
    db.query(Product).delete()
    db.query(Region).delete()
    db.commit()

    print("1. Seeding Regions...")
    regions_data = [
        {"name": "North India", "code": "REG-NORTH", "state_coverage": "Delhi, Punjab, Haryana, UP, Rajasthan, J&K", "headquarters_city": "Delhi"},
        {"name": "South India", "code": "REG-SOUTH", "state_coverage": "Karnataka, Tamil Nadu, Telangana, Kerala", "headquarters_city": "Bengaluru"},
        {"name": "West India", "code": "REG-WEST", "state_coverage": "Maharashtra, Gujarat, Goa", "headquarters_city": "Mumbai"},
        {"name": "East India", "code": "REG-EAST", "state_coverage": "West Bengal, Odisha, Bihar, Assam", "headquarters_city": "Kolkata"},
        {"name": "Central India", "code": "REG-CENTRAL", "state_coverage": "Madhya Pradesh, Chhattisgarh", "headquarters_city": "Indore"}
    ]
    regions = {}
    for r in regions_data:
        obj = Region(**r)
        db.add(obj)
        db.flush()
        regions[r["name"]] = obj

    print("2. Seeding Warehouses...")
    warehouses_data = [
        {"name": "Delhi Central Distribution Centre", "code": "WH-DEL-01", "region_id": regions["North India"].id, "city": "Delhi", "latitude": 28.6139, "longitude": 77.2090, "total_capacity_sqft": 65000, "cold_storage_capacity_sqft": 35000, "chiller_operational_status": "Optimal"},
        {"name": "Jaipur Cold Hub", "code": "WH-JAI-01", "region_id": regions["North India"].id, "city": "Jaipur", "latitude": 26.9124, "longitude": 75.7873, "total_capacity_sqft": 30000, "cold_storage_capacity_sqft": 18000, "chiller_operational_status": "Optimal"},
        {"name": "Chandigarh Perishables Depot", "code": "WH-CHD-01", "region_id": regions["North India"].id, "city": "Chandigarh", "latitude": 30.7333, "longitude": 76.7794, "total_capacity_sqft": 25000, "cold_storage_capacity_sqft": 15000, "chiller_operational_status": "Optimal"},
        {"name": "Bengaluru Mega Logistics Hub", "code": "WH-BLR-01", "region_id": regions["South India"].id, "city": "Bengaluru", "latitude": 12.9716, "longitude": 77.5946, "total_capacity_sqft": 80000, "cold_storage_capacity_sqft": 45000, "chiller_operational_status": "Optimal"},
        {"name": "Hyderabad Storage Facility", "code": "WH-HYD-01", "region_id": regions["South India"].id, "city": "Hyderabad", "latitude": 17.3850, "longitude": 78.4867, "total_capacity_sqft": 40000, "cold_storage_capacity_sqft": 22000, "chiller_operational_status": "Optimal"},
        {"name": "Mumbai Bhiwandi Master DC", "code": "WH-BHW-01", "region_id": regions["West India"].id, "city": "Mumbai", "latitude": 19.2969, "longitude": 73.0631, "total_capacity_sqft": 90000, "cold_storage_capacity_sqft": 50000, "chiller_operational_status": "Optimal"},
        {"name": "Ahmedabad Cold Depot", "code": "WH-AMD-01", "region_id": regions["West India"].id, "city": "Ahmedabad", "latitude": 23.0225, "longitude": 72.5714, "total_capacity_sqft": 35000, "cold_storage_capacity_sqft": 20000, "chiller_operational_status": "Optimal"},
        {"name": "Kolkata Dankuni Hub", "code": "WH-KOL-01", "region_id": regions["East India"].id, "city": "Kolkata", "latitude": 22.5726, "longitude": 88.3639, "total_capacity_sqft": 50000, "cold_storage_capacity_sqft": 28000, "chiller_operational_status": "Optimal"}
    ]
    warehouses = {}
    for w in warehouses_data:
        obj = Warehouse(**w)
        db.add(obj)
        db.flush()
        warehouses[w["code"]] = obj

    print("3. Seeding Products...")
    products_data = [
        {"sku": "PRD-DAIRY-01", "name": "Fresh Organic Paneer 500g", "category": "Dairy", "subcategory": "Paneer", "unit_cost_inr": 160.0, "base_selling_price_inr": 230.0, "storage_temp_min_c": 2.0, "storage_temp_max_c": 4.0, "shelf_life_days": 12, "is_perishable": True},
        {"sku": "PRD-DAIRY-02", "name": "Pasteurized Full Cream Milk 1L", "category": "Dairy", "subcategory": "Milk", "unit_cost_inr": 48.0, "base_selling_price_inr": 66.0, "storage_temp_min_c": 2.0, "storage_temp_max_c": 4.0, "shelf_life_days": 4, "is_perishable": True},
        {"sku": "PRD-DAIRY-03", "name": "Cultured Salted Butter 500g", "category": "Dairy", "subcategory": "Butter", "unit_cost_inr": 210.0, "base_selling_price_inr": 285.0, "storage_temp_min_c": -2.0, "storage_temp_max_c": 4.0, "shelf_life_days": 90, "is_perishable": True},
        {"sku": "PRD-DAIRY-04", "name": "Artisanal Greek Yogurt 400g", "category": "Dairy", "subcategory": "Yogurt", "unit_cost_inr": 85.0, "base_selling_price_inr": 135.0, "storage_temp_min_c": 2.0, "storage_temp_max_c": 5.0, "shelf_life_days": 15, "is_perishable": True},
        {"sku": "PRD-VEG-01", "name": "Hydroponic English Cucumber 1kg", "category": "Fresh Produce", "subcategory": "Exotics", "unit_cost_inr": 55.0, "base_selling_price_inr": 95.0, "storage_temp_min_c": 8.0, "storage_temp_max_c": 12.0, "shelf_life_days": 7, "is_perishable": True},
        {"sku": "PRD-VEG-02", "name": "Premium Baby Spinach 250g", "category": "Fresh Produce", "subcategory": "Leafy Greens", "unit_cost_inr": 25.0, "base_selling_price_inr": 48.0, "storage_temp_min_c": 2.0, "storage_temp_max_c": 5.0, "shelf_life_days": 5, "is_perishable": True},
        {"sku": "PRD-VEG-03", "name": "Shimla Royal Delicious Apples 1kg", "category": "Fresh Produce", "subcategory": "Fruits", "unit_cost_inr": 110.0, "base_selling_price_inr": 170.0, "storage_temp_min_c": 1.0, "storage_temp_max_c": 4.0, "shelf_life_days": 30, "is_perishable": True},
        {"sku": "PRD-VEG-04", "name": "Alphonso Mango Pulp 1L", "category": "Fresh Produce", "subcategory": "Processed Fruits", "unit_cost_inr": 180.0, "base_selling_price_inr": 290.0, "storage_temp_min_c": 4.0, "storage_temp_max_c": 10.0, "shelf_life_days": 60, "is_perishable": True},
        {"sku": "PRD-MEAT-01", "name": "Antibiotic-Free Fresh Chicken Breast 500g", "category": "Poultry & Meat", "subcategory": "Poultry", "unit_cost_inr": 140.0, "base_selling_price_inr": 215.0, "storage_temp_min_c": -1.0, "storage_temp_max_c": 2.0, "shelf_life_days": 5, "is_perishable": True},
        {"sku": "PRD-FROZEN-01", "name": "Frozen Sweet Corn 1kg", "category": "Frozen Foods", "subcategory": "Vegetables", "unit_cost_inr": 75.0, "base_selling_price_inr": 125.0, "storage_temp_min_c": -18.0, "storage_temp_max_c": -15.0, "shelf_life_days": 180, "is_perishable": False},
        {"sku": "PRD-BAKERY-01", "name": "Stoneground Whole Wheat Sourdough 400g", "category": "Bakery", "subcategory": "Bread", "unit_cost_inr": 45.0, "base_selling_price_inr": 85.0, "storage_temp_min_c": 18.0, "storage_temp_max_c": 24.0, "shelf_life_days": 4, "is_perishable": True}
    ]
    products = {}
    for p in products_data:
        obj = Product(**p)
        db.add(obj)
        db.flush()
        products[p["sku"]] = obj

    print("4. Seeding Customers & Suppliers...")
    customers_data = [
        {"name": "FreshHyper Supermarkets North", "customer_type": "Supermarket Chain", "region_id": regions["North India"].id, "city": "Delhi"},
        {"name": "BlinkNow Quick Commerce Delhi", "customer_type": "Quick Commerce", "region_id": regions["North India"].id, "city": "Gurgaon"},
        {"name": "Northern Star Luxury Hotels", "customer_type": "Horeca", "region_id": regions["North India"].id, "city": "Jaipur"},
        {"name": "Punjab Fresh Gourmet Stores", "customer_type": "Retail Chain", "region_id": regions["North India"].id, "city": "Chandigarh"},
        {"name": "Southern Spices Superstore", "customer_type": "Supermarket Chain", "region_id": regions["South India"].id, "city": "Bengaluru"},
        {"name": "ZeptoSwift Bengaluru Dark Stores", "customer_type": "Quick Commerce", "region_id": regions["South India"].id, "city": "Bengaluru"},
        {"name": "WestCoast Gourmet Marts", "customer_type": "Retail Chain", "region_id": regions["West India"].id, "city": "Mumbai"},
        {"name": "Gujarat Fresh Grocers Association", "customer_type": "Wholesale Distributor", "region_id": regions["West India"].id, "city": "Ahmedabad"},
        {"name": "Bengal Daily Essentials Retail", "customer_type": "Supermarket Chain", "region_id": regions["East India"].id, "city": "Kolkata"}
    ]
    customers = []
    for c in customers_data:
        obj = Customer(**c)
        db.add(obj)
        db.flush()
        customers.append(obj)

    suppliers_data = [
        {"name": "Punjab Dairy Cooperative Farms", "category": "Dairy Farm", "city": "Ludhiana", "state": "Punjab", "quality_rating": 4.8},
        {"name": "Himachal Apple Orchards & Co", "category": "Fruit Producer", "city": "Shimla", "state": "Himachal Pradesh", "quality_rating": 4.6},
        {"name": "Haryana Hydroponic Produce LLP", "category": "Hydroponic Veg", "city": "Karnal", "state": "Haryana", "quality_rating": 4.7},
        {"name": "Ratnagiri Mango Growers Syndicate", "category": "Fruit Producer", "city": "Ratnagiri", "state": "Maharashtra", "quality_rating": 4.9},
        {"name": "Malnad Organic Farm Dairies", "category": "Dairy Farm", "city": "Hassan", "state": "Karnataka", "quality_rating": 4.8}
    ]
    for s in suppliers_data:
        db.add(Supplier(**s))
    db.flush()

    print("5. Seeding Transport Routes...")
    routes_data = [
        {"route_code": "RT-DEL-CHD", "origin_city": "Delhi", "destination_city": "Chandigarh", "origin_warehouse_id": warehouses["WH-DEL-01"].id, "distance_km": 245.0, "transit_time_hours_expected": 5.5, "base_cost_per_km": 42.0, "refrigeration_required": True},
        {"route_code": "RT-DEL-JAI", "origin_city": "Delhi", "destination_city": "Jaipur", "origin_warehouse_id": warehouses["WH-DEL-01"].id, "distance_km": 280.0, "transit_time_hours_expected": 6.0, "base_cost_per_km": 44.0, "refrigeration_required": True},
        {"route_code": "RT-DEL-SXR", "origin_city": "Delhi", "destination_city": "Srinagar", "origin_warehouse_id": warehouses["WH-DEL-01"].id, "distance_km": 810.0, "transit_time_hours_expected": 22.0, "base_cost_per_km": 68.0, "refrigeration_required": True},
        {"route_code": "RT-BLR-HYD", "origin_city": "Bengaluru", "destination_city": "Hyderabad", "origin_warehouse_id": warehouses["WH-BLR-01"].id, "distance_km": 570.0, "transit_time_hours_expected": 10.0, "base_cost_per_km": 38.0, "refrigeration_required": True},
        {"route_code": "RT-BHW-AMD", "origin_city": "Mumbai", "destination_city": "Ahmedabad", "origin_warehouse_id": warehouses["WH-BHW-01"].id, "distance_km": 525.0, "transit_time_hours_expected": 10.5, "base_cost_per_km": 39.0, "refrigeration_required": True},
        {"route_code": "RT-BHW-PUN", "origin_city": "Mumbai", "destination_city": "Pune", "origin_warehouse_id": warehouses["WH-BHW-01"].id, "distance_km": 150.0, "transit_time_hours_expected": 3.5, "base_cost_per_km": 45.0, "refrigeration_required": True}
    ]
    routes = {}
    for r in routes_data:
        obj = TransportRoute(**r)
        db.add(obj)
        db.flush()
        routes[r["route_code"]] = obj

    print("6. Seeding Historical Weather Data (2023 - 2025)...")
    # In August 2024, North India experienced severe rainfall & flash flood warnings
    cities = [
        ("Delhi", regions["North India"].id),
        ("Jaipur", regions["North India"].id),
        ("Chandigarh", regions["North India"].id),
        ("Bengaluru", regions["South India"].id),
        ("Mumbai", regions["West India"].id),
        ("Kolkata", regions["East India"].id)
    ]
    
    start_dt = date(2023, 1, 1)
    end_dt = date(2025, 12, 31)
    cur = start_dt
    
    weather_objs = []
    while cur <= end_dt:
        for city_name, reg_id in cities:
            is_monsoon = cur.month in [7, 8, 9]
            is_august_2024_north = (cur.year == 2024 and cur.month == 8 and city_name in ["Delhi", "Chandigarh", "Jaipur"])
            
            if is_august_2024_north:
                # Planted severe monsoon weather event
                t_max = round(random.uniform(32.0, 36.5), 1)
                t_min = round(random.uniform(26.0, 28.5), 1)
                precip = round(random.uniform(45.0, 140.0), 1) if random.random() < 0.75 else round(random.uniform(10.0, 30.0), 1)
                condition = "Severe Monsoon & Waterlogging" if precip > 50 else "Heavy Rain"
            elif is_monsoon:
                t_max = round(random.uniform(29.0, 33.0), 1)
                t_min = round(random.uniform(23.0, 26.0), 1)
                precip = round(random.uniform(5.0, 35.0), 1) if random.random() < 0.4 else 0.0
                condition = "Monsoon Showers" if precip > 0 else "Overcast"
            else:
                t_max = round(random.uniform(20.0, 32.0), 1)
                t_min = round(random.uniform(10.0, 20.0), 1)
                precip = 0.0 if random.random() < 0.9 else round(random.uniform(1.0, 8.0), 1)
                condition = "Clear" if precip == 0 else "Scattered Light Rain"

            weather_objs.append(WeatherObservation(
                observation_date=cur,
                city=city_name,
                region_id=reg_id,
                temp_max_c=t_max,
                temp_min_c=t_min,
                precipitation_mm=precip,
                weather_condition=condition,
                source="Open-Meteo Historical Archive"
            ))
        cur += timedelta(days=1)
    db.bulk_save_objects(weather_objs)
    db.flush()

    print("7. Seeding Historical Shipments and Planted Disruption...")
    # Shipments every 2-3 days on key routes
    shipment_objs = []
    event_objs = []
    cost_objs = []
    spoilage_objs = []
    
    cur_date = date(2023, 1, 1)
    shipment_counter = 1000
    
    while cur_date <= end_dt:
        for r_code, r_obj in routes.items():
            if random.random() < 0.65:
                shipment_counter += 1
                s_num = f"SHP-{cur_date.year}-{shipment_counter}"
                dispatch_time = datetime.combine(cur_date, datetime.min.time()) + timedelta(hours=random.randint(4, 8))
                
                # Check for planted crisis: August 2024 on North routes RT-DEL-CHD, RT-DEL-JAI, RT-DEL-SXR
                is_crisis_period = (cur_date.year == 2024 and cur_date.month == 8 and r_code in ["RT-DEL-CHD", "RT-DEL-JAI", "RT-DEL-SXR"])
                
                if is_crisis_period:
                    # Significant transit delays and cold chain failures
                    delay = round(random.uniform(18.0, 38.0), 1)
                    cold_chain_breach = True if random.random() < 0.85 else False
                    temp_recorded = round(random.uniform(14.5, 19.8), 1) if cold_chain_breach else round(random.uniform(3.0, 4.5), 1)
                    # Emergency transport surcharges
                    shipment_cost = round(r_obj.distance_km * r_obj.base_cost_per_km * random.uniform(1.8, 2.6), 2)
                    status = "Delayed - Disrupted"
                    delay_reason = "NH44 Highway Flooding & Cold Chain Breakdown"
                else:
                    delay = round(random.uniform(0.0, 3.5), 1) if random.random() < 0.2 else 0.0
                    cold_chain_breach = True if random.random() < 0.03 else False
                    temp_recorded = round(random.uniform(2.5, 4.2), 1)
                    shipment_cost = round(r_obj.distance_km * r_obj.base_cost_per_km * random.uniform(0.95, 1.1), 2)
                    status = "Delayed" if delay > 2.0 else "Completed"
                    delay_reason = "Minor Traffic Congestion" if delay > 0 else "On-Time Schedule"

                delivery_time = dispatch_time + timedelta(hours=r_obj.transit_time_hours_expected + delay)
                
                s_obj = Shipment(
                    shipment_number=s_num,
                    route_id=r_obj.id,
                    origin_warehouse_id=r_obj.origin_warehouse_id,
                    vehicle_id=f"TRK-{r_code[-3:]}-{random.randint(101, 140)}",
                    dispatch_datetime=dispatch_time,
                    delivery_datetime=delivery_time,
                    delay_hours=delay,
                    cold_chain_breached=cold_chain_breach,
                    temperature_recorded_c=temp_recorded,
                    shipment_cost_inr=shipment_cost,
                    status=status,
                    delay_reason=delay_reason
                )
                db.add(s_obj)
                db.flush()
                
                # Associated vehicle cost
                fuel = round(shipment_cost * 0.45, 2)
                refrig_fuel = round(shipment_cost * (0.35 if is_crisis_period else 0.15), 2)
                maint = round(shipment_cost * (0.25 if is_crisis_period else 0.08), 2)
                overtime = round(shipment_cost * (0.20 if is_crisis_period else 0.05), 2)
                cost_objs.append(VehicleCost(
                    vehicle_id=s_obj.vehicle_id,
                    route_id=r_obj.id,
                    date=cur_date,
                    fuel_cost_inr=fuel,
                    refrigeration_fuel_cost_inr=refrig_fuel,
                    maintenance_cost_inr=maint,
                    driver_overtime_cost_inr=overtime,
                    total_vehicle_cost_inr=fuel + refrig_fuel + maint + overtime
                ))
                
                # If cold chain was breached, record severe spoilage
                if cold_chain_breach:
                    # Choose a dairy or perishable product
                    spoiled_prod = products["PRD-DAIRY-01"] if random.random() < 0.5 else products["PRD-DAIRY-02"]
                    qty_spoiled = random.randint(350, 800) if is_crisis_period else random.randint(40, 120)
                    spoilage_cost = round(qty_spoiled * spoiled_prod.unit_cost_inr, 2)
                    spoilage_objs.append(SpoilageRecord(
                        record_date=cur_date,
                        warehouse_id=r_obj.origin_warehouse_id,
                        shipment_id=s_obj.id,
                        product_id=spoiled_prod.id,
                        quantity_spoiled=qty_spoiled,
                        spoilage_cost_inr=spoilage_cost,
                        cause="Cold Chain Breach During Highway Delay",
                        notes=f"Vehicle {s_obj.vehicle_id} delayed by {delay} hrs on {r_code}. Temp rose to {temp_recorded}°C."
                    ))
        cur_date += timedelta(days=2)
        
    db.bulk_save_objects(cost_objs)
    db.bulk_save_objects(spoilage_objs)
    db.flush()

    print("8. Seeding Planted August 2024 Warehouse Chiller Breakdown...")
    # Delhi Central Chiller Compressor breakdown between Aug 11 and Aug 16, 2024
    delhi_wh = warehouses["WH-DEL-01"]
    for day_off in range(11, 17):
        chiller_date = date(2024, 8, day_off)
        for p_sku in ["PRD-DAIRY-01", "PRD-DAIRY-03", "PRD-MEAT-01"]:
            p = products[p_sku]
            qty_loss = random.randint(600, 1100)
            loss_val = round(qty_loss * p.unit_cost_inr, 2)
            db.add(SpoilageRecord(
                record_date=chiller_date,
                warehouse_id=delhi_wh.id,
                shipment_id=None,
                product_id=p.id,
                quantity_spoiled=qty_loss,
                spoilage_cost_inr=loss_val,
                cause="Chiller Compressor Failure at Depot",
                notes="Primary and backup compressors failed. Ambient temp reached 16.5°C in cold chamber 2."
            ))
    db.flush()

    print("9. Generating Reconciled Sales Orders & Monthly Financials (2023 - 2025)...")
    # For every month and region, create realistic transactional volume and reconcile financials
    order_id_counter = 50000
    for yr in [2023, 2024, 2025]:
        for mo in range(1, 13):
            for reg_name, reg_obj in regions.items():
                is_north = (reg_name == "North India")
                is_aug_2024_north = (yr == 2024 and mo == 8 and is_north)
                is_july_2024_north = (yr == 2024 and mo == 7 and is_north)
                
                # Base monthly revenue range per region: ~ ₹1.2 Cr to ₹2.5 Cr
                base_rev = random.uniform(16000000, 24000000)
                if is_north:
                    base_rev = 22000000 # Healthy ~2.2 Cr
                
                # If August 2024 North India: sales were lower due to stockouts & order cancellations
                if is_aug_2024_north:
                    gross_revenue = 18500000.0  # ₹1.85 Cr
                    discount_pct = 0.08
                    net_revenue = round(gross_revenue * (1 - discount_pct), 2)
                    cogs = round(net_revenue * 0.72, 2)
                    gross_profit = round(net_revenue - cogs, 2)
                    gross_margin = round((gross_profit / net_revenue) * 100, 2)
                    
                    # Logistical costs skyrocketed (+ ₹18.5 L) due to emergency transport & detours
                    opex_logistics = 3450000.0  # Normally ~16 L
                    opex_storage = 2100000.0    # Normally ~12 L (repair & rented backup chillers)
                    opex_other = 1400000.0
                    
                    # Direct spoilage loss recorded this month was ₹28.4 Lakhs
                    spoilage_loss = 2840000.0
                    
                    operating_profit = round(gross_profit - opex_logistics - opex_storage - opex_other, 2)
                    operating_margin = round((operating_profit / net_revenue) * 100, 2)
                    
                    # Net Profit goes NEGATIVE into loss!
                    net_profit = round(operating_profit - spoilage_loss, 2)
                    net_margin = round((net_profit / net_revenue) * 100, 2)
                    
                elif is_july_2024_north:
                    # Early monsoon warning month
                    gross_revenue = 20500000.0
                    discount_pct = 0.05
                    net_revenue = round(gross_revenue * (1 - discount_pct), 2)
                    cogs = round(net_revenue * 0.68, 2)
                    gross_profit = round(net_revenue - cogs, 2)
                    gross_margin = round((gross_profit / net_revenue) * 100, 2)
                    opex_logistics = 2100000.0
                    opex_storage = 1350000.0
                    opex_other = 1200000.0
                    spoilage_loss = 820000.0
                    operating_profit = round(gross_profit - opex_logistics - opex_storage - opex_other, 2)
                    operating_margin = round((operating_profit / net_revenue) * 100, 2)
                    net_profit = round(operating_profit - spoilage_loss, 2)
                    net_margin = round((net_profit / net_revenue) * 100, 2)
                else:
                    # Normal healthy month
                    gross_revenue = round(base_rev * random.uniform(0.95, 1.15), 2)
                    discount_pct = random.uniform(0.03, 0.06)
                    net_revenue = round(gross_revenue * (1 - discount_pct), 2)
                    cogs = round(net_revenue * random.uniform(0.64, 0.67), 2)
                    gross_profit = round(net_revenue - cogs, 2)
                    gross_margin = round((gross_profit / net_revenue) * 100, 2)
                    opex_logistics = round(net_revenue * random.uniform(0.08, 0.11), 2)
                    opex_storage = round(net_revenue * random.uniform(0.05, 0.07), 2)
                    opex_other = round(net_revenue * random.uniform(0.04, 0.06), 2)
                    spoilage_loss = round(net_revenue * random.uniform(0.008, 0.018), 2)
                    operating_profit = round(gross_profit - opex_logistics - opex_storage - opex_other, 2)
                    operating_margin = round((operating_profit / net_revenue) * 100, 2)
                    net_profit = round(operating_profit - spoilage_loss, 2)
                    net_margin = round((net_profit / net_revenue) * 100, 2)

                fin = MonthlyFinancial(
                    year=yr,
                    month=mo,
                    region_id=reg_obj.id,
                    gross_revenue_inr=gross_revenue,
                    net_revenue_inr=net_revenue,
                    cogs_inr=cogs,
                    gross_profit_inr=gross_profit,
                    gross_margin_pct=gross_margin,
                    opex_logistics_inr=opex_logistics,
                    opex_storage_inr=opex_storage,
                    opex_other_inr=opex_other,
                    operating_profit_inr=operating_profit,
                    operating_margin_pct=operating_margin,
                    spoilage_loss_inr=spoilage_loss,
                    net_profit_inr=net_profit,
                    net_margin_pct=net_margin
                )
                db.add(fin)
                
                # Also generate sample sales orders for this region & month to support order-level drilldown
                reg_customers = [c for c in customers if c.region_id == reg_obj.id]
                if reg_customers:
                    for _ in range(8):
                        order_id_counter += 1
                        order_dt = date(yr, mo, random.randint(1, 28))
                        cust = random.choice(reg_customers)
                        
                        so = SalesOrder(
                            order_number=f"ORD-{yr}-{order_id_counter}",
                            customer_id=cust.id,
                            region_id=reg_obj.id,
                            order_date=order_dt,
                            expected_delivery_date=order_dt + timedelta(days=2),
                            actual_delivery_date=order_dt + timedelta(days=2 + (random.randint(2, 4) if is_aug_2024_north else 0)),
                            status="Delayed" if is_aug_2024_north and random.random() < 0.6 else "Delivered",
                            total_revenue_inr=0.0,
                            total_cogs_inr=0.0,
                            total_discount_inr=0.0
                        )
                        db.add(so)
                        db.flush()
                        
                        tot_rev = 0.0
                        tot_cogs = 0.0
                        # Pick 2-4 products
                        sample_prods = random.sample(list(products.values()), random.randint(2, 4))
                        for prd in sample_prods:
                            # Check product margin squeeze scenario for Organic Paneer
                            unit_cost = prd.unit_cost_inr * (1.18 if (prd.sku == "PRD-DAIRY-01" and yr == 2024) else 1.0)
                            unit_price = prd.base_selling_price_inr * (0.80 if (prd.sku == "PRD-DAIRY-01" and yr == 2024) else 1.0)
                            qty = random.randint(80, 250) * (2 if (prd.sku == "PRD-DAIRY-01" and yr == 2024) else 1)
                            line_rev = round(qty * unit_price, 2)
                            line_c = round(qty * unit_cost, 2)
                            
                            soi = SalesOrderItem(
                                order_id=so.id,
                                product_id=prd.id,
                                quantity=qty,
                                unit_cost_inr=round(unit_cost, 2),
                                unit_price_inr=round(unit_price, 2),
                                discount_percent=20.0 if (prd.sku == "PRD-DAIRY-01" and yr == 2024) else 0.0,
                                line_total_inr=line_rev,
                                line_cogs_inr=line_c
                            )
                            db.add(soi)
                            tot_rev += line_rev
                            tot_cogs += line_c
                        
                        so.total_revenue_inr = round(tot_rev, 2)
                        so.total_cogs_inr = round(tot_cogs, 2)

    db.commit()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        seed_all_data(db, seed=42)
    finally:
        db.close()
