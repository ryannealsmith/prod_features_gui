# Product Features Management System

A comprehensive GUI application for managing Product Features, Capabilities, and Technical Functions with many-to-many relationships, readiness matrix queries, and roadmap visualization.

## Features

### 1. **Database Management**
- SQLite relational database with proper schema
- Many-to-many relationships between:
  - Product Features ↔ Capabilities
  - Capabilities ↔ Technical Functions
- Full CRUD operations for all entities

### 2. **Product Features Management**
- View, add, edit, and delete product features
- Track TRL (Technology Readiness Level) dates: TRL3, TRL6, TRL9
- Filter by platform, ODD, environment
- Link/unlink capabilities to product features

### 3. **Capabilities Management**
- Manage capabilities with swimlane organization
- Track dates and dependencies
- Link to technical functions

### 4. **Technical Functions Management**
- Create and manage technical functions
- Organize by swimlane
- Link to capabilities

### 5. **Readiness Matrix Query Interface**
- Filter data by multiple criteria:
  - Platform
  - ODD (Operational Design Domain)
  - Environment
  - Swimlane
- View filtered results in organized tabs
- Export results to CSV

### 6. **Roadmap Visualization**
- Timeline view of product features and capabilities
- Visual representation based on TRL dates
- Updates dynamically based on readiness matrix filters
- Interactive matplotlib charts

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **Tkinter** (for GUI)

On macOS, tkinter should come with Python. If you encounter issues:
```bash
# Using Homebrew
brew install python-tk@3.13
```

On Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

### Setup

1. **Create a virtual environment** (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

2. **Install required packages**:
```bash
pip install openpyxl pandas matplotlib tkcalendar
```

3. **Import data from Excel**:
```bash
python import_data.py
```

This will create `product_features.db` with all the data from the Excel spreadsheet.

4. **Run the application**:
```bash
python app.py
```

## Usage Guide

### Product Features Tab
- **View**: Browse all product features in the left panel
- **Filter**: Use the filter dropdown to narrow results by platform
- **Edit**: Select a feature to view/edit details in the right panel
- **Add**: Click "Add New" to create a new product feature
- **Delete**: Select a feature and click "Delete"
- **Manage Capabilities**: 
  - View linked capabilities in the list
  - Click "Add Capability" to link existing capabilities
  - Select and click "Remove Capability" to unlink

### Capabilities Tab
- Similar interface for managing capabilities
- Edit swimlane, dates, and other attributes
- View dependencies and dependents

### Technical Functions Tab
- Manage technical functions
- Link to capabilities
- Organize by swimlane

### Readiness Matrix Tab
- **Set Filters**: Choose criteria from dropdown menus
- **Apply Query**: Click to filter results
- **View Results**: 
  - Product Features tab shows filtered features
  - Capabilities tab shows filtered capabilities
- **Export**: Save results to CSV file

### Roadmap Tab
- **Select View**: Choose to show Product Features, Capabilities, or Both
- **Update Roadmap**: Click to refresh the timeline visualization
- The chart displays milestones based on TRL dates
- Color-coded: Blue for Product Features, Green for Capabilities

## Database Schema

### Tables

1. **product_features**
   - Core product feature data
   - TRL dates (TRL3, TRL6, TRL9)
   - Platform, ODD, Environment attributes

2. **capabilities**
   - Capability definitions
   - Swimlane organization
   - TRL dates and dependencies

3. **technical_functions**
   - Technical function specifications
   - Swimlane categorization

4. **pf_capabilities** (Junction table)
   - Links product features to capabilities
   - Many-to-many relationship

5. **cap_technical_functions** (Junction table)
   - Links capabilities to technical functions
   - Many-to-many relationship

## File Structure

```
prod_features_gui/
├── Product Engineering Canonical Product Features.xlsx  # Source data
├── product_features.db          # SQLite database
├── database.py                  # Database operations
├── import_data.py               # Excel import script
├── app.py                       # Main GUI application
├── analyze_excel.py             # Excel analysis utility
└── README.md                    # This file
```

## Data Import Details

The `import_data.py` script:
- Reads from the Excel spreadsheet
- Parses "Product Features", "Capabilities", and "Technical Functions (WIP)" sheets
- Creates all database tables
- Imports all data with proper relationships
- Handles date parsing from various formats
- Links related entities based on the spreadsheet data

## Troubleshooting

### Tkinter Not Available
If you see `ModuleNotFoundError: No module named '_tkinter'`:
- On macOS: Install via Homebrew: `brew install python-tk@3.13`
- On Linux: `sudo apt-get install python3-tk`
- Make sure you're using the system Python or a Python with tkinter support

### Database Locked
If you encounter database lock errors:
- Close all instances of the application
- Delete `product_features.db` and re-run `import_data.py`

### Excel File Not Found
Ensure `Product Engineering Canonical Product Features.xlsx` is in the same directory as the scripts.

## Future Enhancements

Potential additions:
- User authentication and permissions
- Change history/audit trail
- Advanced search functionality
- Gantt chart view for roadmap
- Dependency graph visualization
- Import/export capabilities for other formats
- API for integration with other systems

## Technical Details

- **GUI Framework**: Tkinter (Python standard library)
- **Database**: SQLite3
- **Visualization**: Matplotlib
- **Data Processing**: Pandas, openpyxl
- **Architecture**: MVC-inspired with database layer separation

## Support

For issues or questions, refer to the code comments or database schema documentation in `database.py`.
