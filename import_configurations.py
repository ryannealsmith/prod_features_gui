"""Import configuration data from Excel file into the database."""
import pandas as pd
import database

# Load the Configurations sheet
excel_file = 'Product Engineering Canonical Product Features.xlsx'
df = pd.read_excel(excel_file, sheet_name='Configurations')

db = database.Database()
db.connect()

# Get existing configurations
existing_configs = db.get_configurations()
existing_codes = set((c['config_type'], c['code']) for c in existing_configs)

# Map Excel swimlanes to config types
type_mapping = {
    'Platform': 'Platform',
    'Operational Environment': 'ODD',
    'Environmental conditions': 'Environment',
    'Cargo': 'Trailer'
}

added_count = 0
skipped_count = 0
current_type = None

for idx, row in df.iterrows():
    # Check if this is a new section header
    swimlane = row['Swimlane']
    if pd.notna(swimlane) and swimlane in type_mapping:
        current_type = type_mapping[swimlane]
        print(f"\n=== Processing {swimlane} ({current_type}) ===")
        continue
    
    # Skip if we don't have a current type or if label is missing
    label = row['Label']
    if current_type is None or pd.isna(label):
        continue
    
    # Get configuration name and details
    config_name = row['Configuration']
    details = row['Details']
    
    # Build description
    if pd.notna(config_name) and pd.notna(details):
        description = f"{config_name} - {details}"
    elif pd.notna(config_name):
        description = config_name
    elif pd.notna(details):
        description = details
    else:
        description = label
    
    # Truncate very long descriptions
    if len(description) > 500:
        description = description[:497] + "..."
    
    # Check if already exists
    if (current_type, label) in existing_codes:
        print(f"  Skipped: {label} (already exists)")
        skipped_count += 1
        continue
    
    # Add to database
    try:
        db.add_configuration({
            'config_type': current_type,
            'code': label,
            'description': description
        })
        print(f"  Added: {label}")
        added_count += 1
    except Exception as e:
        print(f"  Error adding {label}: {e}")
        skipped_count += 1

print(f"\n=== Summary ===")
print(f"Added: {added_count} configurations")
print(f"Skipped: {skipped_count} configurations")

db.close()
