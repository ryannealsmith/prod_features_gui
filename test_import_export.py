#!/usr/bin/env python3
"""
Test script to verify JSON import/export functionality.
This script will:
1. Export the current database to engineering_plan_db.json
2. Display the export summary
3. Verify the file was created
"""
import os
import json
import database

def main():
    print("="*70)
    print("JSON IMPORT/EXPORT TEST")
    print("="*70)
    
    # Connect to database
    db = database.Database()
    db.connect()
    
    # Export data (simulate what export_to_json does)
    filepath = os.path.join(os.path.dirname(__file__), 'engineering_plan_db.json')
    
    print(f"\nExporting database to: {filepath}")
    
    try:
        # Gather all data from database
        export_data = {
            'export_date': '2025-11-20 12:00:00',
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
        pfs = db.get_product_features({})
        for pf in pfs:
            export_data['product_features'].append(pf)
        
        # Export Capabilities
        caps = db.get_capabilities({})
        for cap in caps:
            export_data['capabilities'].append(cap)
        
        # Export Technical Functions
        tfs = db.get_technical_functions({})
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
        
        # Write to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*70)
        print("EXPORT SUMMARY")
        print("="*70)
        print(f"Product Variants: {len(export_data['product_variants'])}")
        print(f"Product Features: {len(export_data['product_features'])}")
        print(f"Capabilities: {len(export_data['capabilities'])}")
        print(f"Technical Functions: {len(export_data['technical_functions'])}")
        print(f"Configurations: {len(export_data['configurations'])}")
        print(f"Milestones: {len(export_data['milestones'])}")
        print(f"PV-PF Links: {len(export_data['pv_product_features_relationships'])}")
        print(f"PF-Capability Links: {len(export_data['pf_capabilities_relationships'])}")
        print(f"Capability-TF Links: {len(export_data['cap_technical_functions_relationships'])}")
        
        # Verify file exists
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            print(f"\n✓ File created successfully")
            print(f"  Size: {file_size:,} bytes")
            print(f"  Location: {filepath}")
        else:
            print(f"\n✗ File not found at: {filepath}")
        
        print("\n" + "="*70)
        print("TEST COMPLETE")
        print("="*70)
        print("\nYou can now test 'Import JSON' from the File menu in the app.")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == '__main__':
    main()
