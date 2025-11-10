"""
Main GUI application for Product Features management.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import Database
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class ProductFeaturesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Features Management System")
        self.root.geometry("1400x900")
        
        self.db = Database()
        self.db.connect()
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_product_features_tab()
        self.create_capabilities_tab()
        self.create_technical_functions_tab()
        self.create_readiness_matrix_tab()
        self.create_roadmap_tab()
        
    def create_product_features_tab(self):
        """Create tab for managing Product Features."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Product Features")
        
        # Split into list and detail panes
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left pane - list
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Filters
        filter_frame = ttk.LabelFrame(left_frame, text="Filters", padding=5)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Platform:").grid(row=0, column=0, sticky=tk.W)
        self.pf_platform_filter = ttk.Combobox(filter_frame, state='readonly')
        self.pf_platform_filter.grid(row=0, column=1, padx=5, sticky=tk.EW)
        self.pf_platform_filter.bind('<<ComboboxSelected>>', lambda e: self.load_product_features())
        
        ttk.Button(filter_frame, text="Clear Filters", 
                  command=self.clear_pf_filters).grid(row=0, column=2, padx=5)
        
        filter_frame.columnconfigure(1, weight=1)
        
        # List
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar and Treeview
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pf_tree = ttk.Treeview(list_frame, 
                                     columns=('Label', 'Name', 'Platform', 'Start Date'),
                                     show='tree headings',
                                     yscrollcommand=scroll.set)
        scroll.config(command=self.pf_tree.yview)
        
        self.pf_tree.heading('Label', text='Label')
        self.pf_tree.heading('Name', text='Name')
        self.pf_tree.heading('Platform', text='Platform')
        self.pf_tree.heading('Start Date', text='Start Date')
        
        self.pf_tree.column('#0', width=0, stretch=False)
        self.pf_tree.column('Label', width=120)
        self.pf_tree.column('Name', width=250)
        self.pf_tree.column('Platform', width=100)
        self.pf_tree.column('Start Date', width=100)
        
        self.pf_tree.pack(fill=tk.BOTH, expand=True)
        self.pf_tree.bind('<<TreeviewSelect>>', self.on_pf_select)
        
        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Add New", 
                  command=self.add_product_feature).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", 
                  command=self.delete_product_feature).pack(side=tk.LEFT, padx=2)
        
        # Right pane - details
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        detail_frame = ttk.LabelFrame(right_frame, text="Details", padding=10)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create form
        self.pf_form = {}
        row = 0
        
        fields = [
            ('label', 'Label*:', 30),
            ('name', 'Name*:', 50),
            ('platform', 'Platform:', 30),
            ('odd', 'ODD:', 30),
            ('environment', 'Environment:', 30),
            ('trailer', 'Trailer:', 30),
            ('when_date', 'When:', 30),
            ('start_date', 'Start Date:', 15),
            ('trl3_date', 'TRL3 Date:', 15),
            ('trl6_date', 'TRL6 Date:', 15),
            ('trl9_date', 'TRL9 Date:', 15)
        ]
        
        for field_name, label_text, width in fields:
            ttk.Label(detail_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(detail_frame, width=width)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=3)
            self.pf_form[field_name] = entry
            row += 1
        
        # Text fields
        ttk.Label(detail_frame, text="Details:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        self.pf_form['details'] = scrolledtext.ScrolledText(detail_frame, height=4, width=50)
        self.pf_form['details'].grid(row=row, column=1, sticky=tk.EW, pady=3)
        row += 1
        
        ttk.Label(detail_frame, text="Comments:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        self.pf_form['comments'] = scrolledtext.ScrolledText(detail_frame, height=4, width=50)
        self.pf_form['comments'].grid(row=row, column=1, sticky=tk.EW, pady=3)
        row += 1
        
        # Capabilities section
        ttk.Label(detail_frame, text="Capabilities:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        
        cap_frame = ttk.Frame(detail_frame)
        cap_frame.grid(row=row, column=1, sticky=tk.EW, pady=3)
        
        cap_scroll = ttk.Scrollbar(cap_frame)
        cap_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pf_capabilities_list = tk.Listbox(cap_frame, height=6, 
                                                yscrollcommand=cap_scroll.set)
        self.pf_capabilities_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cap_scroll.config(command=self.pf_capabilities_list.yview)
        row += 1
        
        # Capability management buttons
        cap_btn_frame = ttk.Frame(detail_frame)
        cap_btn_frame.grid(row=row, column=1, sticky=tk.W, pady=3)
        ttk.Button(cap_btn_frame, text="Add Capability", 
                  command=self.add_pf_capability).pack(side=tk.LEFT, padx=2)
        ttk.Button(cap_btn_frame, text="Remove Capability", 
                  command=self.remove_pf_capability).pack(side=tk.LEFT, padx=2)
        row += 1
        
        # Save button
        ttk.Button(detail_frame, text="Save Changes", 
                  command=self.save_product_feature).grid(row=row, column=1, sticky=tk.E, pady=10)
        
        detail_frame.columnconfigure(1, weight=1)
        
        self.current_pf_id = None
        self.load_pf_filters()
        self.load_product_features()
    
    def create_capabilities_tab(self):
        """Create tab for managing Capabilities."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Capabilities")
        
        # Similar structure to Product Features
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left pane
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # List
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cap_tree = ttk.Treeview(list_frame,
                                      columns=('Label', 'Name', 'Swimlane'),
                                      show='tree headings',
                                      yscrollcommand=scroll.set)
        scroll.config(command=self.cap_tree.yview)
        
        self.cap_tree.heading('Label', text='Label')
        self.cap_tree.heading('Name', text='Name')
        self.cap_tree.heading('Swimlane', text='Swimlane')
        
        self.cap_tree.column('#0', width=0, stretch=False)
        self.cap_tree.column('Label', width=120)
        self.cap_tree.column('Name', width=300)
        self.cap_tree.column('Swimlane', width=100)
        
        self.cap_tree.pack(fill=tk.BOTH, expand=True)
        self.cap_tree.bind('<<TreeviewSelect>>', self.on_cap_select)
        
        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Add New", 
                  command=self.add_capability).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", 
                  command=self.delete_capability).pack(side=tk.LEFT, padx=2)
        
        # Right pane
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        detail_frame = ttk.LabelFrame(right_frame, text="Details", padding=10)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create form
        self.cap_form = {}
        row = 0
        
        fields = [
            ('label', 'Label*:', 30),
            ('name', 'Name*:', 50),
            ('swimlane', 'Swimlane:', 20),
            ('platform', 'Platform:', 30),
            ('start_date', 'Start Date:', 15),
            ('trl3_date', 'TRL3 Date:', 15),
            ('trl6_date', 'TRL6 Date:', 15),
            ('trl9_date', 'TRL9 Date:', 15)
        ]
        
        for field_name, label_text, width in fields:
            ttk.Label(detail_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(detail_frame, width=width)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=3)
            self.cap_form[field_name] = entry
            row += 1
        
        ttk.Label(detail_frame, text="Details:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        self.cap_form['details'] = scrolledtext.ScrolledText(detail_frame, height=4, width=50)
        self.cap_form['details'].grid(row=row, column=1, sticky=tk.EW, pady=3)
        row += 1
        
        ttk.Button(detail_frame, text="Save Changes",
                  command=self.save_capability).grid(row=row, column=1, sticky=tk.E, pady=10)
        
        detail_frame.columnconfigure(1, weight=1)
        
        self.current_cap_id = None
        self.load_capabilities()
    
    def create_technical_functions_tab(self):
        """Create tab for managing Technical Functions."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Technical Functions")
        
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left pane
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tf_tree = ttk.Treeview(list_frame,
                                     columns=('Label', 'Name', 'Swimlane'),
                                     show='tree headings',
                                     yscrollcommand=scroll.set)
        scroll.config(command=self.tf_tree.yview)
        
        self.tf_tree.heading('Label', text='Label')
        self.tf_tree.heading('Name', text='Name')
        self.tf_tree.heading('Swimlane', text='Swimlane')
        
        self.tf_tree.column('#0', width=0, stretch=False)
        self.tf_tree.column('Label', width=120)
        self.tf_tree.column('Name', width=300)
        self.tf_tree.column('Swimlane', width=100)
        
        self.tf_tree.pack(fill=tk.BOTH, expand=True)
        self.tf_tree.bind('<<TreeviewSelect>>', self.on_tf_select)
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Add New",
                  command=self.add_technical_function).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete",
                  command=self.delete_technical_function).pack(side=tk.LEFT, padx=2)
        
        # Right pane
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        detail_frame = ttk.LabelFrame(right_frame, text="Details", padding=10)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tf_form = {}
        row = 0
        
        fields = [
            ('label', 'Label*:', 30),
            ('name', 'Name*:', 50),
            ('swimlane', 'Swimlane:', 20),
            ('platform', 'Platform:', 30)
        ]
        
        for field_name, label_text, width in fields:
            ttk.Label(detail_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(detail_frame, width=width)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=3)
            self.tf_form[field_name] = entry
            row += 1
        
        ttk.Label(detail_frame, text="Details:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        self.tf_form['details'] = scrolledtext.ScrolledText(detail_frame, height=4, width=50)
        self.tf_form['details'].grid(row=row, column=1, sticky=tk.EW, pady=3)
        row += 1
        
        ttk.Button(detail_frame, text="Save Changes",
                  command=self.save_technical_function).grid(row=row, column=1, sticky=tk.E, pady=10)
        
        detail_frame.columnconfigure(1, weight=1)
        
        self.current_tf_id = None
        self.load_technical_functions()
    
    def create_readiness_matrix_tab(self):
        """Create Readiness Matrix query interface."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Readiness Matrix")
        
        # Filters section
        filter_frame = ttk.LabelFrame(tab, text="Query Filters", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        row = 0
        ttk.Label(filter_frame, text="Platform:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.rm_platform = ttk.Combobox(filter_frame, state='readonly', width=25)
        self.rm_platform.grid(row=row, column=1, sticky=tk.W, padx=5, pady=3)
        
        ttk.Label(filter_frame, text="ODD:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.rm_odd = ttk.Combobox(filter_frame, state='readonly', width=25)
        self.rm_odd.grid(row=row, column=3, sticky=tk.W, padx=5, pady=3)
        row += 1
        
        ttk.Label(filter_frame, text="Environment:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.rm_environment = ttk.Combobox(filter_frame, state='readonly', width=25)
        self.rm_environment.grid(row=row, column=1, sticky=tk.W, padx=5, pady=3)
        
        ttk.Label(filter_frame, text="Swimlane:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.rm_swimlane = ttk.Combobox(filter_frame, state='readonly', width=25)
        self.rm_swimlane.grid(row=row, column=3, sticky=tk.W, padx=5, pady=3)
        row += 1
        
        btn_frame = ttk.Frame(filter_frame)
        btn_frame.grid(row=row, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Apply Query", 
                  command=self.apply_readiness_query).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Filters", 
                  command=self.clear_readiness_filters).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export Results", 
                  command=self.export_readiness_results).pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(tab, text="Query Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for different result views
        results_notebook = ttk.Notebook(results_frame)
        results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Product Features results
        pf_tab = ttk.Frame(results_notebook)
        results_notebook.add(pf_tab, text="Product Features")
        
        pf_scroll = ttk.Scrollbar(pf_tab)
        pf_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.rm_pf_tree = ttk.Treeview(pf_tab,
                                        columns=('Label', 'Name', 'Platform', 'TRL3', 'TRL6', 'TRL9'),
                                        show='tree headings',
                                        yscrollcommand=pf_scroll.set)
        pf_scroll.config(command=self.rm_pf_tree.yview)
        
        for col in ('Label', 'Name', 'Platform', 'TRL3', 'TRL6', 'TRL9'):
            self.rm_pf_tree.heading(col, text=col)
        
        self.rm_pf_tree.column('#0', width=0, stretch=False)
        self.rm_pf_tree.pack(fill=tk.BOTH, expand=True)
        
        # Capabilities results
        cap_tab = ttk.Frame(results_notebook)
        results_notebook.add(cap_tab, text="Capabilities")
        
        cap_scroll = ttk.Scrollbar(cap_tab)
        cap_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.rm_cap_tree = ttk.Treeview(cap_tab,
                                         columns=('Label', 'Name', 'Swimlane', 'TRL3', 'TRL6', 'TRL9'),
                                         show='tree headings',
                                         yscrollcommand=cap_scroll.set)
        cap_scroll.config(command=self.rm_cap_tree.yview)
        
        for col in ('Label', 'Name', 'Swimlane', 'TRL3', 'TRL6', 'TRL9'):
            self.rm_cap_tree.heading(col, text=col)
        
        self.rm_cap_tree.column('#0', width=0, stretch=False)
        self.rm_cap_tree.pack(fill=tk.BOTH, expand=True)
        
        self.load_readiness_filters()
    
    def create_roadmap_tab(self):
        """Create Roadmap visualization."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Roadmap")
        
        # Controls
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="View:").pack(side=tk.LEFT, padx=5)
        self.roadmap_view = ttk.Combobox(control_frame, 
                                         values=['Product Features', 'Capabilities', 'Both'],
                                         state='readonly',
                                         width=20)
        self.roadmap_view.set('Product Features')
        self.roadmap_view.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Update Roadmap",
                  command=self.update_roadmap).pack(side=tk.LEFT, padx=5)
        
        # Canvas for matplotlib
        self.roadmap_frame = ttk.Frame(tab)
        self.roadmap_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.update_roadmap()
    
    # Data loading methods
    def load_pf_filters(self):
        """Load filter options for Product Features."""
        platforms = [''] + self.db.get_unique_values('product_features', 'platform')
        self.pf_platform_filter['values'] = platforms
        
    def clear_pf_filters(self):
        """Clear Product Features filters."""
        self.pf_platform_filter.set('')
        self.load_product_features()
        
    def load_product_features(self):
        """Load product features into the tree."""
        # Clear current items
        for item in self.pf_tree.get_children():
            self.pf_tree.delete(item)
        
        # Get filters
        filters = {}
        if self.pf_platform_filter.get():
            filters['platform'] = self.pf_platform_filter.get()
        
        # Load data
        features = self.db.get_product_features(filters)
        
        for feature in features:
            self.pf_tree.insert('', tk.END, iid=feature['id'],
                               values=(feature['label'], 
                                      feature['name'],
                                      feature['platform'],
                                      feature['start_date']))
    
    def on_pf_select(self, event):
        """Handle Product Feature selection."""
        selection = self.pf_tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        self.current_pf_id = int(item_id)
        
        # Load details
        pf = self.db.get_product_feature_by_id(self.current_pf_id)
        if not pf:
            return
        
        # Populate form
        text_fields = ['details', 'comments']
        for field_name, widget in self.pf_form.items():
            if field_name in text_fields:
                widget.delete('1.0', tk.END)
                if pf.get(field_name):
                    widget.insert('1.0', pf[field_name])
            else:
                widget.delete(0, tk.END)
                if pf.get(field_name):
                    widget.insert(0, str(pf[field_name]))
        
        # Load capabilities
        self.pf_capabilities_list.delete(0, tk.END)
        caps = self.db.get_pf_capabilities(self.current_pf_id)
        for cap in caps:
            self.pf_capabilities_list.insert(tk.END, f"{cap['label']} - {cap['name']}")
    
    def save_product_feature(self):
        """Save Product Feature changes."""
        if not self.current_pf_id:
            messagebox.showwarning("No Selection", "Please select a product feature to edit.")
            return
        
        # Collect data
        data = {}
        text_fields = ['details', 'comments']
        for field_name, widget in self.pf_form.items():
            if field_name in text_fields:
                data[field_name] = widget.get('1.0', tk.END).strip()
            else:
                data[field_name] = widget.get().strip() or None
        
        try:
            self.db.update_product_feature(self.current_pf_id, data)
            messagebox.showinfo("Success", "Product Feature updated successfully!")
            self.load_product_features()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")
    
    def add_product_feature(self):
        """Add a new Product Feature."""
        # Open dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product Feature")
        dialog.geometry("500x400")
        
        form = {}
        row = 0
        
        fields = [
            ('label', 'Label*:', 30),
            ('name', 'Name*:', 40),
            ('platform', 'Platform:', 30)
        ]
        
        for field_name, label_text, width in fields:
            ttk.Label(dialog, text=label_text).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(dialog, width=width)
            entry.grid(row=row, column=1, sticky=tk.W, padx=10, pady=5)
            form[field_name] = entry
            row += 1
        
        def save_new():
            data = {
                'label': form['label'].get().strip(),
                'name': form['name'].get().strip(),
                'platform': form['platform'].get().strip() or None
            }
            
            if not data['label'] or not data['name']:
                messagebox.showwarning("Missing Data", "Label and Name are required!")
                return
            
            try:
                self.db.add_product_feature(data)
                messagebox.showinfo("Success", "Product Feature added successfully!")
                dialog.destroy()
                self.load_product_features()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save_new).grid(row=row, column=1, sticky=tk.E, padx=10, pady=10)
    
    def delete_product_feature(self):
        """Delete selected Product Feature."""
        if not self.current_pf_id:
            messagebox.showwarning("No Selection", "Please select a product feature to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product feature?"):
            try:
                self.db.delete_product_feature(self.current_pf_id)
                messagebox.showinfo("Success", "Product Feature deleted successfully!")
                self.current_pf_id = None
                self.load_product_features()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
    
    def add_pf_capability(self):
        """Add a capability to the current product feature."""
        if not self.current_pf_id:
            messagebox.showwarning("No Selection", "Please select a product feature first.")
            return
        
        # Open dialog to select capability
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Capability")
        dialog.geometry("500x400")
        
        ttk.Label(dialog, text="Select Capability:").pack(padx=10, pady=10)
        
        listbox = tk.Listbox(dialog, height=15)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load all capabilities
        caps = self.db.get_capabilities()
        cap_map = {}
        for cap in caps:
            display_text = f"{cap['label']} - {cap['name']}"
            listbox.insert(tk.END, display_text)
            cap_map[display_text] = cap['id']
        
        def add_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a capability.")
                return
            
            selected_text = listbox.get(selection[0])
            cap_id = cap_map[selected_text]
            
            self.db.link_pf_capability(self.current_pf_id, cap_id)
            messagebox.showinfo("Success", "Capability linked successfully!")
            dialog.destroy()
            self.on_pf_select(None)  # Refresh the capabilities list
        
        ttk.Button(dialog, text="Add", command=add_selected).pack(pady=10)
    
    def remove_pf_capability(self):
        """Remove a capability from the current product feature."""
        if not self.current_pf_id:
            messagebox.showwarning("No Selection", "Please select a product feature first.")
            return
        
        selection = self.pf_capabilities_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a capability to remove.")
            return
        
        # Get the capability label from the selection
        selected_text = self.pf_capabilities_list.get(selection[0])
        cap_label = selected_text.split(' - ')[0]
        
        # Find capability ID
        caps = self.db.get_capabilities()
        cap_id = None
        for cap in caps:
            if cap['label'] == cap_label:
                cap_id = cap['id']
                break
        
        if cap_id:
            self.db.unlink_pf_capability(self.current_pf_id, cap_id)
            messagebox.showinfo("Success", "Capability unlinked successfully!")
            self.on_pf_select(None)  # Refresh
    
    def load_capabilities(self):
        """Load capabilities into the tree."""
        for item in self.cap_tree.get_children():
            self.cap_tree.delete(item)
        
        caps = self.db.get_capabilities()
        
        for cap in caps:
            self.cap_tree.insert('', tk.END, iid=cap['id'],
                                values=(cap['label'], cap['name'], cap['swimlane']))
    
    def on_cap_select(self, event):
        """Handle Capability selection."""
        selection = self.cap_tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        self.current_cap_id = int(item_id)
        
        cap = self.db.get_capability_by_id(self.current_cap_id)
        if not cap:
            return
        
        text_fields = ['details']
        for field_name, widget in self.cap_form.items():
            if field_name in text_fields:
                widget.delete('1.0', tk.END)
                if cap.get(field_name):
                    widget.insert('1.0', cap[field_name])
            else:
                widget.delete(0, tk.END)
                if cap.get(field_name):
                    widget.insert(0, str(cap[field_name]))
    
    def save_capability(self):
        """Save Capability changes."""
        if not self.current_cap_id:
            messagebox.showwarning("No Selection", "Please select a capability to edit.")
            return
        
        data = {}
        text_fields = ['details']
        for field_name, widget in self.cap_form.items():
            if field_name in text_fields:
                data[field_name] = widget.get('1.0', tk.END).strip()
            else:
                data[field_name] = widget.get().strip() or None
        
        try:
            self.db.update_capability(self.current_cap_id, data)
            messagebox.showinfo("Success", "Capability updated successfully!")
            self.load_capabilities()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")
    
    def add_capability(self):
        """Add new capability."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Capability")
        dialog.geometry("500x300")
        
        form = {}
        row = 0
        
        fields = [('label', 'Label*:', 30), ('name', 'Name*:', 40), ('swimlane', 'Swimlane:', 30)]
        
        for field_name, label_text, width in fields:
            ttk.Label(dialog, text=label_text).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(dialog, width=width)
            entry.grid(row=row, column=1, sticky=tk.W, padx=10, pady=5)
            form[field_name] = entry
            row += 1
        
        def save_new():
            data = {
                'label': form['label'].get().strip(),
                'name': form['name'].get().strip(),
                'swimlane': form['swimlane'].get().strip() or None
            }
            
            if not data['label'] or not data['name']:
                messagebox.showwarning("Missing Data", "Label and Name are required!")
                return
            
            try:
                self.db.add_capability(data)
                messagebox.showinfo("Success", "Capability added successfully!")
                dialog.destroy()
                self.load_capabilities()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save_new).grid(row=row, column=1, sticky=tk.E, padx=10, pady=10)
    
    def delete_capability(self):
        """Delete selected capability."""
        if not self.current_cap_id:
            messagebox.showwarning("No Selection", "Please select a capability to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this capability?"):
            try:
                self.db.delete_capability(self.current_cap_id)
                messagebox.showinfo("Success", "Capability deleted successfully!")
                self.current_cap_id = None
                self.load_capabilities()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
    
    def load_technical_functions(self):
        """Load technical functions into the tree."""
        for item in self.tf_tree.get_children():
            self.tf_tree.delete(item)
        
        tfs = self.db.get_technical_functions()
        
        for tf in tfs:
            self.tf_tree.insert('', tk.END, iid=tf['id'],
                               values=(tf['label'], tf['name'], tf['swimlane']))
    
    def on_tf_select(self, event):
        """Handle Technical Function selection."""
        selection = self.tf_tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        self.current_tf_id = int(item_id)
        
        tf = self.db.get_technical_function_by_id(self.current_tf_id)
        if not tf:
            return
        
        text_fields = ['details']
        for field_name, widget in self.tf_form.items():
            if field_name in text_fields:
                widget.delete('1.0', tk.END)
                if tf.get(field_name):
                    widget.insert('1.0', tf[field_name])
            else:
                widget.delete(0, tk.END)
                if tf.get(field_name):
                    widget.insert(0, str(tf[field_name]))
    
    def save_technical_function(self):
        """Save Technical Function changes."""
        if not self.current_tf_id:
            messagebox.showwarning("No Selection", "Please select a technical function to edit.")
            return
        
        data = {}
        text_fields = ['details']
        for field_name, widget in self.tf_form.items():
            if field_name in text_fields:
                data[field_name] = widget.get('1.0', tk.END).strip()
            else:
                data[field_name] = widget.get().strip() or None
        
        try:
            self.db.update_technical_function(self.current_tf_id, data)
            messagebox.showinfo("Success", "Technical Function updated successfully!")
            self.load_technical_functions()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")
    
    def add_technical_function(self):
        """Add new technical function."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Technical Function")
        dialog.geometry("500x300")
        
        form = {}
        row = 0
        
        fields = [('label', 'Label*:', 30), ('name', 'Name*:', 40), ('swimlane', 'Swimlane:', 30)]
        
        for field_name, label_text, width in fields:
            ttk.Label(dialog, text=label_text).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(dialog, width=width)
            entry.grid(row=row, column=1, sticky=tk.W, padx=10, pady=5)
            form[field_name] = entry
            row += 1
        
        def save_new():
            data = {
                'label': form['label'].get().strip(),
                'name': form['name'].get().strip(),
                'swimlane': form['swimlane'].get().strip() or None
            }
            
            if not data['label'] or not data['name']:
                messagebox.showwarning("Missing Data", "Label and Name are required!")
                return
            
            try:
                self.db.add_technical_function(data)
                messagebox.showinfo("Success", "Technical Function added successfully!")
                dialog.destroy()
                self.load_technical_functions()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add: {str(e)}")
        
        ttk.Button(dialog, text="Save", command=save_new).grid(row=row, column=1, sticky=tk.E, padx=10, pady=10)
    
    def delete_technical_function(self):
        """Delete selected technical function."""
        if not self.current_tf_id:
            messagebox.showwarning("No Selection", "Please select a technical function to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this technical function?"):
            try:
                self.db.delete_technical_function(self.current_tf_id)
                messagebox.showinfo("Success", "Technical Function deleted successfully!")
                self.current_tf_id = None
                self.load_technical_functions()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
    
    def load_readiness_filters(self):
        """Load filter options for Readiness Matrix."""
        platforms = [''] + self.db.get_unique_values('product_features', 'platform')
        self.rm_platform['values'] = platforms
        
        odds = [''] + self.db.get_unique_values('product_features', 'odd')
        self.rm_odd['values'] = odds
        
        envs = [''] + self.db.get_unique_values('product_features', 'environment')
        self.rm_environment['values'] = envs
        
        swimlanes = [''] + self.db.get_unique_values('capabilities', 'swimlane')
        self.rm_swimlane['values'] = swimlanes
    
    def clear_readiness_filters(self):
        """Clear Readiness Matrix filters."""
        self.rm_platform.set('')
        self.rm_odd.set('')
        self.rm_environment.set('')
        self.rm_swimlane.set('')
        self.apply_readiness_query()
    
    def apply_readiness_query(self):
        """Apply Readiness Matrix query."""
        # Clear current results
        for item in self.rm_pf_tree.get_children():
            self.rm_pf_tree.delete(item)
        for item in self.rm_cap_tree.get_children():
            self.rm_cap_tree.delete(item)
        
        # Build filters
        pf_filters = {}
        if self.rm_platform.get():
            pf_filters['platform'] = self.rm_platform.get()
        if self.rm_odd.get():
            pf_filters['odd'] = self.rm_odd.get()
        if self.rm_environment.get():
            pf_filters['environment'] = self.rm_environment.get()
        
        cap_filters = {}
        if self.rm_platform.get():
            cap_filters['platform'] = self.rm_platform.get()
        if self.rm_swimlane.get():
            cap_filters['swimlane'] = self.rm_swimlane.get()
        
        # Load Product Features
        pfs = self.db.get_product_features(pf_filters)
        for pf in pfs:
            self.rm_pf_tree.insert('', tk.END,
                                   values=(pf['label'], pf['name'], pf['platform'],
                                          pf['trl3_date'], pf['trl6_date'], pf['trl9_date']))
        
        # Load Capabilities
        caps = self.db.get_capabilities(cap_filters)
        for cap in caps:
            self.rm_cap_tree.insert('', tk.END,
                                    values=(cap['label'], cap['name'], cap['swimlane'],
                                           cap['trl3_date'], cap['trl6_date'], cap['trl9_date']))
    
    def export_readiness_results(self):
        """Export readiness matrix results to CSV."""
        import csv
        from tkinter import filedialog
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write Product Features
                writer.writerow(['Product Features'])
                writer.writerow(['Label', 'Name', 'Platform', 'TRL3', 'TRL6', 'TRL9'])
                
                for item in self.rm_pf_tree.get_children():
                    values = self.rm_pf_tree.item(item)['values']
                    writer.writerow(values)
                
                writer.writerow([])
                
                # Write Capabilities
                writer.writerow(['Capabilities'])
                writer.writerow(['Label', 'Name', 'Swimlane', 'TRL3', 'TRL6', 'TRL9'])
                
                for item in self.rm_cap_tree.get_children():
                    values = self.rm_cap_tree.item(item)['values']
                    writer.writerow(values)
            
            messagebox.showinfo("Success", f"Results exported to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def update_roadmap(self):
        """Update the roadmap visualization."""
        # Clear previous plot
        for widget in self.roadmap_frame.winfo_children():
            widget.destroy()
        
        # Get current filters from readiness matrix if any
        pf_filters = {}
        if hasattr(self, 'rm_platform') and self.rm_platform.get():
            pf_filters['platform'] = self.rm_platform.get()
        
        # Create figure
        fig = Figure(figsize=(12, 8), dpi=100)
        ax = fig.add_subplot(111)
        
        view = self.roadmap_view.get()
        
        # Collect items with dates
        items = []
        
        if view in ['Product Features', 'Both']:
            pfs = self.db.get_product_features(pf_filters)
            for pf in pfs:
                for trl, date_field in [('TRL3', 'trl3_date'), ('TRL6', 'trl6_date'), ('TRL9', 'trl9_date')]:
                    if pf.get(date_field):
                        try:
                            date = datetime.strptime(pf[date_field], '%Y-%m-%d')
                            items.append({
                                'date': date,
                                'label': f"{pf['label']} ({trl})",
                                'type': 'PF',
                                'color': 'blue'
                            })
                        except:
                            pass
        
        if view in ['Capabilities', 'Both']:
            caps = self.db.get_capabilities()
            for cap in caps:
                for trl, date_field in [('TRL3', 'trl3_date'), ('TRL6', 'trl6_date'), ('TRL9', 'trl9_date')]:
                    if cap.get(date_field):
                        try:
                            date = datetime.strptime(cap[date_field], '%Y-%m-%d')
                            items.append({
                                'date': date,
                                'label': f"{cap['label']} ({trl})",
                                'type': 'CAP',
                                'color': 'green'
                            })
                        except:
                            pass
        
        if not items:
            ax.text(0.5, 0.5, 'No timeline data available', 
                   ha='center', va='center', fontsize=14)
        else:
            # Sort by date
            items.sort(key=lambda x: x['date'])
            
            # Create timeline
            dates = [item['date'] for item in items]
            y_positions = list(range(len(items)))
            colors = [item['color'] for item in items]
            labels = [item['label'] for item in items]
            
            ax.scatter(dates, y_positions, c=colors, s=100, alpha=0.6)
            
            # Add labels
            for i, item in enumerate(items):
                ax.text(item['date'], i, f"  {item['label']}", 
                       va='center', fontsize=8)
            
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Milestones', fontsize=12)
            ax.set_title('Product Roadmap', fontsize=14, fontweight='bold')
            
            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            fig.autofmt_xdate()
            
            ax.grid(True, alpha=0.3)
            ax.set_yticks([])
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.roadmap_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def __del__(self):
        """Cleanup."""
        if hasattr(self, 'db'):
            self.db.close()

def main():
    root = tk.Tk()
    app = ProductFeaturesApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
