#!/usr/bin/env python3
"""
Test script to verify owner and URL fields work correctly
"""

import sys
from database import Database

def test_owner_url_fields():
    """Test adding and updating records with owner and URL fields."""
    db = Database('product_features.db')
    db.connect()  # Initialize database connection
    
    print("Testing Owner and URL Fields\n" + "="*50)
    
    # Test 1: Add a product variant with owner and URL
    print("\n1. Adding new Product Variant with owner and URL...")
    pv_data = {
        'label': 'TEST-PV-1',
        'title': 'Test Product Variant',
        'description': 'Testing owner/url fields',
        'platform': 'Highway',
        'trl': 'TRL3',
        'due_date': '2025-12-31',
        'owner': 'John Doe',
        'url': 'https://example.com/pv-test'
    }
    
    try:
        pv_id = db.add_product_variant(pv_data)
        print(f"   ✓ Created Product Variant with ID: {pv_id}")
        
        # Verify it was saved
        pv = db.get_product_variant_by_id(pv_id)
        print(f"   ✓ Owner: {pv.get('owner')}")
        print(f"   ✓ URL: {pv.get('url')}")
        
        # Update the owner
        update_data = {**pv_data, 'owner': 'Jane Smith', 'url': 'https://updated.com'}
        db.update_product_variant(pv_id, update_data)
        pv = db.get_product_variant_by_id(pv_id)
        print(f"   ✓ Updated Owner: {pv.get('owner')}")
        print(f"   ✓ Updated URL: {pv.get('url')}")
        
        # Clean up
        db.delete_product_variant(pv_id)
        print(f"   ✓ Cleaned up test data")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 2: Check unique owners function
    print("\n2. Testing get_unique_owners()...")
    try:
        owners = db.get_unique_owners()
        print(f"   ✓ Found {len(owners)} unique owners: {owners}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 3: Add product feature with owner/url
    print("\n3. Adding new Product Feature with owner and URL...")
    pf_data = {
        'label': 'TEST-PF-1',
        'name': 'Test Product Feature',
        'details': 'Testing owner/url fields',
        'owner': 'Alice Johnson',
        'url': 'https://example.com/pf-test'
    }
    
    try:
        pf_id = db.add_product_feature(pf_data)
        print(f"   ✓ Created Product Feature with ID: {pf_id}")
        
        pf = db.get_product_feature_by_id(pf_id)
        print(f"   ✓ Owner: {pf.get('owner')}")
        print(f"   ✓ URL: {pf.get('url')}")
        
        # Clean up
        db.delete_product_feature(pf_id)
        print(f"   ✓ Cleaned up test data")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 4: Add capability with owner/url
    print("\n4. Adding new Capability with owner and URL...")
    cap_data = {
        'label': 'TEST-CAP-1',
        'name': 'Test Capability',
        'details': 'Testing owner/url fields',
        'owner': 'Bob Williams',
        'url': 'https://example.com/cap-test'
    }
    
    try:
        cap_id = db.add_capability(cap_data)
        print(f"   ✓ Created Capability with ID: {cap_id}")
        
        cap = db.get_capability_by_id(cap_id)
        print(f"   ✓ Owner: {cap.get('owner')}")
        print(f"   ✓ URL: {cap.get('url')}")
        
        # Clean up
        db.delete_capability(cap_id)
        print(f"   ✓ Cleaned up test data")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 5: Add technical function with owner/url
    print("\n5. Adding new Technical Function with owner and URL...")
    tf_data = {
        'label': 'TEST-TF-1',
        'name': 'Test Technical Function',
        'details': 'Testing owner/url fields',
        'owner': 'Charlie Brown',
        'url': 'https://example.com/tf-test'
    }
    
    try:
        tf_id = db.add_technical_function(tf_data)
        print(f"   ✓ Created Technical Function with ID: {tf_id}")
        
        tf = db.get_technical_function_by_id(tf_id)
        print(f"   ✓ Owner: {tf.get('owner')}")
        print(f"   ✓ URL: {tf.get('url')}")
        
        # Clean up
        db.delete_technical_function(tf_id)
        print(f"   ✓ Cleaned up test data")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "="*50)
    print("All tests passed! ✓")
    return True

if __name__ == '__main__':
    success = test_owner_url_fields()
    sys.exit(0 if success else 1)
