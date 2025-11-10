# Quick Start Guide

## Installation & Setup (macOS)

### Option 1: Using Homebrew (Recommended)

If you have Homebrew installed, this is the easiest way:

```bash
# Install Python with tkinter support
brew install python-tk@3.13

# Navigate to the project directory
cd /Users/ryan-smith/Documents/code/prod_features_gui

# Create virtual environment with Homebrew Python
/opt/homebrew/bin/python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Import data from Excel (first time only)
python import_data.py

# Run the application
python app.py
```

### Option 2: Using System Python

If tkinter works with your system Python:

```bash
# Navigate to the project directory
cd /Users/ryan-smith/Documents/code/prod_features_gui

# Try running directly
/usr/bin/python3 app.py
```

### Option 3: Using the Launch Script

```bash
cd /Users/ryan-smith/Documents/code/prod_features_gui
./run.sh
```

## First Time Setup

1. **Ensure Excel file exists**: Make sure `Product Engineering Canonical Product Features.xlsx` is in the project directory

2. **Import data** (if not already done):
   ```bash
   python import_data.py
   ```
   
   This creates `product_features.db` with all your data.

3. **Launch the app**:
   ```bash
   python app.py
   ```

## Quick Feature Tour

### 1. Product Features Tab
- **Browse**: See all 94 product features
- **Filter**: Click Platform dropdown to filter
- **Edit**: Click any feature to see details on the right
- **Capabilities**: See linked capabilities in the bottom section
- **Save**: Make changes and click "Save Changes"

### 2. Capabilities Tab
- Manage 90 capabilities
- Edit details, dates, and dependencies
- Similar interface to Product Features

### 3. Technical Functions Tab
- Manage 7 technical functions
- Link to capabilities

### 4. Readiness Matrix Tab
- **Filter Data**: Use dropdowns to filter by Platform, ODD, Environment, Swimlane
- **Apply Query**: Click to see filtered results
- **Two Views**: 
  - Product Features tab shows matching features
  - Capabilities tab shows matching capabilities
- **Export**: Save filtered results to CSV

### 5. Roadmap Tab
- **Visualize Timeline**: See when features/capabilities reach TRL milestones
- **Select View**: Choose Product Features, Capabilities, or Both
- **Update**: Click "Update Roadmap" after changing filters
- **Interactive**: Blue = Product Features, Green = Capabilities

## Common Tasks

### Add a New Product Feature
1. Go to "Product Features" tab
2. Click "Add New"
3. Enter Label (required) and Name (required)
4. Click "Save"

### Link Capability to Product Feature
1. Select a product feature
2. Scroll to "Capabilities" section
3. Click "Add Capability"
4. Select from the list
5. Click "Add"

### Query Readiness Matrix
1. Go to "Readiness Matrix" tab
2. Select filters (e.g., Platform: "Terberg-1")
3. Click "Apply Query"
4. View results in sub-tabs
5. Optionally click "Export Results" to save

### View Roadmap
1. Go to "Roadmap" tab
2. Select view type (Product Features/Capabilities/Both)
3. Click "Update Roadmap"
4. See timeline visualization with TRL dates

## Database Info

- **File**: `product_features.db`
- **Type**: SQLite
- **Tables**: 5 (3 main entities + 2 junction tables)
- **Records**: 
  - 94 Product Features
  - 90 Capabilities
  - 7 Technical Functions
  - Plus relationship mappings

## Troubleshooting

### "No module named '_tkinter'"
You need Python with tkinter. Try:
```bash
brew install python-tk@3.13
```

### "Database is locked"
Close all instances of the app and try again.

### "Excel file not found"
Make sure `Product Engineering Canonical Product Features.xlsx` is in the project folder.

### App won't start
Check that you've imported data:
```bash
python import_data.py
```

## Data Safety

- All changes are saved to `product_features.db`
- Original Excel file is never modified
- To reset: Delete `product_features.db` and run `import_data.py` again

## Need Help?

See the full `README.md` for comprehensive documentation.
