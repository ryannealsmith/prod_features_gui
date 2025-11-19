# Product Variant Export Guide

## Overview

The Product Variant export feature allows you to generate a comprehensive Markdown document that includes:

- Product Variant title, description, and configuration details
- All linked Product Features with their TRL completion dates
- All dependent Capabilities with TRL dates and cross-dependencies
- All dependent Technical Functions with TRL dates and cross-dependencies
- A visual roadmap snapshot showing the timeline for all dependencies

## How to Export a Product Variant

1. **Open the Application**
   ```bash
   .venv/bin/python app.py
   ```

2. **Navigate to Product Variants Tab**
   - Click on the "Product Variants" tab at the top of the window

3. **Select a Product Variant**
   - Click on the product variant you want to export from the list on the left

4. **Click Export Button**
   - Click the "Export to Markdown" button in the button frame
   - A file save dialog will appear

5. **Choose Save Location**
   - Select where you want to save the markdown file
   - The default filename will be `{ProductVariantLabel}_export.md`
   - Click "Save"

6. **Review the Generated File**
   - Open the markdown file in any markdown viewer or text editor
   - The roadmap image is saved to your system's temp directory

## Export Contents

### 1. Product Variant Overview
- Label and Title
- Description
- Target Date
- Export timestamp

### 2. Configuration Details
Complete configuration information including:
- **Platform**: Vehicle platform details
- **ODD (Operational Design Domain)**: Operating conditions
- **Environment**: Deployment environment
- **Trailer**: Trailer configuration
- **TRL**: Target Technology Readiness Level

### 3. Product Features
For each linked Product Feature:
- Label and Name
- Details/Description
- TRL completion dates (TRL3, TRL6, TRL9)
- Configuration (Platform, ODD, Environment, Trailer)
- List of dependent Capabilities
- List of dependent Technical Functions

### 4. All Capabilities
For each unique Capability across all Product Features:
- Label and Name
- Description
- TRL completion dates
- **Cross-dependencies**: Which Product Features use this Capability
- List of dependent Technical Functions

### 5. All Technical Functions
For each unique Technical Function:
- Label and Name
- Description
- TRL completion dates
- **Cross-dependencies**: Which Capabilities use this Technical Function

### 6. Roadmap Snapshot
A visual Gantt-style timeline showing:
- All Product Features, Capabilities, and Technical Functions
- TRL progression with color coding:
  - 🔴 Red: TRL3
  - 🟡 Amber: TRL6
  - 🟢 Green: TRL9
- Milestones marked with ⭐ stars
- Items grouped by type: [PF], [CAP], [TF]

## Example Use Cases

### 1. Project Documentation
Export a Product Variant to create comprehensive project documentation that shows:
- What features are being developed
- Their dependencies on capabilities and technical functions
- Timeline for completion
- Cross-dependencies between components

### 2. Stakeholder Reporting
Generate a detailed report for stakeholders showing:
- Current project scope
- Technology readiness progression
- Key dependencies and milestones
- Visual roadmap for easy understanding

### 3. Technical Planning
Use the export to:
- Identify shared capabilities across multiple product features
- Understand technical function dependencies
- Plan resource allocation based on TRL dates
- Identify bottlenecks in the dependency chain

### 4. Change Impact Analysis
When considering changes to a Capability or Technical Function:
- Export to see which Product Features depend on it
- Understand the ripple effects of changes
- Plan updates across the dependency tree

## File Format

The exported file is in Markdown format (`.md`), which means:
- ✅ Human-readable plain text
- ✅ Can be opened in any text editor
- ✅ Renders beautifully in Markdown viewers (VS Code, GitHub, etc.)
- ✅ Can be version-controlled with Git
- ✅ Easy to share and collaborate on
- ✅ Can be converted to PDF, HTML, or other formats

## Roadmap Image

The roadmap snapshot is saved as a PNG image to your system's temporary directory:
- **macOS/Linux**: `/tmp/{ProductVariantLabel}_roadmap.png`
- **Windows**: `C:\Users\{Username}\AppData\Local\Temp\{ProductVariantLabel}_roadmap.png`

The markdown file includes the path to this image so it can be viewed when opening the markdown file.

## Tips

1. **Select Product Features First**: Make sure your Product Variant has linked Product Features before exporting. The export will include all dependencies automatically.

2. **Regular Exports**: Export regularly to track progress over time. You can compare exports to see how dates and dependencies change.

3. **Share with Team**: The markdown format makes it easy to share with team members via email, Slack, or version control.

4. **Use with Git**: Add the exported markdown files to your Git repository for version-controlled documentation.

5. **Combine with Other Tools**: Import the markdown into documentation systems like Confluence, Notion, or static site generators.

## Troubleshooting

**Issue**: Export button is greyed out or shows warning
- **Solution**: Select a Product Variant from the list first

**Issue**: Export file is empty or incomplete
- **Solution**: Ensure the Product Variant has linked Product Features and that they have TRL dates set

**Issue**: Roadmap image doesn't display
- **Solution**: Check the image path in the markdown file. You may need to copy the image to the same directory as the markdown file

**Issue**: Export fails with an error
- **Solution**: Check the console for error details. Common issues:
  - Database connection problems
  - Missing data (TRL dates, configuration details)
  - Permissions to write to the selected directory

## Support

For issues or questions about the export feature:
1. Check the application logs
2. Verify database integrity
3. Ensure all required fields are filled in the Product Variant
4. Contact the development team with error details
