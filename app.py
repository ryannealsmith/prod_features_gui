"""
Main GUI application for Product Features management.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from tkcalendar import Calendar
from database import Database
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import json

class ProductFeaturesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product, Capability and Technical Roadmapping Management Tool")
        self.root.geometry("1400x900")
        
        self.db = Database()
        self.db.connect()
        
        # Create menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export to JSON", command=self.export_to_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_configurations_tab()
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
                                     columns=('Label', 'Name', 'Swimlane', 'Platform', 'Start Date', 'TRL3', 'TRL6', 'TRL9'),
                                     show='tree headings',
                                     yscrollcommand=scroll.set)
        scroll.config(command=self.pf_tree.yview)
        
        self.pf_tree.heading('Label', text='Label')
        self.pf_tree.heading('Name', text='Name')
        self.pf_tree.heading('Swimlane', text='Swimlane')
        self.pf_tree.heading('Platform', text='Platform')
        self.pf_tree.heading('Start Date', text='Start Date')
        self.pf_tree.heading('TRL3', text='TRL3')
        self.pf_tree.heading('TRL6', text='TRL6')
        self.pf_tree.heading('TRL9', text='TRL9')
        
        self.pf_tree.column('#0', width=0, stretch=False)
        self.pf_tree.column('Label', width=100)
        self.pf_tree.column('Name', width=200)
        self.pf_tree.column('Swimlane', width=80)
        self.pf_tree.column('Platform', width=90)
        self.pf_tree.column('Start Date', width=90)
        self.pf_tree.column('TRL3', width=90)
        self.pf_tree.column('TRL6', width=90)
        self.pf_tree.column('TRL9', width=90)
        
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
        
        # Text entry fields
        text_fields = [
            ('label', 'Label*:', 30),
            ('name', 'Name*:', 50),
            ('swimlane', 'Swimlane:', 20),
            ('when_date', 'When:', 30),
            ('start_date', 'Start Date:', 15),
            ('trl3_date', 'TRL3 Date:', 15),
            ('trl6_date', 'TRL6 Date:', 15),
            ('trl9_date', 'TRL9 Date:', 15)
        ]
        
        for field_name, label_text, width in text_fields:
            ttk.Label(detail_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(detail_frame, width=width)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=3)
            self.pf_form[field_name] = entry
            row += 1
        
        # Combobox fields for configurations
        combo_fields = [
            ('platform', 'Platform:', 'Platform'),
            ('odd', 'ODD:', 'ODD'),
            ('environment', 'Environment:', 'Environment'),
            ('trailer', 'Trailer:', 'Trailer')
        ]
        
        for field_name, label_text, config_type in combo_fields:
            ttk.Label(detail_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3)
            combo = ttk.Combobox(detail_frame, width=27)
            combo['values'] = [''] + self.get_config_codes(config_type)
            combo.grid(row=row, column=1, sticky=tk.EW, pady=3)
            self.pf_form[field_name] = combo
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
                                      columns=('Label', 'Name', 'Swimlane', 'Start Date', 'TRL3', 'TRL6', 'TRL9'),
                                      show='tree headings',
                                      yscrollcommand=scroll.set)
        scroll.config(command=self.cap_tree.yview)
        
        self.cap_tree.heading('Label', text='Label')
        self.cap_tree.heading('Name', text='Name')
        self.cap_tree.heading('Swimlane', text='Swimlane')
        self.cap_tree.heading('Start Date', text='Start Date')
        self.cap_tree.heading('TRL3', text='TRL3')
        self.cap_tree.heading('TRL6', text='TRL6')
        self.cap_tree.heading('TRL9', text='TRL9')
        
        self.cap_tree.column('#0', width=0, stretch=False)
        self.cap_tree.column('Label', width=100)
        self.cap_tree.column('Name', width=200)
        self.cap_tree.column('Swimlane', width=80)
        self.cap_tree.column('Start Date', width=90)
        self.cap_tree.column('TRL3', width=90)
        self.cap_tree.column('TRL6', width=90)
        self.cap_tree.column('TRL9', width=90)
        
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
        
        # Text entry fields
        text_fields = [
            ('label', 'Label*:', 30),
            ('name', 'Name*:', 50),
            ('swimlane', 'Swimlane:', 20),
            ('start_date', 'Start Date:', 15),
            ('trl3_date', 'TRL3 Date:', 15),
            ('trl6_date', 'TRL6 Date:', 15),
            ('trl9_date', 'TRL9 Date:', 15)
        ]
        
        for field_name, label_text, width in text_fields:
            ttk.Label(detail_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(detail_frame, width=width)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=3)
            self.cap_form[field_name] = entry
            row += 1
        
        # Combobox field for platform
        ttk.Label(detail_frame, text='Platform:').grid(row=row, column=0, sticky=tk.W, pady=3)
        platform_combo = ttk.Combobox(detail_frame, width=27)
        platform_combo['values'] = [''] + self.get_config_codes('Platform')
        platform_combo.grid(row=row, column=1, sticky=tk.EW, pady=3)
        self.cap_form['platform'] = platform_combo
        row += 1
        
        ttk.Label(detail_frame, text="Details:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        self.cap_form['details'] = scrolledtext.ScrolledText(detail_frame, height=4, width=50)
        self.cap_form['details'].grid(row=row, column=1, sticky=tk.EW, pady=3)
        row += 1
        
        # Technical Functions section
        ttk.Label(detail_frame, text="Technical Functions:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        
        tf_frame = ttk.Frame(detail_frame)
        tf_frame.grid(row=row, column=1, sticky=tk.EW, pady=3)
        
        tf_scroll = ttk.Scrollbar(tf_frame)
        tf_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cap_tfs_list = tk.Listbox(tf_frame, height=4, 
                                        yscrollcommand=tf_scroll.set)
        self.cap_tfs_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tf_scroll.config(command=self.cap_tfs_list.yview)
        row += 1
        
        # Technical Function management buttons
        tf_btn_frame = ttk.Frame(detail_frame)
        tf_btn_frame.grid(row=row, column=1, sticky=tk.W, pady=3)
        ttk.Button(tf_btn_frame, text="Add Technical Function", 
                  command=self.add_cap_tf).pack(side=tk.LEFT, padx=2)
        ttk.Button(tf_btn_frame, text="Remove Technical Function", 
                  command=self.remove_cap_tf).pack(side=tk.LEFT, padx=2)
        row += 1
        
        # Product Features section
        ttk.Label(detail_frame, text="Product Features:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        
        pf_frame = ttk.Frame(detail_frame)
        pf_frame.grid(row=row, column=1, sticky=tk.EW, pady=3)
        
        pf_scroll = ttk.Scrollbar(pf_frame)
        pf_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cap_pfs_list = tk.Listbox(pf_frame, height=4, 
                                        yscrollcommand=pf_scroll.set)
        self.cap_pfs_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pf_scroll.config(command=self.cap_pfs_list.yview)
        row += 1
        
        # Product Feature management buttons
        pf_btn_frame = ttk.Frame(detail_frame)
        pf_btn_frame.grid(row=row, column=1, sticky=tk.W, pady=3)
        ttk.Button(pf_btn_frame, text="Add Product Feature", 
                  command=self.add_cap_pf).pack(side=tk.LEFT, padx=2)
        ttk.Button(pf_btn_frame, text="Remove Product Feature", 
                  command=self.remove_cap_pf).pack(side=tk.LEFT, padx=2)
        row += 1
        
        # Save button
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
        
        # Text entry fields
        text_fields = [
            ('label', 'Label*:', 30),
            ('name', 'Name*:', 50),
            ('swimlane', 'Swimlane:', 20)
        ]
        
        for field_name, label_text, width in text_fields:
            ttk.Label(detail_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=3)
            entry = ttk.Entry(detail_frame, width=width)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=3)
            self.tf_form[field_name] = entry
            row += 1
        
        # Combobox field for platform
        ttk.Label(detail_frame, text='Platform:').grid(row=row, column=0, sticky=tk.W, pady=3)
        platform_combo = ttk.Combobox(detail_frame, width=27)
        platform_combo['values'] = [''] + self.get_config_codes('Platform')
        platform_combo.grid(row=row, column=1, sticky=tk.EW, pady=3)
        self.tf_form['platform'] = platform_combo
        row += 1
        
        ttk.Label(detail_frame, text="Details:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        self.tf_form['details'] = scrolledtext.ScrolledText(detail_frame, height=4, width=50)
        self.tf_form['details'].grid(row=row, column=1, sticky=tk.EW, pady=3)
        row += 1
        
        # Capabilities section
        ttk.Label(detail_frame, text="Enabled Capabilities:").grid(row=row, column=0, sticky=tk.NW, pady=3)
        
        cap_frame = ttk.Frame(detail_frame)
        cap_frame.grid(row=row, column=1, sticky=tk.EW, pady=3)
        
        cap_scroll = ttk.Scrollbar(cap_frame)
        cap_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tf_caps_list = tk.Listbox(cap_frame, height=6, 
                                        yscrollcommand=cap_scroll.set)
        self.tf_caps_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cap_scroll.config(command=self.tf_caps_list.yview)
        row += 1
        
        # Save button
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
        
        ttk.Label(filter_frame, text="Trailer:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=3)
        self.rm_trailer = ttk.Combobox(filter_frame, state='readonly', width=25)
        self.rm_trailer.grid(row=row, column=3, sticky=tk.W, padx=5, pady=3)
        row += 1
        
        # Query mode selection
        ttk.Label(filter_frame, text="Query Mode:", font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.rm_query_mode = tk.StringVar(value='date')
        ttk.Radiobutton(filter_frame, text="By Date (show TRL achieved)", 
                       variable=self.rm_query_mode, value='date',
                       command=self.on_rm_query_mode_change).grid(row=row, column=1, sticky=tk.W, padx=5, pady=3)
        ttk.Radiobutton(filter_frame, text="By TRL Level (show dates)", 
                       variable=self.rm_query_mode, value='trl',
                       command=self.on_rm_query_mode_change).grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=3)
        row += 1
        
        # Date query field with calendar picker button
        ttk.Label(filter_frame, text="Query Date:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        date_frame = ttk.Frame(filter_frame)
        date_frame.grid(row=row, column=1, sticky=tk.W, padx=5, pady=3)
        
        self.rm_date = ttk.Entry(date_frame, width=15)
        self.rm_date.pack(side=tk.LEFT, padx=(0, 5))
        self.rm_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ttk.Button(date_frame, text="📅", width=3, command=self.open_calendar_picker).pack(side=tk.LEFT)
        row += 1
        
        # TRL level query field
        ttk.Label(filter_frame, text="Query TRL Level:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
        self.rm_trl = ttk.Combobox(filter_frame, state='readonly', width=25, 
                                    values=['TRL 3', 'TRL 6', 'TRL 9'])
        self.rm_trl.grid(row=row, column=1, sticky=tk.W, padx=5, pady=3)
        self.rm_trl_label = ttk.Label(filter_frame, text="(Select TRL level to query)", font=('TkDefaultFont', 8, 'italic'))
        self.rm_trl_label.grid(row=row, column=1, sticky=tk.E, padx=5, pady=3)
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
        
        # Create horizontal split - left for tables, right for pie chart
        results_paned = ttk.PanedWindow(results_frame, orient=tk.HORIZONTAL)
        results_paned.pack(fill=tk.BOTH, expand=True)
        
        # Left side - tables
        tables_frame = ttk.Frame(results_paned)
        results_paned.add(tables_frame, weight=2)
        
        # Create notebook for different result views
        results_notebook = ttk.Notebook(tables_frame)
        results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Product Features results
        pf_tab = ttk.Frame(results_notebook)
        results_notebook.add(pf_tab, text="Product Features")
        
        pf_scroll = ttk.Scrollbar(pf_tab)
        pf_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.rm_pf_tree = ttk.Treeview(pf_tab,
                                        columns=('Label', 'Name', 'Description', 'Required', 'TRL Achieved'),
                                        show='headings',
                                        yscrollcommand=pf_scroll.set)
        pf_scroll.config(command=self.rm_pf_tree.yview)
        
        self.rm_pf_tree.heading('Label', text='Label')
        self.rm_pf_tree.heading('Name', text='Name')
        self.rm_pf_tree.heading('Description', text='Description')
        self.rm_pf_tree.heading('Required', text='Required')
        self.rm_pf_tree.heading('TRL Achieved', text='TRL Achieved')
        
        self.rm_pf_tree.column('Label', width=120)
        self.rm_pf_tree.column('Name', width=200)
        self.rm_pf_tree.column('Description', width=300)
        self.rm_pf_tree.column('Required', width=80)
        self.rm_pf_tree.column('TRL Achieved', width=120)
        
        self.rm_pf_tree.pack(fill=tk.BOTH, expand=True)
        
        # Capabilities results
        cap_tab = ttk.Frame(results_notebook)
        results_notebook.add(cap_tab, text="Capabilities")
        
        cap_scroll = ttk.Scrollbar(cap_tab)
        cap_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.rm_cap_tree = ttk.Treeview(cap_tab,
                                         columns=('Label', 'Name', 'Description', 'Required', 'TRL Achieved'),
                                         show='headings',
                                         yscrollcommand=cap_scroll.set)
        cap_scroll.config(command=self.rm_cap_tree.yview)
        
        self.rm_cap_tree.heading('Label', text='Label')
        self.rm_cap_tree.heading('Name', text='Name')
        self.rm_cap_tree.heading('Description', text='Description')
        self.rm_cap_tree.heading('Required', text='Required')
        self.rm_cap_tree.heading('TRL Achieved', text='TRL Achieved')
        
        self.rm_cap_tree.column('Label', width=120)
        self.rm_cap_tree.column('Name', width=200)
        self.rm_cap_tree.column('Description', width=300)
        self.rm_cap_tree.column('Required', width=80)
        self.rm_cap_tree.column('TRL Achieved', width=120)
        
        self.rm_cap_tree.pack(fill=tk.BOTH, expand=True)
        
        # Right side - pie chart
        chart_frame = ttk.LabelFrame(results_paned, text="TRL Distribution", padding=5)
        results_paned.add(chart_frame, weight=1)
        
        self.rm_chart_frame = ttk.Frame(chart_frame)
        self.rm_chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Store the results notebook for later reference
        self.rm_results_notebook = results_notebook
        
        # Store query results for pie chart updates
        self.rm_last_pfs = []
        self.rm_last_caps = []
        self.rm_last_query_date = None
        
        # Bind tab change to update pie chart
        results_notebook.bind('<<NotebookTabChanged>>', self.on_rm_tab_changed)
        
        self.load_readiness_filters()
        
        # Initialize query mode fields state
        self.on_rm_query_mode_change()
    
    def create_roadmap_tab(self):
        """Create Roadmap visualization."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Roadmap")
        
        # Controls
        control_frame = ttk.Frame(tab)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="View:").pack(side=tk.LEFT, padx=5)
        self.roadmap_view = ttk.Combobox(control_frame, 
                                         values=['Product Features', 'Capabilities'],
                                         state='readonly',
                                         width=20)
        self.roadmap_view.set('Product Features')
        self.roadmap_view.pack(side=tk.LEFT, padx=5)
        
        # Add filter controls
        ttk.Label(control_frame, text="Platform:").pack(side=tk.LEFT, padx=(20, 5))
        self.roadmap_platform = ttk.Combobox(control_frame, width=15)
        self.roadmap_platform.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="ODD:").pack(side=tk.LEFT, padx=(10, 5))
        self.roadmap_odd = ttk.Combobox(control_frame, width=15)
        self.roadmap_odd.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Environment:").pack(side=tk.LEFT, padx=(10, 5))
        self.roadmap_environment = ttk.Combobox(control_frame, width=15)
        self.roadmap_environment.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Update Roadmap",
                  command=self.update_roadmap).pack(side=tk.LEFT, padx=20)
        
        ttk.Button(control_frame, text="Manage Milestones",
                  command=self.manage_milestones).pack(side=tk.LEFT, padx=5)
        
        # Canvas for matplotlib
        self.roadmap_frame = ttk.Frame(tab)
        self.roadmap_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load filter options
        self.load_roadmap_filters()
        self.update_roadmap()
    
    def create_configurations_tab(self):
        """Create tab for managing configuration options."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Configurations")
        
        # Split into two panes: type selector on left, items on right
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left pane - configuration type selector
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Configuration Types", 
                 font=('TkDefaultFont', 12, 'bold')).pack(pady=10)
        
        # Listbox for configuration types
        type_frame = ttk.Frame(left_frame)
        type_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        type_scroll = ttk.Scrollbar(type_frame)
        type_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.config_type_listbox = tk.Listbox(type_frame, yscrollcommand=type_scroll.set,
                                              font=('TkDefaultFont', 10))
        type_scroll.config(command=self.config_type_listbox.yview)
        self.config_type_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configuration types
        self.config_types = [
            ('Platform', 'Vehicle platforms supported by the system'),
            ('ODD', 'Operational Design Domains'),
            ('Environment', 'Deployment environments'),
            ('Trailer', 'Trailer types and configurations'),
            ('TRL', 'Technology Readiness Levels')
        ]
        
        for config_type, description in self.config_types:
            self.config_type_listbox.insert(tk.END, config_type)
        
        self.config_type_listbox.bind('<<ListboxSelect>>', self.on_config_type_select)
        
        # Right pane - configuration items
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        
        # Title and description
        self.config_title_label = ttk.Label(right_frame, text="Select a configuration type", 
                                           font=('TkDefaultFont', 12, 'bold'))
        self.config_title_label.pack(pady=(10, 0))
        
        self.config_desc_label = ttk.Label(right_frame, text="", 
                                          font=('TkDefaultFont', 9, 'italic'),
                                          foreground='#666666')
        self.config_desc_label.pack(pady=(0, 10))
        
        # Toolbar
        toolbar = ttk.Frame(right_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Add New", command=self.add_configuration).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Selected", command=self.edit_configuration).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Selected", command=self.delete_configuration).pack(side=tk.LEFT, padx=2)
        
        # Configuration items list
        list_frame = ttk.Frame(right_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.config_tree = ttk.Treeview(list_frame,
                                        columns=('Code', 'Description'),
                                        show='tree headings',
                                        yscrollcommand=scroll.set)
        scroll.config(command=self.config_tree.yview)
        
        self.config_tree.heading('Code', text='Code')
        self.config_tree.heading('Description', text='Description')
        
        self.config_tree.column('#0', width=0, stretch=False)
        self.config_tree.column('Code', width=150)
        self.config_tree.column('Description', width=400)
        
        self.config_tree.pack(fill=tk.BOTH, expand=True)
        
        # Note at bottom
        note_label = ttk.Label(right_frame, 
                              text="Configuration values are used throughout the system for filtering and categorization.",
                              font=('TkDefaultFont', 9),
                              foreground='#333333')
        note_label.pack(pady=5)
        
        # Select first type by default
        self.config_type_listbox.selection_set(0)
        self.on_config_type_select(None)
    
    def on_config_type_select(self, event):
        """Handle configuration type selection."""
        selection = self.config_type_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        config_type, description = self.config_types[idx]
        
        self.config_title_label.config(text=config_type + 's')
        self.config_desc_label.config(text=description)
        
        # Load configurations of this type
        self.load_configurations(config_type)
    
    def load_configurations(self, config_type):
        """Load configurations from database for the selected type."""
        # Clear existing items
        for item in self.config_tree.get_children():
            self.config_tree.delete(item)
        
        # Get configurations from database
        configs = self.db.get_configurations(config_type)
        
        for config in configs:
            self.config_tree.insert('', tk.END, iid=config['id'],
                                   values=(config['code'], config['description']))
    
    def add_configuration(self):
        """Add a new configuration."""
        selection = self.config_type_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Type Selected", "Please select a configuration type first.")
            return
        
        idx = selection[0]
        config_type, _ = self.config_types[idx]
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Add {config_type}")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Code:", font=('TkDefaultFont', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        code_entry = ttk.Entry(form_frame, width=40)
        code_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Description:", font=('TkDefaultFont', 10, 'bold')).grid(row=1, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(form_frame, width=40, height=5, wrap=tk.WORD)
        desc_text.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(dialog, padding=(20, 0, 20, 20))
        button_frame.pack(fill=tk.X)
        
        def save():
            code = code_entry.get().strip()
            description = desc_text.get('1.0', tk.END).strip()
            
            if not code or not description:
                messagebox.showwarning("Missing Information", "Please fill in all fields.")
                return
            
            try:
                self.db.add_configuration({
                    'config_type': config_type,
                    'code': code,
                    'description': description
                })
                self.load_configurations(config_type)
                self.refresh_all_config_dropdowns()
                dialog.destroy()
                messagebox.showinfo("Success", f"{config_type} added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add {config_type}: {str(e)}")
        
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
        
        code_entry.focus()
    
    def edit_configuration(self):
        """Edit the selected configuration."""
        selection = self.config_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a configuration to edit.")
            return
        
        config_id = int(selection[0])
        config = self.db.get_configuration_by_id(config_id)
        
        if not config:
            messagebox.showerror("Error", "Configuration not found.")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit {config['config_type']}")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Code:", font=('TkDefaultFont', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        code_entry = ttk.Entry(form_frame, width=40)
        code_entry.insert(0, config['code'])
        code_entry.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        ttk.Label(form_frame, text="Description:", font=('TkDefaultFont', 10, 'bold')).grid(row=1, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(form_frame, width=40, height=5, wrap=tk.WORD)
        desc_text.insert('1.0', config['description'])
        desc_text.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(dialog, padding=(20, 0, 20, 20))
        button_frame.pack(fill=tk.X)
        
        def save():
            code = code_entry.get().strip()
            description = desc_text.get('1.0', tk.END).strip()
            
            if not code or not description:
                messagebox.showwarning("Missing Information", "Please fill in all fields.")
                return
            
            try:
                self.db.update_configuration(config_id, {
                    'config_type': config['config_type'],
                    'code': code,
                    'description': description
                })
                self.load_configurations(config['config_type'])
                self.refresh_all_config_dropdowns()
                dialog.destroy()
                messagebox.showinfo("Success", f"{config['config_type']} updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update {config['config_type']}: {str(e)}")
        
        ttk.Button(button_frame, text="Save", command=save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
        
        code_entry.focus()
    
    def delete_configuration(self):
        """Delete the selected configuration."""
        selection = self.config_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a configuration to delete.")
            return
        
        config_id = int(selection[0])
        config = self.db.get_configuration_by_id(config_id)
        
        if not config:
            messagebox.showerror("Error", "Configuration not found.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{config['code']}'?\n\n"
                              f"This action cannot be undone."):
            try:
                self.db.delete_configuration(config_id)
                self.load_configurations(config['config_type'])
                self.refresh_all_config_dropdowns()
                messagebox.showinfo("Success", f"{config['config_type']} deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete {config['config_type']}: {str(e)}")
    
    # Helper methods
    def get_config_codes(self, config_type):
        """Get configuration codes for a given type."""
        configs = self.db.get_configurations(config_type)
        return [c['code'] for c in configs]
    
    def refresh_all_config_dropdowns(self):
        """Refresh all configuration-based dropdowns across all tabs."""
        # Product Features tab
        platforms = [''] + self.get_config_codes('Platform')
        odds = [''] + self.get_config_codes('ODD')
        environments = [''] + self.get_config_codes('Environment')
        trailers = [''] + self.get_config_codes('Trailer')
        
        # Product Features filter
        self.pf_platform_filter['values'] = platforms
        
        # Product Features form
        self.pf_form['platform']['values'] = platforms
        self.pf_form['odd']['values'] = odds
        self.pf_form['environment']['values'] = environments
        self.pf_form['trailer']['values'] = trailers
        
        # Capabilities form
        self.cap_form['platform']['values'] = platforms
        
        # Technical Functions form
        self.tf_form['platform']['values'] = platforms
        
        # Readiness Matrix filters
        self.rm_platform['values'] = platforms
        self.rm_odd['values'] = odds
        self.rm_environment['values'] = environments
        self.rm_trailer['values'] = trailers
        
        # Roadmap filters
        self.roadmap_platform['values'] = platforms
        self.roadmap_odd['values'] = odds
        self.roadmap_environment['values'] = environments
    
    # Data loading methods
    def load_roadmap_filters(self):
        """Load filter options for Roadmap."""
        platforms = [''] + self.get_config_codes('Platform')
        odds = [''] + self.get_config_codes('ODD')
        environments = [''] + self.get_config_codes('Environment')
        
        self.roadmap_platform['values'] = platforms
        self.roadmap_odd['values'] = odds
        self.roadmap_environment['values'] = environments
    
    def load_pf_filters(self):
        """Load filter options for Product Features."""
        platforms = [''] + self.get_config_codes('Platform')
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
                                      feature.get('swimlane', ''),
                                      feature['platform'],
                                      feature['start_date'],
                                      feature['trl3_date'] or '',
                                      feature['trl6_date'] or '',
                                      feature['trl9_date'] or ''))
    
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
                                values=(cap['label'], 
                                       cap['name'], 
                                       cap['swimlane'],
                                       cap['start_date'] or '',
                                       cap['trl3_date'] or '',
                                       cap['trl6_date'] or '',
                                       cap['trl9_date'] or ''))
    
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
        
        # Load linked Technical Functions
        self.cap_tfs_list.delete(0, tk.END)
        tfs = self.db.get_cap_technical_functions(self.current_cap_id)
        for tf in tfs:
            self.cap_tfs_list.insert(tk.END, f"{tf['label']}: {tf['name']}")
        
        # Load linked Product Features
        self.cap_pfs_list.delete(0, tk.END)
        pfs = self.db.get_cap_product_features(self.current_cap_id)
        for pf in pfs:
            self.cap_pfs_list.insert(tk.END, f"{pf['label']}: {pf['name']}")
    
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
    
    def add_cap_tf(self):
        """Add a Technical Function to the current Capability."""
        if not self.current_cap_id:
            messagebox.showwarning("No Selection", "Please select a capability first.")
            return
        
        # Create dialog to select TF
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Technical Function")
        dialog.geometry("600x400")
        
        ttk.Label(dialog, text="Select Technical Function to add:", 
                 font=('TkDefaultFont', 10, 'bold')).pack(padx=10, pady=10)
        
        # List of available TFs
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tf_listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set)
        tf_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=tf_listbox.yview)
        
        # Load all TFs
        all_tfs = self.db.get_technical_functions()
        linked_tfs = self.db.get_cap_technical_functions(self.current_cap_id)
        linked_tf_ids = {tf['id'] for tf in linked_tfs}
        
        tf_map = {}
        for tf in all_tfs:
            if tf['id'] not in linked_tf_ids:
                display_text = f"{tf['label']}: {tf['name']}"
                tf_listbox.insert(tk.END, display_text)
                tf_map[display_text] = tf['id']
        
        def add_selected():
            selection = tf_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a technical function.")
                return
            
            selected_text = tf_listbox.get(selection[0])
            tf_id = tf_map[selected_text]
            
            self.db.link_cap_tf(self.current_cap_id, tf_id)
            
            # Refresh the list
            self.cap_tfs_list.delete(0, tk.END)
            tfs = self.db.get_cap_technical_functions(self.current_cap_id)
            for tf in tfs:
                self.cap_tfs_list.insert(tk.END, f"{tf['label']}: {tf['name']}")
            
            dialog.destroy()
            messagebox.showinfo("Success", "Technical Function added!")
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=add_selected).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def remove_cap_tf(self):
        """Remove a Technical Function from the current Capability."""
        if not self.current_cap_id:
            messagebox.showwarning("No Selection", "Please select a capability first.")
            return
        
        selection = self.cap_tfs_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a technical function to remove.")
            return
        
        selected_text = self.cap_tfs_list.get(selection[0])
        tf_label = selected_text.split(':')[0].strip()
        
        # Find the TF by label
        tfs = self.db.get_cap_technical_functions(self.current_cap_id)
        tf_to_remove = None
        for tf in tfs:
            if tf['label'] == tf_label:
                tf_to_remove = tf
                break
        
        if tf_to_remove:
            if messagebox.askyesno("Confirm", f"Remove '{selected_text}'?"):
                self.db.unlink_cap_tf(self.current_cap_id, tf_to_remove['id'])
                self.cap_tfs_list.delete(selection[0])
                messagebox.showinfo("Success", "Technical Function removed!")
    
    def add_cap_pf(self):
        """Add a Product Feature to the current Capability."""
        if not self.current_cap_id:
            messagebox.showwarning("No Selection", "Please select a capability first.")
            return
        
        # Create dialog to select PF
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Product Feature")
        dialog.geometry("600x400")
        
        ttk.Label(dialog, text="Select Product Feature to add:", 
                 font=('TkDefaultFont', 10, 'bold')).pack(padx=10, pady=10)
        
        # List of available PFs
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scroll = ttk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        pf_listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set)
        pf_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=pf_listbox.yview)
        
        # Load all PFs
        all_pfs = self.db.get_product_features()
        linked_pfs = self.db.get_cap_product_features(self.current_cap_id)
        linked_pf_ids = {pf['id'] for pf in linked_pfs}
        
        pf_map = {}
        for pf in all_pfs:
            if pf['id'] not in linked_pf_ids:
                display_text = f"{pf['label']}: {pf['name']}"
                pf_listbox.insert(tk.END, display_text)
                pf_map[display_text] = pf['id']
        
        def add_selected():
            selection = pf_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a product feature.")
                return
            
            selected_text = pf_listbox.get(selection[0])
            pf_id = pf_map[selected_text]
            
            self.db.link_pf_capability(pf_id, self.current_cap_id)
            
            # Refresh the list
            self.cap_pfs_list.delete(0, tk.END)
            pfs = self.db.get_cap_product_features(self.current_cap_id)
            for pf in pfs:
                self.cap_pfs_list.insert(tk.END, f"{pf['label']}: {pf['name']}")
            
            dialog.destroy()
            messagebox.showinfo("Success", "Product Feature added!")
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Add", command=add_selected).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def remove_cap_pf(self):
        """Remove a Product Feature from the current Capability."""
        if not self.current_cap_id:
            messagebox.showwarning("No Selection", "Please select a capability first.")
            return
        
        selection = self.cap_pfs_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a product feature to remove.")
            return
        
        selected_text = self.cap_pfs_list.get(selection[0])
        pf_label = selected_text.split(':')[0].strip()
        
        # Find the PF by label
        pfs = self.db.get_cap_product_features(self.current_cap_id)
        pf_to_remove = None
        for pf in pfs:
            if pf['label'] == pf_label:
                pf_to_remove = pf
                break
        
        if pf_to_remove:
            if messagebox.askyesno("Confirm", f"Remove '{selected_text}'?"):
                self.db.unlink_pf_capability(pf_to_remove['id'], self.current_cap_id)
                self.cap_pfs_list.delete(selection[0])
                messagebox.showinfo("Success", "Product Feature removed!")
    
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
        
        # Load linked Capabilities
        self.tf_caps_list.delete(0, tk.END)
        caps = self.db.get_tf_capabilities(self.current_tf_id)
        for cap in caps:
            self.tf_caps_list.insert(tk.END, f"{cap['label']}: {cap['name']}")
    
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
        platforms = [''] + self.get_config_codes('Platform')
        self.rm_platform['values'] = platforms
        
        odds = [''] + self.get_config_codes('ODD')
        self.rm_odd['values'] = odds
        
        envs = [''] + self.get_config_codes('Environment')
        self.rm_environment['values'] = envs
        
        trailers = [''] + self.get_config_codes('Trailer')
        self.rm_trailer['values'] = trailers
    
    def clear_readiness_filters(self):
        """Clear Readiness Matrix filters."""
        self.rm_platform.set('')
        self.rm_odd.set('')
        self.rm_environment.set('')
        self.rm_trailer.set('')
        self.rm_date.delete(0, tk.END)
        self.rm_trl.set('')
        self.apply_readiness_query()
    
    def open_calendar_picker(self):
        """Open a calendar dialog to select a date."""
        # Create a new top-level window
        cal_window = tk.Toplevel(self.root)
        cal_window.title("Select Date")
        cal_window.geometry("300x300")
        cal_window.resizable(False, False)
        
        # Get current date from entry field or use today
        try:
            current_date = datetime.strptime(self.rm_date.get(), '%Y-%m-%d').date()
        except:
            current_date = datetime.now().date()
        
        # Create calendar widget with black text and light background
        cal = Calendar(cal_window, selectmode='day', 
                      year=current_date.year, 
                      month=current_date.month, 
                      day=current_date.day,
                      date_pattern='yyyy-mm-dd',
                      foreground='black',
                      background='white',
                      headersforeground='black',
                      headersbackground='lightgray',
                      normalforeground='black',
                      normalbackground='white',
                      weekendforeground='black',
                      weekendbackground='white')
        cal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        def select_date():
            """Set the selected date and close the window."""
            selected = cal.get_date()
            self.rm_date.delete(0, tk.END)
            self.rm_date.insert(0, selected)
            cal_window.destroy()
        
        # Buttons
        btn_frame = ttk.Frame(cal_window)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Select", command=select_date).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=cal_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Make the window modal
        cal_window.transient(self.root)
        cal_window.grab_set()
    
    def on_rm_query_mode_change(self):
        """Handle query mode change to enable/disable appropriate fields."""
        mode = self.rm_query_mode.get()
        if mode == 'date':
            # Enable date field, disable TRL field
            self.rm_date.config(state='normal')
            self.rm_trl.config(state='disabled')
        else:  # mode == 'trl'
            # Set date field to readonly, enable TRL field
            self.rm_date.config(state='readonly')
            self.rm_trl.config(state='readonly')
    
    def apply_readiness_query(self):
        """Apply Readiness Matrix query."""
        from datetime import datetime
        
        # Clear current results
        for item in self.rm_pf_tree.get_children():
            self.rm_pf_tree.delete(item)
        for item in self.rm_cap_tree.get_children():
            self.rm_cap_tree.delete(item)
        
        # Determine query mode
        query_mode = self.rm_query_mode.get()
        
        # Update column headers based on mode
        if query_mode == 'date':
            # Date mode: show TRL achieved
            self.rm_pf_tree.heading('TRL Achieved', text='TRL Achieved')
            self.rm_cap_tree.heading('TRL Achieved', text='TRL Achieved')
            
            # Get query date from entry field
            query_date_str = self.rm_date.get().strip()
            query_date = None
            if query_date_str:
                try:
                    query_date = datetime.strptime(query_date_str, '%Y-%m-%d').date()
                except ValueError:
                    messagebox.showwarning("Invalid Date", "Please enter date in YYYY-MM-DD format")
                    return
        else:  # TRL mode
            # TRL mode: show dates when TRL is achieved
            self.rm_pf_tree.heading('TRL Achieved', text='Date Achieved')
            self.rm_cap_tree.heading('TRL Achieved', text='Date Achieved')
            
            # Get query TRL level
            query_trl = self.rm_trl.get().strip()
            if not query_trl:
                messagebox.showwarning("No TRL Selected", "Please select a TRL level to query")
                return
        
        # Build filters
        pf_filters = {}
        if self.rm_platform.get():
            pf_filters['platform'] = self.rm_platform.get()
        if self.rm_odd.get():
            pf_filters['odd'] = self.rm_odd.get()
        if self.rm_environment.get():
            pf_filters['environment'] = self.rm_environment.get()
        if self.rm_trailer.get():
            pf_filters['trailer'] = self.rm_trailer.get()
        
        cap_filters = {}
        if self.rm_platform.get():
            cap_filters['platform'] = self.rm_platform.get()
        if self.rm_odd.get():
            cap_filters['odd'] = self.rm_odd.get()
        if self.rm_environment.get():
            cap_filters['environment'] = self.rm_environment.get()
        if self.rm_trailer.get():
            cap_filters['trailer'] = self.rm_trailer.get()
        
        # Helper functions
        def calculate_trl_achieved(trl3_date, trl6_date, trl9_date, query_date):
            """Calculate TRL achieved by a given date."""
            if not query_date:
                return 'N/A'
            
            # Parse dates
            trl3 = datetime.strptime(trl3_date, '%Y-%m-%d').date() if trl3_date else None
            trl6 = datetime.strptime(trl6_date, '%Y-%m-%d').date() if trl6_date else None
            trl9 = datetime.strptime(trl9_date, '%Y-%m-%d').date() if trl9_date else None
            
            # Determine TRL achieved by query date
            if trl9 and query_date >= trl9:
                return 'TRL 9'
            elif trl6 and query_date >= trl6:
                return 'TRL 6'
            elif trl3 and query_date >= trl3:
                return 'TRL 3'
            else:
                return 'Not Started'
        
        def get_trl_date(trl3_date, trl6_date, trl9_date, query_trl):
            """Get the date when a specific TRL level is achieved."""
            if query_trl == 'TRL 3':
                return trl3_date if trl3_date else 'Not Planned'
            elif query_trl == 'TRL 6':
                return trl6_date if trl6_date else 'Not Planned'
            elif query_trl == 'TRL 9':
                return trl9_date if trl9_date else 'Not Planned'
            return 'N/A'
        
        # Load Product Features
        pfs = self.db.get_product_features(pf_filters)
        print(f"DEBUG: Found {len(pfs)} product features matching filters: {pf_filters}")
        
        for pf in pfs:
            try:
                # Determine if required (using when_date field)
                required = 'Yes' if pf.get('when_date') else 'N/A'
                
                # Get description from details field
                description = pf.get('details', '')[:100] + '...' if pf.get('details') and len(pf.get('details', '')) > 100 else pf.get('details', '')
                
                # Add color indicators to text
                # Required: 🟢 = green (Yes), 🔴 = red (No), ⚪ = grey (N/A)
                if required == 'Yes':
                    required_display = '🟢 Yes'
                elif required == 'No':
                    required_display = '🔴 No'
                else:
                    required_display = '⚪ N/A'
                
                # Calculate result based on query mode
                if query_mode == 'date':
                    # Date mode: show TRL achieved
                    trl_achieved = calculate_trl_achieved(
                        pf.get('trl3_date'), 
                        pf.get('trl6_date'), 
                        pf.get('trl9_date'),
                        query_date
                    )
                    
                    # TRL: ⚪ = grey (Not Started), 🔴 = red (TRL 3), 🟠 = amber (TRL 6), 🟢 = green (TRL 9)
                    if trl_achieved == 'TRL 9':
                        result_display = '🟢 TRL 9'
                    elif trl_achieved == 'TRL 6':
                        result_display = '🟠 TRL 6'
                    elif trl_achieved == 'TRL 3':
                        result_display = '🔴 TRL 3'
                    else:
                        result_display = '⚪ Not Started'
                else:
                    # TRL mode: show date when TRL is achieved
                    trl_date = get_trl_date(
                        pf.get('trl3_date'),
                        pf.get('trl6_date'),
                        pf.get('trl9_date'),
                        query_trl
                    )
                    result_display = trl_date if trl_date != 'Not Planned' else '⚪ Not Planned'
                
                print(f"DEBUG: Inserting PF {pf['label']}: {pf['name'][:30]}")
                self.rm_pf_tree.insert('', tk.END,
                                       values=(pf['label'], pf['name'], description, required_display, result_display))
            except Exception as e:
                print(f"Error processing product feature {pf.get('label', 'UNKNOWN')}: {e}")
                import traceback
                traceback.print_exc()
                # Still insert the row with basic info
                self.rm_pf_tree.insert('', tk.END,
                                       values=(pf.get('label', '?'), pf.get('name', '?'), 
                                              pf.get('details', '')[:50] if pf.get('details') else '', 
                                              'N/A', 'Error'))
        
        print(f"DEBUG: Tree now has {len(self.rm_pf_tree.get_children())} items")
        
        # Load Capabilities
        # Environment filter now handles CFG-ENV-2.1 including CFG-ENV-1.1 at database level
        caps = self.db.get_capabilities(cap_filters)
        print(f"DEBUG: Found {len(caps)} capabilities matching filters: {cap_filters}")
        for cap in caps:
            try:
                # Determine if required (using when_date field)
                required = 'Yes' if cap.get('when_date') else 'N/A'
                
                # Get description from details field
                description = cap.get('details', '')[:100] + '...' if cap.get('details') and len(cap.get('details', '')) > 100 else cap.get('details', '')
                
                # Add color indicators to text
                # Required: 🟢 = green (Yes), 🔴 = red (No), ⚪ = grey (N/A)
                if required == 'Yes':
                    required_display = '🟢 Yes'
                elif required == 'No':
                    required_display = '🔴 No'
                else:
                    required_display = '⚪ N/A'
                
                # Calculate result based on query mode
                if query_mode == 'date':
                    # Date mode: show TRL achieved
                    trl_achieved = calculate_trl_achieved(
                        cap.get('trl3_date'), 
                        cap.get('trl6_date'), 
                        cap.get('trl9_date'),
                        query_date
                    )
                    
                    # TRL: ⚪ = grey (Not Started), 🔴 = red (TRL 3), 🟠 = amber (TRL 6), 🟢 = green (TRL 9)
                    if trl_achieved == 'TRL 9':
                        result_display = '🟢 TRL 9'
                    elif trl_achieved == 'TRL 6':
                        result_display = '🟠 TRL 6'
                    elif trl_achieved == 'TRL 3':
                        result_display = '🔴 TRL 3'
                    else:
                        result_display = '⚪ Not Started'
                else:
                    # TRL mode: show date when TRL is achieved
                    trl_date = get_trl_date(
                        cap.get('trl3_date'),
                        cap.get('trl6_date'),
                        cap.get('trl9_date'),
                        query_trl
                    )
                    result_display = trl_date if trl_date != 'Not Planned' else '⚪ Not Planned'
                
                self.rm_cap_tree.insert('', tk.END,
                                        values=(cap['label'], cap['name'], description, required_display, result_display))
                
                self.rm_cap_tree.insert('', tk.END,
                                        values=(cap['label'], cap['name'], description, required_display, result_display))
            except Exception as e:
                print(f"Error processing capability {cap.get('label', 'UNKNOWN')}: {e}")
                # Still insert the row with basic info
                self.rm_cap_tree.insert('', tk.END,
                                        values=(cap.get('label', '?'), cap.get('name', '?'), 
                                               cap.get('details', '')[:50] if cap.get('details') else '', 
                                               'N/A', 'Error'))
        
        # Store results for pie chart updates (only in date mode)
        if query_mode == 'date':
            self.rm_last_pfs = pfs
            self.rm_last_caps = caps
            self.rm_last_query_date = query_date
            
            # Update pie chart based on current tab
            self.update_readiness_pie_chart(pfs, caps, query_date)
        else:
            # In TRL mode, pie chart doesn't make sense, so clear it
            for widget in self.rm_chart_frame.winfo_children():
                widget.destroy()
            label = tk.Label(self.rm_chart_frame, text="Pie chart only available in Date mode", 
                           font=('TkDefaultFont', 10))
            label.pack(expand=True)
    
    def on_rm_tab_changed(self, event):
        """Handle readiness matrix tab change to update pie chart."""
        if hasattr(self, 'rm_last_pfs'):
            self.update_readiness_pie_chart(
                self.rm_last_pfs, 
                self.rm_last_caps, 
                self.rm_last_query_date
            )
    
    def update_readiness_pie_chart(self, pfs, caps, query_date):
        """Update the TRL distribution pie chart."""
        # Clear previous chart
        for widget in self.rm_chart_frame.winfo_children():
            widget.destroy()
        
        # Get current tab (Product Features or Capabilities)
        current_tab_index = self.rm_results_notebook.index(self.rm_results_notebook.select())
        
        # Helper function to calculate TRL achieved
        def calculate_trl_achieved(trl3_date, trl6_date, trl9_date, query_date):
            if not query_date:
                return 'Not Started'
            
            # Parse dates
            trl3 = datetime.strptime(trl3_date, '%Y-%m-%d').date() if trl3_date else None
            trl6 = datetime.strptime(trl6_date, '%Y-%m-%d').date() if trl6_date else None
            trl9 = datetime.strptime(trl9_date, '%Y-%m-%d').date() if trl9_date else None
            
            # Determine TRL achieved by query date
            if trl9 and query_date >= trl9:
                return 'TRL 9'
            elif trl6 and query_date >= trl6:
                return 'TRL 6'
            elif trl3 and query_date >= trl3:
                return 'TRL 3'
            else:
                return 'Not Started'
        
        # Collect TRL data based on current tab
        trl_counts = {'Not Started': 0, 'TRL 3': 0, 'TRL 6': 0, 'TRL 9': 0}
        
        if current_tab_index == 0:  # Product Features tab
            items = pfs
            title = "Product Features TRL Distribution"
        else:  # Capabilities tab
            items = caps
            title = "Capabilities TRL Distribution"
        
        # Count TRL levels
        for item in items:
            trl = calculate_trl_achieved(
                item.get('trl3_date'),
                item.get('trl6_date'),
                item.get('trl9_date'),
                query_date
            )
            trl_counts[trl] += 1
        
        # Filter out zero counts
        labels = []
        sizes = []
        colors = []
        color_map = {
            'Not Started': '#D3D3D3',  # Grey
            'TRL 3': '#DC3545',        # Red
            'TRL 6': '#FFC107',        # Amber
            'TRL 9': '#28A745'         # Green
        }
        
        for trl_level in ['Not Started', 'TRL 3', 'TRL 6', 'TRL 9']:
            if trl_counts[trl_level] > 0:
                labels.append(f'{trl_level}\n({trl_counts[trl_level]})')
                sizes.append(trl_counts[trl_level])
                colors.append(color_map[trl_level])
        
        if not sizes:
            # No data to display
            label = tk.Label(self.rm_chart_frame, text="No data to display", 
                           font=('TkDefaultFont', 10))
            label.pack(expand=True)
            return
        
        # Create pie chart
        fig = Figure(figsize=(5, 5), dpi=80)
        ax = fig.add_subplot(111)
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                           autopct='%1.1f%%', startangle=90,
                                           textprops={'fontsize': 9})
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.rm_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
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
                writer.writerow(['Label', 'Name', 'Description', 'Required', 'TRL Achieved'])
                
                for item in self.rm_pf_tree.get_children():
                    values = self.rm_pf_tree.item(item)['values']
                    writer.writerow(values)
                
                writer.writerow([])
                
                # Write Capabilities
                writer.writerow(['Capabilities'])
                writer.writerow(['Label', 'Name', 'Description', 'Required', 'TRL Achieved'])
                
                for item in self.rm_cap_tree.get_children():
                    values = self.rm_cap_tree.item(item)['values']
                    writer.writerow(values)
            
            messagebox.showinfo("Success", f"Results exported to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def add_milestone(self):
        """Add a new milestone to the roadmap."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Milestone")
        dialog.geometry("450x250")
        dialog.resizable(False, False)
        
        # Create form
        ttk.Label(dialog, text="Milestone Name:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        
        ttk.Label(dialog, text="Description:", font=('TkDefaultFont', 9, 'bold')).grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
        desc_text = scrolledtext.ScrolledText(dialog, width=40, height=5)
        desc_text.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        
        ttk.Label(dialog, text="Date:", font=('TkDefaultFont', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        date_frame = ttk.Frame(dialog)
        date_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        
        date_entry = ttk.Entry(date_frame, width=15)
        date_entry.pack(side=tk.LEFT, padx=(0, 5))
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def open_milestone_calendar():
            """Open calendar picker for milestone date."""
            cal_window = tk.Toplevel(dialog)
            cal_window.title("Select Date")
            cal_window.geometry("300x300")
            cal_window.resizable(False, False)
            
            try:
                current_date = datetime.strptime(date_entry.get(), '%Y-%m-%d').date()
            except:
                current_date = datetime.now().date()
            
            cal = Calendar(cal_window, selectmode='day', 
                          year=current_date.year, 
                          month=current_date.month, 
                          day=current_date.day,
                          date_pattern='yyyy-mm-dd',
                          foreground='black',
                          background='white',
                          headersforeground='black',
                          headersbackground='lightgray',
                          normalforeground='black',
                          normalbackground='white',
                          weekendforeground='black',
                          weekendbackground='white')
            cal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            def select_date():
                selected = cal.get_date()
                date_entry.delete(0, tk.END)
                date_entry.insert(0, selected)
                cal_window.destroy()
            
            btn_frame = ttk.Frame(cal_window)
            btn_frame.pack(pady=5)
            ttk.Button(btn_frame, text="Select", command=select_date).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Cancel", command=cal_window.destroy).pack(side=tk.LEFT, padx=5)
            
            cal_window.transient(dialog)
            cal_window.grab_set()
        
        ttk.Button(date_frame, text="📅", width=3, command=open_milestone_calendar).pack(side=tk.LEFT)
        
        def save_milestone():
            """Save the milestone."""
            name = name_entry.get().strip()
            description = desc_text.get('1.0', tk.END).strip()
            date_str = date_entry.get().strip()
            
            if not name:
                messagebox.showwarning("Missing Data", "Milestone name is required!")
                return
            
            if not date_str:
                messagebox.showwarning("Missing Data", "Date is required!")
                return
            
            # Validate date
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showwarning("Invalid Date", "Please enter date in YYYY-MM-DD format")
                return
            
            try:
                self.db.add_milestone({
                    'name': name,
                    'description': description,
                    'date': date_str
                })
                messagebox.showinfo("Success", "Milestone added successfully!")
                dialog.destroy()
                self.update_roadmap()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add milestone: {str(e)}")
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Save", command=save_milestone).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
    
    def manage_milestones(self):
        """Manage existing milestones - view, edit, and delete."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Milestones")
        dialog.geometry("700x400")
        
        # Create frame for list
        list_frame = ttk.LabelFrame(dialog, text="Existing Milestones", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview to display milestones
        columns = ('name', 'date', 'description')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        tree.heading('name', text='Milestone Name')
        tree.heading('date', text='Date')
        tree.heading('description', text='Description')
        
        tree.column('name', width=200)
        tree.column('date', width=100)
        tree.column('description', width=350)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load milestones
        def load_milestones():
            """Load milestones into the tree."""
            for item in tree.get_children():
                tree.delete(item)
            
            milestones = self.db.get_milestones()
            for milestone in milestones:
                desc = milestone.get('description', '')
                desc_short = desc[:50] + '...' if len(desc) > 50 else desc
                tree.insert('', tk.END, iid=milestone['id'],
                           values=(milestone['name'], milestone['date'], desc_short))
        
        load_milestones()
        
        # Buttons frame
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def delete_selected():
            """Delete the selected milestone."""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a milestone to delete.")
                return
            
            milestone_id = int(selection[0])
            milestone = self.db.get_milestone_by_id(milestone_id)
            
            if messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete milestone '{milestone['name']}'?"):
                try:
                    self.db.delete_milestone(milestone_id)
                    messagebox.showinfo("Success", "Milestone deleted successfully!")
                    load_milestones()
                    self.update_roadmap()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete milestone: {str(e)}")
        
        def view_selected():
            """View details of selected milestone."""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a milestone to view.")
                return
            
            milestone_id = int(selection[0])
            milestone = self.db.get_milestone_by_id(milestone_id)
            
            # Create detail dialog
            detail_dialog = tk.Toplevel(dialog)
            detail_dialog.title("Milestone Details")
            detail_dialog.geometry("450x300")
            
            ttk.Label(detail_dialog, text="Name:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
            ttk.Label(detail_dialog, text=milestone['name']).grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
            
            ttk.Label(detail_dialog, text="Date:", font=('TkDefaultFont', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
            ttk.Label(detail_dialog, text=milestone['date']).grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
            
            ttk.Label(detail_dialog, text="Description:", font=('TkDefaultFont', 9, 'bold')).grid(row=2, column=0, sticky=tk.NW, padx=10, pady=10)
            desc_text = scrolledtext.ScrolledText(detail_dialog, width=40, height=8, wrap=tk.WORD)
            desc_text.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
            desc_text.insert('1.0', milestone.get('description', ''))
            desc_text.config(state='disabled')
            
            ttk.Button(detail_dialog, text="Close", command=detail_dialog.destroy).grid(row=3, column=1, sticky=tk.E, padx=10, pady=10)
            
            detail_dialog.transient(dialog)
        
        def add_new_milestone():
            """Add a new milestone from within the manage dialog."""
            add_dialog = tk.Toplevel(dialog)
            add_dialog.title("Add Milestone")
            add_dialog.geometry("450x250")
            add_dialog.resizable(False, False)
            
            # Create form
            ttk.Label(add_dialog, text="Milestone Name:", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
            name_entry = ttk.Entry(add_dialog, width=40)
            name_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
            
            ttk.Label(add_dialog, text="Description:", font=('TkDefaultFont', 9, 'bold')).grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
            desc_text = scrolledtext.ScrolledText(add_dialog, width=40, height=5)
            desc_text.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
            
            ttk.Label(add_dialog, text="Date:", font=('TkDefaultFont', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
            date_frame = ttk.Frame(add_dialog)
            date_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
            
            date_entry = ttk.Entry(date_frame, width=15)
            date_entry.pack(side=tk.LEFT, padx=(0, 5))
            date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
            
            def open_milestone_calendar():
                """Open calendar picker for milestone date."""
                cal_window = tk.Toplevel(add_dialog)
                cal_window.title("Select Date")
                cal_window.geometry("300x300")
                cal_window.resizable(False, False)
                
                try:
                    current_date = datetime.strptime(date_entry.get(), '%Y-%m-%d').date()
                except:
                    current_date = datetime.now().date()
                
                cal = Calendar(cal_window, selectmode='day', 
                              year=current_date.year, 
                              month=current_date.month, 
                              day=current_date.day,
                              date_pattern='yyyy-mm-dd',
                              foreground='black',
                              background='white',
                              headersforeground='black',
                              headersbackground='lightgray',
                              normalforeground='black',
                              normalbackground='white',
                              weekendforeground='black',
                              weekendbackground='white')
                cal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                
                def select_date():
                    selected = cal.get_date()
                    date_entry.delete(0, tk.END)
                    date_entry.insert(0, selected)
                    cal_window.destroy()
                
                btn_frame_cal = ttk.Frame(cal_window)
                btn_frame_cal.pack(pady=5)
                ttk.Button(btn_frame_cal, text="Select", command=select_date).pack(side=tk.LEFT, padx=5)
                ttk.Button(btn_frame_cal, text="Cancel", command=cal_window.destroy).pack(side=tk.LEFT, padx=5)
                
                cal_window.transient(add_dialog)
                cal_window.grab_set()
            
            ttk.Button(date_frame, text="📅", width=3, command=open_milestone_calendar).pack(side=tk.LEFT)
            
            def save_new_milestone():
                """Save the new milestone."""
                name = name_entry.get().strip()
                description = desc_text.get('1.0', tk.END).strip()
                date_str = date_entry.get().strip()
                
                if not name:
                    messagebox.showwarning("Missing Data", "Milestone name is required!")
                    return
                
                if not date_str:
                    messagebox.showwarning("Missing Data", "Date is required!")
                    return
                
                # Validate date
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    messagebox.showwarning("Invalid Date", "Please enter date in YYYY-MM-DD format")
                    return
                
                try:
                    self.db.add_milestone({
                        'name': name,
                        'description': description,
                        'date': date_str
                    })
                    messagebox.showinfo("Success", "Milestone added successfully!")
                    add_dialog.destroy()
                    load_milestones()  # Refresh the list
                    self.update_roadmap()  # Update roadmap
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add milestone: {str(e)}")
            
            # Buttons
            btn_frame_add = ttk.Frame(add_dialog)
            btn_frame_add.grid(row=3, column=0, columnspan=2, pady=15)
            
            ttk.Button(btn_frame_add, text="Save", command=save_new_milestone).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame_add, text="Cancel", command=add_dialog.destroy).pack(side=tk.LEFT, padx=5)
            
            # Make dialog modal
            add_dialog.transient(dialog)
            add_dialog.grab_set()
        
        ttk.Button(btn_frame, text="Add New", command=add_new_milestone).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Details", command=view_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
    
    def update_roadmap(self):
        """Update the roadmap visualization with Gantt-style timeline."""
        # Clear previous plot
        for widget in self.roadmap_frame.winfo_children():
            widget.destroy()
        
        # Get filters
        filters = {}
        if hasattr(self, 'roadmap_platform') and self.roadmap_platform.get():
            filters['platform'] = self.roadmap_platform.get()
        if hasattr(self, 'roadmap_odd') and self.roadmap_odd.get():
            filters['odd'] = self.roadmap_odd.get()
        if hasattr(self, 'roadmap_environment') and self.roadmap_environment.get():
            filters['environment'] = self.roadmap_environment.get()
        
        # Create figure
        fig = Figure(figsize=(14, 10), dpi=100)
        ax = fig.add_subplot(111)
        
        view = self.roadmap_view.get()
        
        # TRL colors: Red (TRL3), Amber (TRL6), Green (TRL9)
        trl_colors = {
            'TRL3': '#DC3545',  # Red
            'TRL6': '#FFC107',  # Amber
            'TRL9': '#28A745'   # Green
        }
        
        # Collect items with TRL progression
        items = []
        
        if view == 'Product Features':
            pfs = self.db.get_product_features(filters)
            for pf in pfs:
                # Skip if no dates
                if not any([pf.get('trl3_date'), pf.get('trl6_date'), pf.get('trl9_date')]):
                    continue
                
                trl_dates = []
                if pf.get('trl3_date'):
                    try:
                        trl_dates.append(('TRL3', datetime.strptime(pf['trl3_date'], '%Y-%m-%d')))
                    except: pass
                if pf.get('trl6_date'):
                    try:
                        trl_dates.append(('TRL6', datetime.strptime(pf['trl6_date'], '%Y-%m-%d')))
                    except: pass
                if pf.get('trl9_date'):
                    try:
                        trl_dates.append(('TRL9', datetime.strptime(pf['trl9_date'], '%Y-%m-%d')))
                    except: pass
                
                if trl_dates:
                    trl_dates.sort(key=lambda x: x[1])  # Sort by date
                    items.append({
                        'label': pf['label'],
                        'name': pf['name'][:40] + '...' if len(pf['name']) > 40 else pf['name'],
                        'trl_dates': trl_dates
                    })
        
        elif view == 'Capabilities':
            caps = self.db.get_capabilities(filters)
            for cap in caps:
                # Skip if no dates
                if not any([cap.get('trl3_date'), cap.get('trl6_date'), cap.get('trl9_date')]):
                    continue
                
                trl_dates = []
                if cap.get('trl3_date'):
                    try:
                        trl_dates.append(('TRL3', datetime.strptime(cap['trl3_date'], '%Y-%m-%d')))
                    except: pass
                if cap.get('trl6_date'):
                    try:
                        trl_dates.append(('TRL6', datetime.strptime(cap['trl6_date'], '%Y-%m-%d')))
                    except: pass
                if cap.get('trl9_date'):
                    try:
                        trl_dates.append(('TRL9', datetime.strptime(cap['trl9_date'], '%Y-%m-%d')))
                    except: pass
                
                if trl_dates:
                    trl_dates.sort(key=lambda x: x[1])  # Sort by date
                    items.append({
                        'label': cap['label'],
                        'name': cap['name'][:40] + '...' if len(cap['name']) > 40 else cap['name'],
                        'trl_dates': trl_dates
                    })
        
        if not items:
            ax.text(0.5, 0.5, 'No timeline data available\n\nSelect filters and click Update Roadmap', 
                   ha='center', va='center', fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            # Sort items by first TRL date
            items.sort(key=lambda x: x['trl_dates'][0][1])
            
            # Limit to top 50 items for readability
            if len(items) > 50:
                items = items[:50]
                title_suffix = f" (showing first 50 of {len(items)} items)"
            else:
                title_suffix = f" ({len(items)} items)"
            
            # Draw timeline bars
            y_pos = 0
            y_labels = []
            y_positions = []
            
            # Find date range
            all_dates = []
            for item in items:
                all_dates.extend([d[1] for d in item['trl_dates']])
            min_date = min(all_dates)
            max_date = max(all_dates)
            
            # Add padding to date range
            date_range = (max_date - min_date).days
            padding = max(30, date_range * 0.1)  # At least 30 days padding
            plot_min_date = min_date - timedelta(days=padding)
            plot_max_date = max_date + timedelta(days=padding)
            
            for item in items:
                y_labels.append(f"{item['label']}")
                y_positions.append(y_pos)
                
                # Draw segments between TRL milestones
                trl_dates = item['trl_dates']
                
                # Draw line segments with colors based on TRL level achieved
                for i in range(len(trl_dates)):
                    start_date = trl_dates[i][1]
                    start_trl = trl_dates[i][0]
                    
                    # Determine end date and color
                    if i < len(trl_dates) - 1:
                        end_date = trl_dates[i + 1][1]
                        color = trl_colors[start_trl]
                    else:
                        # Last segment extends to the right
                        end_date = start_date + timedelta(days=max(30, date_range * 0.05))
                        color = trl_colors[start_trl]
                    
                    # Draw horizontal bar
                    ax.barh(y_pos, (end_date - start_date).days, 
                           left=mdates.date2num(start_date), 
                           height=0.6, 
                           color=color, 
                           alpha=0.8,
                           edgecolor='black',
                           linewidth=0.5)
                    
                    # Add TRL marker at milestone
                    ax.plot(mdates.date2num(start_date), y_pos, 'o', 
                           color='black', markersize=6, zorder=10)
                
                y_pos += 1
            
            # Configure axes
            ax.set_ylim(-0.5, len(items) - 0.5)
            ax.set_yticks(y_positions)
            ax.set_yticklabels(y_labels, fontsize=8)
            ax.invert_yaxis()  # Top to bottom
            
            # Format x-axis as dates with abbreviated month and 2-digit year (Jan 25, Feb 26, etc.)
            ax.xaxis_date()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            
            # Rotate date labels
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            ax.set_xlabel('Timeline', fontsize=12, fontweight='bold')
            ax.set_title(f'{view} Roadmap{title_suffix}', fontsize=14, fontweight='bold')
            
            # Add grid
            ax.grid(True, axis='x', alpha=0.3, linestyle='--')
            
            # Add milestones
            milestones = self.db.get_milestones()
            for milestone in milestones:
                try:
                    milestone_date = datetime.strptime(milestone['date'], '%Y-%m-%d')
                    
                    # Check if milestone is within the visible date range
                    if plot_min_date <= milestone_date <= plot_max_date:
                        # Draw vertical line
                        ax.axvline(x=mdates.date2num(milestone_date), 
                                  color='purple', linestyle='--', linewidth=2, alpha=0.7, zorder=5)
                        
                        # Add star at the top
                        ax.plot(mdates.date2num(milestone_date), -0.3, 
                               marker='*', color='gold', markersize=20, 
                               markeredgecolor='purple', markeredgewidth=1.5, zorder=15)
                        
                        # Add milestone name as annotation
                        ax.annotate(milestone['name'], 
                                   xy=(mdates.date2num(milestone_date), -0.3),
                                   xytext=(0, 10), textcoords='offset points',
                                   ha='center', va='bottom',
                                   fontsize=8, fontweight='bold',
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', 
                                           edgecolor='purple', alpha=0.8))
                except:
                    pass  # Skip invalid milestone dates
            
            # Add legend
            from matplotlib.patches import Patch
            from matplotlib.lines import Line2D
            legend_elements = [
                Patch(facecolor=trl_colors['TRL3'], label='TRL 3 (Proof of Concept)', alpha=0.8),
                Patch(facecolor=trl_colors['TRL6'], label='TRL 6 (Prototype)', alpha=0.8),
                Patch(facecolor=trl_colors['TRL9'], label='TRL 9 (Production)', alpha=0.8),
                Line2D([0], [0], marker='*', color='w', markerfacecolor='gold', 
                      markeredgecolor='purple', markersize=12, label='Milestone')
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
            
            # Tight layout
            fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.roadmap_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def export_to_json(self):
        """Export all database content to a JSON file."""
        # Ask user for file location
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Database to JSON"
        )
        
        if not filepath:
            return
        
        try:
            # Gather all data from database
            export_data = {
                'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'product_features': [],
                'capabilities': [],
                'technical_functions': [],
                'pf_capabilities_relationships': [],
                'cap_technical_functions_relationships': []
            }
            
            # Export Product Features
            pfs = self.db.get_product_features()
            for pf in pfs:
                export_data['product_features'].append(pf)
            
            # Export Capabilities
            caps = self.db.get_capabilities()
            for cap in caps:
                export_data['capabilities'].append(cap)
            
            # Export Technical Functions
            tfs = self.db.get_technical_functions()
            for tf in tfs:
                export_data['technical_functions'].append(tf)
            
            # Export relationships - Product Features to Capabilities
            for pf in pfs:
                linked_caps = self.db.get_pf_capabilities(pf['id'])
                for cap in linked_caps:
                    export_data['pf_capabilities_relationships'].append({
                        'product_feature_id': pf['id'],
                        'product_feature_label': pf['label'],
                        'capability_id': cap['id'],
                        'capability_label': cap['label']
                    })
            
            # Export relationships - Capabilities to Technical Functions
            for cap in caps:
                linked_tfs = self.db.get_cap_technical_functions(cap['id'])
                for tf in linked_tfs:
                    export_data['cap_technical_functions_relationships'].append({
                        'capability_id': cap['id'],
                        'capability_label': cap['label'],
                        'technical_function_id': tf['id'],
                        'technical_function_label': tf['label']
                    })
            
            # Write to JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo(
                "Export Successful",
                f"Database exported successfully to:\n{filepath}\n\n"
                f"Product Features: {len(export_data['product_features'])}\n"
                f"Capabilities: {len(export_data['capabilities'])}\n"
                f"Technical Functions: {len(export_data['technical_functions'])}\n"
                f"PF-Capability Links: {len(export_data['pf_capabilities_relationships'])}\n"
                f"Capability-TF Links: {len(export_data['cap_technical_functions_relationships'])}"
            )
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export database:\n{str(e)}")
    
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
