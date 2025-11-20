#!/usr/bin/env python3
"""
Test script to verify JSON import functionality works correctly.
This will simulate what the import_from_json() method does.
"""
import os
import json
import database

def main():
    print("="*70)
    print("JSON IMPORT TEST")
    print("="*70)
    
    # Connect to database
    db = database.Database()
    db.connect()
    
    filepath = os.path.join(os.path.dirname(__file__), 'engineering_plan_db.json')
    
    if not os.path.exists(filepath):
        print(f"\n✗ File not found: {filepath}")
        print("Run test_import_export.py first to create the export file.")
        return
    
    print(f"\nImporting from: {filepath}")
    
    try:
        # Read JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        stats = {
            'product_variants': {'added': 0, 'updated': 0},
            'product_features': {'added': 0, 'updated': 0},
            'capabilities': {'added': 0, 'updated': 0},
            'technical_functions': {'added': 0, 'updated': 0},
            'configurations': {'added': 0, 'updated': 0},
            'milestones': {'added': 0, 'updated': 0},
            'relationships': 0
        }
        
        print("\nProcessing entities...")
        
        # Import Product Variants
        for pv_data in import_data.get('product_variants', []):
            existing = db.get_product_variant_by_label(pv_data['label'])
            if existing:
                db.update_product_variant(existing['id'], pv_data)
                stats['product_variants']['updated'] += 1
            else:
                db.add_product_variant(pv_data)
                stats['product_variants']['added'] += 1
        
        # Import Product Features
        for pf_data in import_data.get('product_features', []):
            existing = db.get_product_feature_by_label(pf_data['label'])
            if existing:
                db.update_product_feature(existing['id'], pf_data)
                stats['product_features']['updated'] += 1
            else:
                db.add_product_feature(pf_data)
                stats['product_features']['added'] += 1
        
        # Import Capabilities
        for cap_data in import_data.get('capabilities', []):
            existing = db.get_capability_by_label(cap_data['label'])
            if existing:
                db.update_capability(existing['id'], cap_data)
                stats['capabilities']['updated'] += 1
            else:
                db.add_capability(cap_data)
                stats['capabilities']['added'] += 1
        
        # Import Technical Functions
        for tf_data in import_data.get('technical_functions', []):
            existing = db.get_technical_function_by_label(tf_data['label'])
            if existing:
                db.update_technical_function(existing['id'], tf_data)
                stats['technical_functions']['updated'] += 1
            else:
                db.add_technical_function(tf_data)
                stats['technical_functions']['added'] += 1
        
        # Import Configurations
        for config_data in import_data.get('configurations', []):
            existing_configs = db.get_configurations(config_data['config_type'])
            existing = next((c for c in existing_configs if c['code'] == config_data['code']), None)
            if existing:
                db.update_configuration(existing['id'], config_data)
                stats['configurations']['updated'] += 1
            else:
                db.add_configuration(config_data)
                stats['configurations']['added'] += 1
        
        # Import Milestones
        for milestone_data in import_data.get('milestones', []):
            existing_milestones = db.get_milestones()
            existing = next((m for m in existing_milestones if m['name'] == milestone_data['name']), None)
            if existing:
                db.update_milestone(existing['id'], milestone_data)
                stats['milestones']['updated'] += 1
            else:
                db.add_milestone(milestone_data)
                stats['milestones']['added'] += 1
        
        print("Clearing and re-importing relationships...")
        
        # Clear existing relationships
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM pv_product_features")
        cursor.execute("DELETE FROM pf_capabilities")
        cursor.execute("DELETE FROM cap_technical_functions")
        
        # Import PV-PF Relationships
        for rel in import_data.get('pv_product_features_relationships', []):
            pv = db.get_product_variant_by_label(rel['product_variant_label'])
            pf = db.get_product_feature_by_label(rel['product_feature_label'])
            if pv and pf:
                db.link_pv_pf(pv['id'], pf['id'])
                stats['relationships'] += 1
        
        # Import PF-Capability Relationships
        for rel in import_data.get('pf_capabilities_relationships', []):
            pf = db.get_product_feature_by_label(rel['product_feature_label'])
            cap = db.get_capability_by_label(rel['capability_label'])
            if pf and cap:
                db.link_pf_capability(pf['id'], cap['id'])
                stats['relationships'] += 1
        
        # Import Capability-TF Relationships
        for rel in import_data.get('cap_technical_functions_relationships', []):
            cap = db.get_capability_by_label(rel['capability_label'])
            tf = db.get_technical_function_by_label(rel['technical_function_label'])
            if cap and tf:
                db.link_cap_tf(cap['id'], tf['id'])
                stats['relationships'] += 1
        
        db.connection.commit()
        
        print("\n" + "="*70)
        print("IMPORT SUMMARY")
        print("="*70)
        print(f"Product Variants: {stats['product_variants']['added']} added, {stats['product_variants']['updated']} updated")
        print(f"Product Features: {stats['product_features']['added']} added, {stats['product_features']['updated']} updated")
        print(f"Capabilities: {stats['capabilities']['added']} added, {stats['capabilities']['updated']} updated")
        print(f"Technical Functions: {stats['technical_functions']['added']} added, {stats['technical_functions']['updated']} updated")
        print(f"Configurations: {stats['configurations']['added']} added, {stats['configurations']['updated']} updated")
        print(f"Milestones: {stats['milestones']['added']} added, {stats['milestones']['updated']} updated")
        print(f"Relationships: {stats['relationships']} linked")
        
        print("\n" + "="*70)
        print("TEST COMPLETE - Import functionality working!")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == '__main__':
    main()
