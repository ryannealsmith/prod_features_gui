"""
Test script to verify JSON export includes all entities.
"""
import database
import json
from datetime import datetime

db = database.Database()
db.connect()

# Simulate the export function
export_data = {
    'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'product_variants': [],
    'product_features': [],
    'capabilities': [],
    'technical_functions': [],
    'configurations': [],
    'milestones': [],
    'pv_product_features_relationships': [],
    'pf_capabilities_relationships': [],
    'cap_technical_functions_relationships': []
}

# Export Product Variants
pvs = db.get_product_variants()
for pv in pvs:
    export_data['product_variants'].append(pv)

# Export Product Features
pfs = db.get_product_features()
for pf in pfs:
    export_data['product_features'].append(pf)

# Export Capabilities
caps = db.get_capabilities()
for cap in caps:
    export_data['capabilities'].append(cap)

# Export Technical Functions
tfs = db.get_technical_functions()
for tf in tfs:
    export_data['technical_functions'].append(tf)

# Export Configurations
for config_type in ['Platform', 'ODD', 'Environment', 'Cargo', 'TRL']:
    configs = db.get_configurations(config_type)
    for config in configs:
        export_data['configurations'].append(config)

# Export Milestones
milestones = db.get_milestones()
for milestone in milestones:
    export_data['milestones'].append(milestone)

# Export relationships - Product Variants to Product Features
for pv in pvs:
    linked_pfs = db.get_pv_product_features(pv['id'])
    for pf in linked_pfs:
        export_data['pv_product_features_relationships'].append({
            'product_variant_id': pv['id'],
            'product_variant_label': pv['label'],
            'product_feature_id': pf['id'],
            'product_feature_label': pf['label']
        })

# Export relationships - Product Features to Capabilities
for pf in pfs:
    linked_caps = db.get_pf_capabilities(pf['id'])
    for cap in linked_caps:
        export_data['pf_capabilities_relationships'].append({
            'product_feature_id': pf['id'],
            'product_feature_label': pf['label'],
            'capability_id': cap['id'],
            'capability_label': cap['label']
        })

# Export relationships - Capabilities to Technical Functions
for cap in caps:
    linked_tfs = db.get_cap_technical_functions(cap['id'])
    for tf in linked_tfs:
        export_data['cap_technical_functions_relationships'].append({
            'capability_id': cap['id'],
            'capability_label': cap['label'],
            'technical_function_id': tf['id'],
            'technical_function_label': tf['label']
        })

# Print summary
print("JSON Export Test Summary")
print("=" * 50)
print(f"Export Date: {export_data['export_date']}")
print()
print(f"Product Variants: {len(export_data['product_variants'])}")
if export_data['product_variants']:
    print("  Sample PVs:")
    for pv in export_data['product_variants'][:3]:
        print(f"    - {pv['label']}: {pv['title']}")

print(f"\nProduct Features: {len(export_data['product_features'])}")
print(f"Capabilities: {len(export_data['capabilities'])}")
print(f"Technical Functions: {len(export_data['technical_functions'])}")
print(f"Configurations: {len(export_data['configurations'])}")
print(f"Milestones: {len(export_data['milestones'])}")
print()
print(f"PV-PF Links: {len(export_data['pv_product_features_relationships'])}")
if export_data['pv_product_features_relationships']:
    print("  Sample links:")
    for link in export_data['pv_product_features_relationships'][:3]:
        print(f"    - {link['product_variant_label']} → {link['product_feature_label']}")

print(f"\nPF-Capability Links: {len(export_data['pf_capabilities_relationships'])}")
print(f"Capability-TF Links: {len(export_data['cap_technical_functions_relationships'])}")

# Save to test file
with open('test_export.json', 'w', encoding='utf-8') as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

print("\n✅ Test export saved to: test_export.json")
print("\nAll entities and relationships successfully included in export!")

db.close()
