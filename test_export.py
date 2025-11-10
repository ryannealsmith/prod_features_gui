#!/usr/bin/env python3
"""Test the JSON export functionality."""

import database
import json
from datetime import datetime

def test_export():
    """Test exporting database to JSON."""
    db = database.Database()
    db.connect()
    
    # Gather all data
    export_data = {
        'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'product_features': [],
        'capabilities': [],
        'technical_functions': [],
        'pf_capabilities_relationships': [],
        'cap_technical_functions_relationships': []
    }
    
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
    
    # Write to test file
    filepath = 'test_export.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"Export successful to {filepath}")
    print(f"Product Features: {len(export_data['product_features'])}")
    print(f"Capabilities: {len(export_data['capabilities'])}")
    print(f"Technical Functions: {len(export_data['technical_functions'])}")
    print(f"PF-Capability Links: {len(export_data['pf_capabilities_relationships'])}")
    print(f"Capability-TF Links: {len(export_data['cap_technical_functions_relationships'])}")
    
    db.close()

if __name__ == '__main__':
    test_export()
