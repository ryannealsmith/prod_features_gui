"""Populate swimlane field for existing product features based on label patterns."""
import database

# Mapping of label patterns to swimlanes
swimlane_mapping = {
    'ACT': 'Actors',
    'INF': 'Infrastructure',
    'ENV': 'Environment',
    'CGO': 'Cargo',
    'SV': 'Supervision',
    'FWD': 'Forward Driving',
    'PRK': 'Parking',
    'DCK': 'Docking',
    'CHE': 'CHE Interactions',
    'HCH': 'Hitching/Unhitching',
    'CE': 'CE Marking',
    'XMS': 'Fleet Management',
    'OPS': 'Operations',
    'REV': 'Reversing',
    'HRI': 'Human-Robot Interaction',
}

db = database.Database()
db.connect()

# Get all product features
features = db.get_product_features()
updated_count = 0
skipped_count = 0

print(f"Processing {len(features)} product features...")

for feature in features:
    label = feature['label']
    current_swimlane = feature.get('swimlane')
    
    # Find matching pattern in label
    matched_swimlane = None
    for pattern, swimlane in swimlane_mapping.items():
        if pattern in label:
            matched_swimlane = swimlane
            break
    
    if matched_swimlane:
        # Update if different from current or force update for consistency
        if current_swimlane != matched_swimlane:
            feature['swimlane'] = matched_swimlane
            db.update_product_feature(feature['id'], feature)
            print(f"  Updated: {label} ('{current_swimlane}' -> '{matched_swimlane}')")
            updated_count += 1
        else:
            print(f"  Skipped: {label} (already correct: {current_swimlane})")
            skipped_count += 1
    else:
        if current_swimlane:
            print(f"  No match: {label} (keeping current: {current_swimlane})")
        else:
            print(f"  No match: {label}")
        skipped_count += 1

print(f"\n=== Summary ===")
print(f"Updated: {updated_count} product features")
print(f"Skipped: {skipped_count} product features")

db.close()
