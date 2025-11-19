"""Populate swimlane field for existing capabilities based on label patterns."""
import database

# Mapping of label patterns to swimlanes
swimlane_mapping = {
    'LPP': 'Loops - Perception',
    'LPR': 'Loops - Reasoning',
    'ENV': 'Environment',
    'MLO': 'ML Ops',
    'LOC': 'Localisation',
    'MAP': 'Mapping',
    'INF': 'Infrastructure (Ghost Town)',
    'STA': 'Static Objects',
    'CGO': 'Cargo',
    'VEH': 'Vehicle',
    'SV': 'Supervision',
    'FWD': 'Forward Driving/Towing',
    'REV': 'Reversing',
    'NAV': 'Navigation',
    'MSN': 'Mission Execution',
    'HMI': 'HMI',
    'CE': 'CE Marking',
}

db = database.Database()
db.connect()

# Get all capabilities
capabilities = db.get_capabilities()
updated_count = 0
skipped_count = 0

print(f"Processing {len(capabilities)} capabilities...")

for capability in capabilities:
    label = capability['label']
    current_swimlane = capability.get('swimlane')
    
    # Find matching pattern in label
    matched_swimlane = None
    for pattern, swimlane in swimlane_mapping.items():
        if pattern in label:
            matched_swimlane = swimlane
            break
    
    if matched_swimlane:
        # Update if different from current or force update for consistency
        if current_swimlane != matched_swimlane:
            capability['swimlane'] = matched_swimlane
            db.update_capability(capability['id'], capability)
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
print(f"Updated: {updated_count} capabilities")
print(f"Skipped: {skipped_count} capabilities")

db.close()
