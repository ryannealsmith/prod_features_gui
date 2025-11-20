"""
Test script to verify Product Variant export functionality.
"""
import database
from datetime import datetime

db = database.Database()
db.connect()

# Get all product variants
pvs = db.get_product_variants()
print(f"Found {len(pvs)} product variants:\n")

for pv in pvs:
    print(f"  - {pv['label']}: {pv['title']}")
    print(f"    Target Date: {pv.get('due_date', 'Not set')}")
    print(f"    Platform: {pv.get('platform', 'Not set')}")
    print(f"    ODD: {pv.get('odd', 'Not set')}")
    print(f"    Environment: {pv.get('environment', 'Not set')}")
    
    # Get linked product features
    pfs = db.get_pv_product_features(pv['id'])
    print(f"    Linked Product Features: {len(pfs)}")
    
    # Get all capabilities from those product features
    all_caps = set()
    all_tfs = set()
    
    for pf in pfs:
        caps = db.get_pf_capabilities(pf['id'])
        for cap in caps:
            all_caps.add(cap['label'])
            
            # Get TFs for this cap
            tfs = db.get_cap_technical_functions(cap['id'])
            for tf in tfs:
                all_tfs.add(tf['label'])
    
    print(f"    Total Capabilities: {len(all_caps)}")
    print(f"    Total Technical Functions: {len(all_tfs)}")
    print()

print("\nExport functionality ready to test!")
print("1. Run the app")
print("2. Go to Product Variants tab")
print("3. Select a product variant")
print("4. Click 'Export to Markdown' button")
print("5. Choose save location")
print("6. Review the generated markdown file")

db.close()
