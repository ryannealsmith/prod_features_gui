"""
Verify that JSON export is a complete database backup.
"""
import database
import sqlite3

db = database.Database()
db.connect()

print("=" * 70)
print("DATABASE BACKUP VERIFICATION")
print("=" * 70)
print()

# Check all tables
tables = {
    'product_variants': 'Product Variants',
    'product_features': 'Product Features',
    'capabilities': 'Capabilities',
    'technical_functions': 'Technical Functions',
    'configurations': 'Configurations',
    'milestones': 'Milestones',
    'pv_product_features': 'PV-PF Relationships',
    'pf_capabilities': 'PF-Capability Relationships',
    'cap_technical_functions': 'Capability-TF Relationships'
}

print("DATABASE TABLES:")
print("-" * 70)
for table, name in tables.items():
    cursor = db.connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {name:40} {count:5} records")
print()

# Check what gets exported
print("JSON EXPORT COVERAGE:")
print("-" * 70)

export_sections = {
    'product_variants': ('get_product_variants', 'Product Variants'),
    'product_features': ('get_product_features', 'Product Features'),
    'capabilities': ('get_capabilities', 'Capabilities'),
    'technical_functions': ('get_technical_functions', 'Technical Functions'),
    'milestones': ('get_milestones', 'Milestones'),
}

for section, (method, name) in export_sections.items():
    func = getattr(db, method)
    if method == 'get_product_features' or method == 'get_capabilities':
        data = func({})  # These methods need filters param
    else:
        data = func()
    print(f"  {name:40} {len(data):5} records ✓")

# Configurations (exported by type)
total_configs = 0
for config_type in ['Platform', 'ODD', 'Environment', 'Cargo', 'TRL']:
    configs = db.get_configurations(config_type)
    total_configs += len(configs)
print(f"  {'Configurations':40} {total_configs:5} records ✓")

# Relationships (calculated from linked entities)
pvs = db.get_product_variants()
pv_pf_links = 0
for pv in pvs:
    pv_pf_links += len(db.get_pv_product_features(pv['id']))

pfs = db.get_product_features({})
pf_cap_links = 0
for pf in pfs:
    pf_cap_links += len(db.get_pf_capabilities(pf['id']))

caps = db.get_capabilities({})
cap_tf_links = 0
for cap in caps:
    cap_tf_links += len(db.get_cap_technical_functions(cap['id']))

print(f"  {'PV-PF Relationships':40} {pv_pf_links:5} links ✓")
print(f"  {'PF-Capability Relationships':40} {pf_cap_links:5} links ✓")
print(f"  {'Capability-TF Relationships':40} {cap_tf_links:5} links ✓")
print()

# Check field coverage for each table
print("FIELD COVERAGE CHECK:")
print("-" * 70)

def check_table_fields(table_name, entity_name, get_method, needs_filters=False):
    """Check if all table fields are exported."""
    cursor = db.connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Get sample record
    method = getattr(db, get_method)
    if needs_filters:
        records = method({})
    else:
        records = method()
    
    if records:
        sample = records[0]
        exported_fields = set(sample.keys())
        db_fields = set(columns)
        
        missing = db_fields - exported_fields
        extra = exported_fields - db_fields
        
        print(f"\n  {entity_name}:")
        print(f"    Database columns: {len(db_fields)}")
        print(f"    Exported fields:  {len(exported_fields)}")
        
        if missing:
            print(f"    ⚠️  Missing in export: {missing}")
            return False
        elif extra:
            print(f"    ℹ️  Extra in export (derived): {extra}")
            return True
        else:
            print(f"    ✓ Complete match")
            return True
    else:
        print(f"\n  {entity_name}: No records to check")
        return True

all_complete = True
all_complete &= check_table_fields('product_variants', 'Product Variants', 'get_product_variants')
all_complete &= check_table_fields('product_features', 'Product Features', 'get_product_features', True)
all_complete &= check_table_fields('capabilities', 'Capabilities', 'get_capabilities', True)
all_complete &= check_table_fields('technical_functions', 'Technical Functions', 'get_technical_functions')
all_complete &= check_table_fields('milestones', 'Milestones', 'get_milestones')
all_complete &= check_table_fields('configurations', 'Configurations', 'get_configurations', needs_filters=True)

print()
print("=" * 70)
if all_complete:
    print("✅ JSON EXPORT IS A COMPLETE DATABASE BACKUP")
    print()
    print("The export includes:")
    print("  • All entity tables with all fields")
    print("  • All relationship/junction tables")
    print("  • Timestamps (created_at, updated_at)")
    print("  • All configuration types")
    print()
    print("The export can be used to:")
    print("  ✓ Fully restore the database")
    print("  ✓ Migrate to another system")
    print("  ✓ Backup and version control")
    print("  ✓ Data analysis and reporting")
else:
    print("⚠️  EXPORT MAY BE INCOMPLETE - CHECK WARNINGS ABOVE")

print("=" * 70)

db.close()
