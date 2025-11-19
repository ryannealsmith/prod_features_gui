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

def extract_swimlane_from_label(label):
    """Extract swimlane from product feature, capability or technical function label.
    
    Examples:
        PF-ACT-1.1 -> Actors
        CA-ACT-1.1 -> Actors
        CA-LOC-4.1 -> Localisation
        TF-PRC-1.0 -> Perception
    """
    if not label:
        return None
    
    # Mapping of abbreviations to full swimlane names
    swimlane_map = {
        'ACT': 'Actors',
        'LOC': 'Localisation',
        'ENV': 'Environment',
        'MAP': 'Mapping',
        'INF': 'Infrastructure',
        'STA': 'Static',
        'CGO': 'Cargo',
        'VEH': 'Vehicle',
        'SV': 'Supervision',
        'FWD': 'Forward Driving',
        'REV': 'Reverse Driving',
        'NAV': 'Navigation',
        'MSN': 'Mission',
        'HMI': 'Human-Robot Interaction',
        'CE': 'CE',
        'PRK': 'Parking',
        'DCK': 'Docking',
        'CHE': 'Charging',
        'HCH': 'Hitching/Unhitching',
        'XMS': 'Crossmarket',
        'OPS': 'Operations',
        'PRC': 'Perception',
        'BAR': 'Barrier',
        'HRI': 'Human-Robot Interaction'
    }
    
    # Try to extract the code (e.g., 'ACT' from 'PF-ACT-1.1', 'CA-ACT-1.1' or 'PRC' from 'TF-PRC-1.0')
    parts = label.split('-')
    if len(parts) >= 2:
        code = parts[1]
        return swimlane_map.get(code, code)  # Return mapped name or the code itself
    
    return None

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
        
        # Skip duplicates
        if label in pf_label_to_id:
            print(f"  Skipping duplicate: {label}")
            continue
        
        # Get swimlane from Excel, or extract from label if missing
        swimlane = clean_text(row.get('Swimlanes'))
        if not swimlane:
            swimlane = extract_swimlane_from_label(label)
            
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
            'trl9_date': parse_date(row.get('TRL 9')),
            'swimlane': swimlane
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
        
        # Skip duplicates
        if label in cap_label_to_id:
            print(f"  Skipping duplicate: {label}")
            continue
        
        # Get swimlane from Excel, or extract from label if missing
        swimlane = clean_text(row.get('Swimlane'))
        if not swimlane:
            swimlane = extract_swimlane_from_label(label)
            
        cap_data = {
            'swimlane': swimlane,
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
        
        # Skip duplicates
        if label in tf_label_to_id:
            print(f"  Skipping duplicate: {label}")
            continue
        
        # Get swimlane from Excel, or extract from label if missing
        swimlane = clean_text(row.get('Swimlane'))
        if not swimlane:
            swimlane = extract_swimlane_from_label(label)
            
        tf_data = {
            'swimlane': swimlane,
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
    
    # Import Configurations
    print("\nImporting Configurations...")
    config_df = pd.read_excel(excel_file, sheet_name='Configurations')
    
    # Map Excel swimlane names to database config_type values
    type_map = {
        'Platform': 'Platform',
        'Operational Environment': 'ODD',
        'Environmental conditions': 'Environment',
        'Cargo': 'Trailer'
    }
    
    current_type = None
    config_count = 0
    
    for idx, row in config_df.iterrows():
        # Check if this row defines a new type (Swimlane column is not empty)
        swimlane = clean_text(row.get('Swimlane'))
        if swimlane:
            current_type = type_map.get(swimlane)
            if current_type:
                print(f"\n  Processing {current_type} configurations...")
        
        # Get the label (code) and description
        label = clean_text(row.get('Label'))
        description = clean_text(row.get('Configuration'))
        
        # Skip rows without label or description, or if no type is set
        if not label or not description or not current_type:
            continue
        
        config_data = {
            'config_type': current_type,
            'code': label,
            'description': description
        }
        
        try:
            db.add_configuration(config_data)
            config_count += 1
            print(f"    Added: {label} ({current_type})")
        except Exception as e:
            print(f"    Error adding {label}: {e}")
    
    print(f"\nImported {config_count} Configurations")
    
    db.close()
    print("\n✓ Data import completed successfully!")

if __name__ == '__main__':
    import_data()
