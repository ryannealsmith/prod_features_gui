"""
Import data from Excel spreadsheet into the database.
"""
import pandas as pd
import numpy as np
from database import Database
from datetime import datetime

def parse_date(date_val):
    """Parse various date formats from Excel."""
    if pd.isna(date_val) or date_val == '' or date_val is None:
        return None
    
    # If it's already a datetime
    if isinstance(date_val, datetime):
        return date_val.strftime('%Y-%m-%d')
    
    # If it's a string, try to parse it
    if isinstance(date_val, str):
        # Try common formats
        formats = ['%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y']
        for fmt in formats:
            try:
                dt = datetime.strptime(date_val, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
    
    return None

def clean_text(text):
    """Clean text fields from Excel."""
    if pd.isna(text) or text == '':
        return None
    return str(text).strip()

def import_data():
    """Import all data from Excel to database."""
    db = Database()
    db.connect()
    db.create_tables()
    
    excel_file = 'Product Engineering Canonical Product Features.xlsx'
    
    print("Importing Product Features...")
    pf_df = pd.read_excel(excel_file, sheet_name='Product Features')
    
    pf_label_to_id = {}
    for idx, row in pf_df.iterrows():
        label = clean_text(row.get('Label'))
        if not label or label == 'nan':
            continue
            
        pf_data = {
            'label': label,
            'name': clean_text(row.get('Product Feature')) or label,
            'platform': clean_text(row.get('Platform')),
            'odd': clean_text(row.get('ODD')),
            'environment': clean_text(row.get('Environment')),
            'trailer': clean_text(row.get('Trailer')),
            'details': clean_text(row.get('Details')),
            'comments': clean_text(row.get('Comments')),
            'when_date': clean_text(row.get('When')),
            'start_date': parse_date(row.get('Start Date')),
            'trl3_date': parse_date(row.get('TRL 3')),
            'trl6_date': parse_date(row.get('TRL 6')),
            'trl9_date': parse_date(row.get('TRL 9'))
        }
        
        try:
            pf_id = db.add_product_feature(pf_data)
            pf_label_to_id[label] = pf_id
            print(f"  Added: {label}")
        except Exception as e:
            print(f"  Error adding {label}: {e}")
    
    print(f"\nImported {len(pf_label_to_id)} Product Features")
    
    print("\nImporting Capabilities...")
    cap_df = pd.read_excel(excel_file, sheet_name='Capabilities')
    
    cap_label_to_id = {}
    for idx, row in cap_df.iterrows():
        label = clean_text(row.get('Label'))
        if not label or label == 'nan':
            continue
            
        cap_data = {
            'swimlane': clean_text(row.get('Swimlane')),
            'sl': clean_text(row.get('SL')),
            'maj': row.get('Maj') if not pd.isna(row.get('Maj')) else None,
            'min': row.get('Min') if not pd.isna(row.get('Min')) else None,
            'label': label,
            'name': clean_text(row.get('Capability')) or label,
            'platform': clean_text(row.get('Platform')),
            'odd': clean_text(row.get('ODD')),
            'environment': clean_text(row.get('Environment')),
            'trailer': clean_text(row.get('Trailer')),
            'details': clean_text(row.get('Details/ comments')),
            'when_date': clean_text(row.get('When')),
            'dependencies': clean_text(row.get('Dependencies')),
            'dependents': clean_text(row.get('Dependents')),
            'start_date': parse_date(row.get('Start date')),
            'trl3_date': parse_date(row.get('TRL3')),
            'trl6_date': parse_date(row.get('TRL6')),
            'trl9_date': parse_date(row.get('TRL9'))
        }
        
        try:
            cap_id = db.add_capability(cap_data)
            cap_label_to_id[label] = cap_id
            print(f"  Added: {label}")
        except Exception as e:
            print(f"  Error adding {label}: {e}")
    
    print(f"\nImported {len(cap_label_to_id)} Capabilities")
    
    print("\nImporting Technical Functions...")
    tf_df = pd.read_excel(excel_file, sheet_name='Technical Functions (WIP)')
    
    tf_label_to_id = {}
    for idx, row in tf_df.iterrows():
        label = clean_text(row.get('Label'))
        if not label or label == 'nan':
            continue
            
        tf_data = {
            'swimlane': clean_text(row.get('Swimlane')),
            'sl': clean_text(row.get('SL')),
            'maj': row.get('Maj') if not pd.isna(row.get('Maj')) else None,
            'min': row.get('Min') if not pd.isna(row.get('Min')) else None,
            'label': label,
            'name': clean_text(row.get('Technical Function')) or label,
            'platform': clean_text(row.get('Platform')),
            'odd': clean_text(row.get('ODD')),
            'environment': clean_text(row.get('Environment')),
            'trailer': clean_text(row.get('Trailer')),
            'details': clean_text(row.get('Details/ comments')),
            'next': clean_text(row.get('Next'))
        }
        
        try:
            tf_id = db.add_technical_function(tf_data)
            tf_label_to_id[label] = tf_id
            print(f"  Added: {label}")
        except Exception as e:
            print(f"  Error adding {label}: {e}")
    
    print(f"\nImported {len(tf_label_to_id)} Technical Functions")
    
    # Link Product Features to Capabilities
    print("\nLinking Product Features to Capabilities...")
    for idx, row in pf_df.iterrows():
        pf_label = clean_text(row.get('Label'))
        if pf_label not in pf_label_to_id:
            continue
            
        pf_id = pf_label_to_id[pf_label]
        capabilities_str = clean_text(row.get('Capabilities'))
        
        if capabilities_str:
            # Split by newlines or commas
            cap_labels = capabilities_str.replace('\n', ',').split(',')
            for cap_label in cap_labels:
                cap_label = cap_label.strip()
                if cap_label and cap_label in cap_label_to_id:
                    db.link_pf_capability(pf_id, cap_label_to_id[cap_label])
                    print(f"  Linked {pf_label} -> {cap_label}")
    
    # Link Capabilities to Technical Functions
    print("\nLinking Capabilities to Technical Functions...")
    for idx, row in tf_df.iterrows():
        tf_label = clean_text(row.get('Label'))
        if tf_label not in tf_label_to_id:
            continue
            
        tf_id = tf_label_to_id[tf_label]
        capabilities_str = clean_text(row.get('Capability'))
        
        if capabilities_str:
            # Split by newlines or commas
            cap_labels = capabilities_str.replace('\n', ',').split(',')
            for cap_label in cap_labels:
                cap_label = cap_label.strip()
                if cap_label and cap_label in cap_label_to_id:
                    db.link_cap_tf(cap_label_to_id[cap_label], tf_id)
                    print(f"  Linked {cap_label} -> {tf_label}")
    
    db.close()
    print("\n✓ Data import completed successfully!")

if __name__ == '__main__':
    import_data()
