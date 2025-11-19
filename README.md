# Product Features Management System

A comprehensive GUI application for managing Product Features, Capabilities, Technical Functions, Product Variants, and Configurations with many-to-many relationships, readiness matrix queries, and roadmap visualization.

## Features

### 1. **Database Management**
- SQLite relational database with proper schema
- Many-to-many relationships between:
  - Product Features ↔ Capabilities
  - Capabilities ↔ Technical Functions
  - Product Variants ↔ Product Features
- Full CRUD operations for all entities
- **Current Data**: 77 Product Features, 116 Capabilities, 7 Technical Functions, 3 Product Variants, 26 Configurations

### 2. **Product Variants Management** ⭐ NEW
- Define product variant configurations (e.g., "Port Baseline", "Jebel Ali")
- Specify platform, ODD, environment, and trailer configurations
- Set target dates for product variants
- Link product features to product variants
- Integrated with Readiness Matrix and Roadmap filtering

### 3. **Product Features Management**
- View, add, edit, and delete product features
- Track TRL (Technology Readiness Level) dates: TRL3, TRL6, TRL9
- Filter by platform, ODD, environment, trailer
- Link/unlink capabilities to product features
- Link to product variants
- Organize by swimlane categories

### 4. **Capabilities Management**
- Manage capabilities with swimlane organization
- Track dates and dependencies
- Link to technical functions and product features
- Filter and search capabilities
- Organize by functional areas

### 5. **Technical Functions Management**
- Create and manage technical functions
- Organize by swimlane
- Link to capabilities
- Track perception and reasoning functions

### 6. **Configurations Management** ⭐ NEW
- Centralized management of configuration options:
  - **Platforms**: Vehicle platforms (Terberg-1.2, Terberg-1.3, etc.)
  - **ODDs**: Operational Design Domains
  - **Environments**: Deployment environments (CFG-ENV-1.1, CFG-ENV-2.1, etc.)
  - **Trailers**: Trailer types and configurations
  - **TRLs**: Technology Readiness Level definitions
- Add, edit, and delete configuration values
- Used throughout the system for filtering and categorization

### 7. **Readiness Matrix Query Interface**
- **Product Variant Filter**: Select a product variant to auto-populate all configuration filters ⭐ NEW
- Filter data by multiple criteria:
  - Product Variant (auto-fills platform, ODD, environment, trailer)
  - Platform, ODD, Environment, Trailer
- **Query Modes**:
  - **By Date**: Query what TRL level is achieved by a specific date
  - **By TRL Level**: Query when a specific TRL level will be achieved
- View filtered results in organized tabs with TRL status
- **TRL Distribution Chart**: Visual pie chart showing TRL breakdown ⭐ NEW
- Export results to JSON format
- Color-coded indicators and calendar picker

### 8. **Roadmap Visualization**
- **Product Variant Filter**: Auto-populate filters ⭐ NEW
- Timeline view with Gantt-style representation based on TRL dates
- Swimlane organization
- Product variant milestones as vertical lines ⭐ NEW
- **Milestone Management**: Add custom milestones ⭐ NEW
- Interactive matplotlib charts

### 9. **Interactive Roadmap** ⭐ NEW
- Dynamic Plotly-based interactive visualization
- Filter by platform, ODD, environment, trailer
- Hover tooltips with detailed information
- Zoom, pan, and export functionality

## Installation

See QUICKSTART.md for detailed setup instructions.

### Quick Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Import data
python import_data.py

# Run application
python app.py
```

## Database Schema

- **product_features** (77 records)
- **capabilities** (116 records)
- **technical_functions** (7 records)
- **product_variants** (3 records) ⭐ NEW
- **configurations** (26 records) ⭐ NEW
- **milestones** ⭐ NEW
- **pf_capabilities** (102 links)
- **cap_technical_functions** (2 links)
- **pv_product_features** ⭐ NEW

## Key Files

- `app.py` - Main GUI (~3,900 lines)
- `database.py` - Database operations (~800 lines)
- `import_data.py` - Excel import
- `populate_*_swimlanes.py` - Swimlane standardization
- `export_to_sheets.py` - Google Sheets export

## Recent Updates (November 2025)

- ✅ Product Variants with auto-fill filtering
- ✅ Configurations management
- ✅ Interactive Plotly roadmap
- ✅ Milestone management
- ✅ TRL distribution charts
- ✅ Swimlane standardization (70 items corrected)
- ✅ Calendar picker widgets
- ✅ Dual query modes
- ✅ Enhanced capability linking

## Documentation

- **README.md** - This file
- **QUICKSTART.md** - Setup and usage guide
- **PROJECT_SUMMARY.md** - Detailed project overview
- **VISUAL_OVERVIEW.md** - Visual documentation
- **EDIT_GUIDE.md** - Editing guide
- **EXPORT_TO_SHEETS_README.md** - Google Sheets export

## Support

For issues or questions, refer to code comments in `database.py` and `app.py`, or see the documentation files above.
