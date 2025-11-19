"""Populate swimlane field for existing technical functions based on label patterns."""
import database

# Mapping of label patterns to swimlanes
swimlane_mapping = {
    'PRC': 'Perception',
    'BAR': 'Reasoning',
}

db = database.Database()
db.connect()

# Get all technical functions
technical_functions = db.get_technical_functions()
updated_count = 0
skipped_count = 0

print(f"Processing {len(technical_functions)} technical functions...")

for tf in technical_functions:
    label = tf['label']
    current_swimlane = tf.get('swimlane')
    
    # Find matching pattern in label
    matched_swimlane = None
    for pattern, swimlane in swimlane_mapping.items():
        if pattern in label:
            matched_swimlane = swimlane
            break
    
    if matched_swimlane:
        # Update if different from current or force update for consistency
        if current_swimlane != matched_swimlane:
            tf['swimlane'] = matched_swimlane
            db.update_technical_function(tf['id'], tf)
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
print(f"Updated: {updated_count} technical functions")
print(f"Skipped: {skipped_count} technical functions")

db.close()
