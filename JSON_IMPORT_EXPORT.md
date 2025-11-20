# JSON Import/Export Feature

## Overview
The application now has full JSON import/export functionality for complete database backup and restoration.

## Features Added

### 1. Export to JSON (Updated)
- **Location**: File → Export to JSON
- **Functionality**: Automatically saves database to `engineering_plan_db.json` in the root directory
- **No user prompts**: File is saved directly without file dialog

### 2. Import JSON (NEW)
- **Location**: File → Import JSON
- **Functionality**: Imports data from `engineering_plan_db.json` in the root directory
- **Behavior**:
  - Updates existing records (matched by label)
  - Adds new records if label doesn't exist
  - Clears and re-imports all relationships
  - Shows confirmation dialog before importing
  - Displays detailed statistics after import

## Database Methods Added

Added to `database.py`:
- `get_product_variant_by_label(label)` - Find PV by label
- `get_product_feature_by_label(label)` - Find PF by label
- `get_capability_by_label(label)` - Find Capability by label
- `get_technical_function_by_label(label)` - Find TF by label

## What Gets Imported/Exported

### Entities (6 tables):
1. Product Variants
2. Product Features
3. Capabilities
4. Technical Functions
5. Configurations (all 5 types)
6. Milestones

### Relationships (3 junction tables):
1. Product Variant → Product Features links
2. Product Features → Capabilities links
3. Capabilities → Technical Functions links

## File Format

The `engineering_plan_db.json` file contains:
```json
{
  "export_date": "timestamp",
  "product_variants": [...],
  "product_features": [...],
  "capabilities": [...],
  "technical_functions": [...],
  "configurations": [...],
  "milestones": [...],
  "pv_product_features_relationships": [...],
  "pf_capabilities_relationships": [...],
  "cap_technical_functions_relationships": [...]
}
```

## Usage

### To Export (Backup):
1. Open the application
2. Click **File → Export to JSON**
3. File is automatically saved as `engineering_plan_db.json` in root directory

### To Import (Restore):
1. Ensure `engineering_plan_db.json` exists in root directory
2. Open the application
3. Click **File → Import JSON**
4. Confirm the import operation
5. All data will be restored/updated

## Test Scripts

Two test scripts are provided:

### `test_import_export.py`
Creates the `engineering_plan_db.json` export file for testing.

```bash
.venv/bin/python test_import_export.py
```

### `test_json_import.py`
Tests the import functionality by reading and importing the JSON file.

```bash
.venv/bin/python test_json_import.py
```

## Import Logic

- **Existing Records**: Updated based on matching label
- **New Records**: Added to database
- **Relationships**: Cleared and rebuilt from JSON
- **Timestamps**: Preserved from export
- **All Tabs**: Automatically refreshed after import

## Error Handling

- File not found: Shows error dialog with file path
- Invalid JSON: Shows parse error details
- Import errors: Shows detailed error message
- Relationship errors: Skips missing entities, continues processing

## Notes

- The JSON file is a complete backup of the database
- Import overwrites existing relationships
- Entity records are updated, not replaced
- IDs may differ between databases (matched by label)
- File location is always the root directory
