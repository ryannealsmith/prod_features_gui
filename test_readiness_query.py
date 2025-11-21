"""Test script to debug Readiness Matrix query."""
import database
from datetime import datetime

db = database.Database()
db.connect()

# Test with the filters you're selecting
print("Enter your filter values (press Enter to skip):")
platform = input("Platform (e.g., Terberg-1): ").strip() or None
odd = input("ODD (e.g., CFG-ODD-1): ").strip() or None
environment = input("Environment (e.g., CFG-ENV-2.1): ").strip() or None
trailer = input("Cargo: ").strip() or None
date_str = input("Query Date (YYYY-MM-DD): ").strip() or None

query_date = None
if date_str:
    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format")
        exit(1)

# Build filters
pf_filters = {}
if platform:
    pf_filters['platform'] = platform
if odd:
    pf_filters['odd'] = odd
if environment:
    pf_filters['environment'] = environment
if trailer:
    pf_filters['trailer'] = trailer

print(f"\nProduct Feature filters: {pf_filters}")

# Query product features
pfs = db.get_product_features(pf_filters)
print(f"\nFound {len(pfs)} product features")

if pfs:
    print("\nFirst 5 product features:")
    for i, pf in enumerate(pfs[:5]):
        print(f"{i+1}. {pf['label']}: {pf['name']}")
        print(f"   Platform: {pf.get('platform')}, ODD: {pf.get('odd')}, Env: {pf.get('environment')}, Cargo: {pf.get('trailer')}")
        print(f"   Details: {pf.get('details', '')[:80]}")
        
        # Calculate TRL achieved
        if query_date:
            trl3 = datetime.strptime(pf['trl3_date'], '%Y-%m-%d').date() if pf.get('trl3_date') else None
            trl6 = datetime.strptime(pf['trl6_date'], '%Y-%m-%d').date() if pf.get('trl6_date') else None
            trl9 = datetime.strptime(pf['trl9_date'], '%Y-%m-%d').date() if pf.get('trl9_date') else None
            
            if trl9 and query_date >= trl9:
                trl_achieved = 'TRL 9'
            elif trl6 and query_date >= trl6:
                trl_achieved = 'TRL 6'
            elif trl3 and query_date >= trl3:
                trl_achieved = 'TRL 3'
            else:
                trl_achieved = 'Not Started'
            print(f"   TRL Achieved: {trl_achieved}")
        print()
else:
    print("\nNo product features match these filters!")
    print("\nLet's check what values exist in the database:")
    print(f"Platforms: {db.get_unique_values('product_features', 'platform')}")
    print(f"ODDs: {db.get_unique_values('product_features', 'odd')}")
    print(f"Environments: {db.get_unique_values('product_features', 'environment')}")
    print(f"Cargo: {db.get_unique_values('product_features', 'trailer')}")

db.close()
