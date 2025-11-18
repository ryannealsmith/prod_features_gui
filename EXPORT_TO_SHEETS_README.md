# Export to Google Sheets

This script (`export_to_sheets.py`) converts `product_features_roadmap_db.json` into a format that can be imported into Google Sheets.

## Features

- **Interactive component selection**: Choose which aspects to export:
  - Product Features
  - Capabilities
  - Technical Functions
  - Or all of the above

- **Maintains all linking relationships**: Automatically includes relevant relationship tables based on your selections:
  - Product Features ↔ Capabilities links (when both are selected)
  - Capabilities ↔ Technical Functions links (when both are selected)

- **Multiple export formats**:
  - **Excel (.xlsx)**: Single file with multiple sheets (RECOMMENDED for Google Sheets import)
  - **CSV files**: Multiple files (one per component/relationship)

## Usage

1. Ensure you have the required dependencies:
   ```bash
   pip install openpyxl
   ```

2. Run the script from the project directory:
   ```bash
   python export_to_sheets.py
   ```
   
   Or if using the virtual environment:
   ```bash
   .venv/bin/python export_to_sheets.py
   ```

3. Follow the interactive prompts:
   - Select which components to export (1-4)
   - Choose output format (Excel or CSV)

## Output

### Excel Format (Recommended)
Creates a single file: `roadmap_export.xlsx` with multiple sheets:
- **Export Metadata**: Information about the export
- **Product Features**: All product feature data (if selected)
- **Capabilities**: All capability data (if selected)
- **Technical Functions**: All technical function data (if selected)
- **PF-Capability Links**: Relationships between Product Features and Capabilities (if both selected)
- **Cap-TF Links**: Relationships between Capabilities and Technical Functions (if both selected)

### CSV Format
Creates a directory: `roadmap_export_csv/` with separate CSV files:
- `product_features.csv`
- `capabilities.csv`
- `technical_functions.csv`
- `pf_capability_links.csv`
- `cap_tf_links.csv`

## Importing to Google Sheets

### From Excel File (Recommended)
1. Go to https://sheets.google.com
2. Create a new spreadsheet or open an existing one
3. Click **File** → **Import** → **Upload**
4. Select `roadmap_export.xlsx`
5. Choose import location:
   - **Replace spreadsheet**: Replaces entire spreadsheet
   - **Insert new sheets**: Adds sheets to existing spreadsheet
6. Click **Import data**

All sheets will be imported with proper formatting and all relationships intact!

### From CSV Files
1. Go to https://sheets.google.com
2. Create a new spreadsheet
3. For each CSV file:
   - Click **File** → **Import** → **Upload**
   - Select the CSV file
   - Choose **Insert new sheet(s)**
   - Click **Import data**
4. Repeat for all CSV files

## Examples

### Export Everything (Excel)
```
Select components: 4
Output format: 1
```
Result: Single Excel file with all components and relationships

### Export Only Product Features and Capabilities (Excel)
```
Select components: 1,2
Output format: 1
```
Result: Excel file with Product Features, Capabilities, and PF-Capability links

### Export Only Technical Functions (CSV)
```
Select components: 3
Output format: 2
```
Result: Single CSV file with technical functions

## Data Integrity

- All original data is preserved
- Linking relationships are automatically filtered to match selected components
- Both IDs and labels are included in relationship tables for easy reference
- No data transformation or loss occurs during export

## Troubleshooting

**"File not found" error**:
- Ensure `product_features_roadmap_db.json` exists in the current directory
- Run the script from the project root directory

**Import issues in Google Sheets**:
- For large datasets, Excel format (.xlsx) is more reliable than CSV
- If sheets don't import correctly, try "Replace spreadsheet" instead of "Insert new sheets"

**Missing relationships**:
- Relationship tables only appear when BOTH related components are selected
- Example: PF-Capability links only appear if you select both Product Features AND Capabilities
