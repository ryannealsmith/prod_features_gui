# Quick Start Guide

## Installation & Setup (macOS)

### Recommended Setup

```bash
# Install Python with tkinter support (if needed)
brew install python-tk@3.13

# Navigate to project directory
cd /Users/ryan-smith/Documents/code/prod_features_gui

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Import data from Excel (first time only)
python import_data.py

# Run the application
python app.py
```

## First Time Setup

1. **Ensure Excel file exists**: `Product Engineering Canonical Product Features.xlsx`
2. **Import data**: `python import_data.py` (creates `product_features.db`)
3. **Launch app**: `python app.py`

## Quick Feature Tour

### 1. Product Variants Tab ⭐ NEW
- Manage product configurations (Port Baseline, Jebel Ali, etc.)
- Set platform, ODD, environment, trailer
- Define target dates
- Link product features to variants
- **Use Case**: Select in Readiness Matrix or Roadmap to auto-fill filters

### 2. Product Features Tab
- Browse 77 product features
- Filter by platform, ODD, environment, trailer
- Edit TRL dates (TRL3, TRL6, TRL9)
- Link capabilities to features
- Organize by swimlane

### 3. Capabilities Tab
- Manage 116 capabilities
- Link to technical functions and product features
- Track dependencies
- Edit dates and details

### 4. Technical Functions Tab
- Manage 7 technical functions
- Link to capabilities
- Organize by perception/reasoning

### 5. Configurations Tab ⭐ NEW
- Centralized configuration management
- Add/edit Platforms, ODDs, Environments, Trailers, TRLs
- Used throughout system for filtering

### 6. Readiness Matrix Tab
- **Product Variant Filter**: Select PV to auto-fill all filters ⭐ NEW
- Filter by Platform, ODD, Environment, Trailer
- **Query Modes**:
  - By Date: What TRL level by this date?
  - By TRL: When will this TRL be achieved?
- View results in Product Features and Capabilities tabs
- **TRL Distribution Chart**: Pie chart showing breakdown ⭐ NEW
- Calendar picker for date selection
- Export to JSON

### 7. Roadmap Tab
- **Product Variant Filter**: Auto-fill filters ⭐ NEW
- Gantt-style timeline with TRL milestones
- Product variant target dates shown as vertical lines ⭐ NEW
- **Manage Milestones**: Add custom milestones ⭐ NEW
- Swimlane organization
- Export capabilities

### 8. Interactive Roadmap Tab ⭐ NEW
- Plotly-based interactive visualization
- Hover for details
- Zoom and pan
- Filter by platform, ODD, environment, trailer
- Product variant milestones with diamond markers

## Common Tasks

### Add a Product Variant ⭐ NEW
1. Go to "Product Variants" tab
2. Click "Add New"
3. Enter Label (e.g., PV-4) and Title
4. Click 📅 to select Target Date
5. Select configurations
6. Click "Save"

### Export Product Variant to Markdown ⭐ NEW
1. Go to "Product Variants" tab
2. Select a Product Variant from the list
3. Click "Export to Markdown" button
4. Choose save location and filename
5. Review generated markdown with:
   - Complete configuration details
   - All linked Product Features
   - All dependent Capabilities and Technical Functions
   - TRL dates and cross-dependencies
   - Roadmap snapshot image
6. See **EXPORT_GUIDE.md** for detailed documentation

### Query by Product Variant ⭐ NEW
1. Go to "Readiness Matrix" or "Roadmap" tab
2. Select Product Variant from dropdown
3. Configuration filters auto-populate
4. Click "Apply Query" or "Update Roadmap"

### Add a Product Feature
1. Go to "Product Features" tab
2. Click "Add New"
3. Enter Label and Name (required)
4. Fill in other fields
5. Click "Save"

### Link Capability to Product Feature
1. Select a product feature
2. Scroll to "Capabilities" section
3. Click "Add Capability"
4. Select from list
5. Click "Add"

### Query Readiness by Date
1. Go to "Readiness Matrix" tab
2. Select "By Date" query mode
3. Click 📅 to pick date (or type YYYY-MM-DD)
4. Select filters (Platform, ODD, etc.)
5. Click "Apply Query"
6. View TRL status in results tabs
7. See TRL Distribution pie chart

### View Roadmap
1. Go to "Roadmap" tab
2. Optionally select Product Variant to filter
3. Select view (Product Features/Capabilities)
4. Click "Update Roadmap"
5. See timeline with TRL progression and milestones

### Standardize Swimlanes
```bash
# Fix inconsistent swimlane names
python populate_swimlanes.py           # Product Features
python populate_capability_swimlanes.py # Capabilities  
python populate_tf_swimlanes.py        # Technical Functions
```

## Database Info

- **File**: `product_features.db`
- **Type**: SQLite
- **Current Data**: 
  - 77 Product Features
  - 116 Capabilities
  - 7 Technical Functions
  - 3 Product Variants ⭐ NEW
  - 26 Configurations ⭐ NEW
  - 102 PF-Capability links
  - 2 Capability-TF links

## Troubleshooting

### "No module named '_tkinter'"
```bash
brew install python-tk@3.13
```

### "Database is locked"
Close all app instances and try again.

### Reset Database
```bash
rm product_features.db
python import_data.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

## What's New (November 2025)

⭐ **Product Variant Markdown Export** - Comprehensive documentation generation with dependencies, TRL dates, cross-references, and roadmap snapshot
⭐ **Product Variants** - Manage product configurations
⭐ **Auto-fill Filters** - Select PV to populate all filters
⭐ **Configurations Management** - Centralized config options
⭐ **Interactive Roadmap** - Plotly visualization
⭐ **Milestone Management** - Custom milestones on roadmaps
⭐ **TRL Distribution Charts** - Visual readiness breakdown
⭐ **Dual Query Modes** - By date or by TRL level
⭐ **Calendar Pickers** - Easy date selection
⭐ **Swimlane Standardization** - 70 items corrected
⭐ **Enhanced Linking** - PFs to Capabilities and PVs

## Need Help?

- **Full Documentation**: See `README.md`
- **Project Overview**: See `PROJECT_SUMMARY.md`
- **Visual Guide**: See `VISUAL_OVERVIEW.md`
- **Code Comments**: Check `app.py` and `database.py`
