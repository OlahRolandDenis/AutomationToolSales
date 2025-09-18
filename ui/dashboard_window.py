import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime, timedelta
from models.sale import Sale
from models.offer import Offer
from models.offer_pos import Offer_pos
import csv
from tkcalendar import DateEntry  # For date selection

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DashboardWindow(ctk.CTk):
    def __init__(self, user, sales_service, offer_service):
        super().__init__()
        self.user = user
        self.sales_service = sales_service
        self.offer_service = offer_service
        
        # Simplified color palette (black, white, and one highlight color)
        self.colors = {
            'primary': '#ffffff',      # White background
            'secondary': '#000000',    # Black text and borders
            'accent': '#007bff',       # Blue highlight
            'light_gray': '#f8f9fa',   # Light gray for subtle backgrounds
            'dark_gray': '#343a40',    # Dark gray for headers
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
        }
        
        self.selected_date = date.today()
        self.date_filter_mode = "day"
        self.start_date = None
        self.end_date = None
        self.current_offer_positions = []
        self.saved_offers = []  # Store saved offers
        
        self.title(f"Sales & Offers Dashboard - {user.username}")
        self.geometry("1600x1000")
        self.configure(fg_color=self.colors['primary'])
        
        self.create_widgets()
        self.refresh_sales_list()
        self.load_saved_offers()
        
    def create_widgets(self):
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_header(main_container)
        
        # Notebook for tabs
        self.notebook = ctk.CTkTabview(
            main_container,
            fg_color=self.colors['primary'],
            segmented_button_fg_color=self.colors['dark_gray'],
            segmented_button_selected_color=self.colors['accent'],
            text_color=self.colors['primary'],
            segmented_button_unselected_color=self.colors['dark_gray'],
            segmented_button_unselected_hover_color=self.colors['text_secondary']
        )
        self.notebook.pack(fill="both", expand=True, pady=(15, 0))
        
        # Create tabs
        self.sales_tab = self.notebook.add("Sales Management")
        self.offers_tab = self.notebook.add("Offers Management")
        
        self.setup_sales_tab()
        self.setup_offers_tab()
        
    def create_header(self, parent):
        # Header frame with user info
        header_frame = ctk.CTkFrame(
            parent, 
            height=70, 
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Left side with user info
        left_info = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_info.pack(side="left", fill="y", padx=25, pady=15)
        
        user_info = ctk.CTkLabel(
            left_info, 
            text=f"User: {self.user.username}",
            font=("Arial", 18, "bold"),
            text_color=self.colors['primary']
        )
        user_info.pack(anchor="w")
        
        role_info = ctk.CTkLabel(
            left_info,
            text=f"Role: {'Administrator' if self.user.is_admin else 'User'}",
            font=("Arial", 12),
            text_color=self.colors['primary']
        )
        role_info.pack(anchor="w", pady=(2, 0))
        
        # Right side with date info
        right_info = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_info.pack(side="right", fill="y", padx=25, pady=15)
        
        date_label = ctk.CTkLabel(
            right_info,
            text=f"Date: {date.today().strftime('%A, %d %B %Y')}",
            font=("Arial", 14),
            text_color=self.colors['primary']
        )
        date_label.pack(anchor="e")
        
    def setup_sales_tab(self):
        # Sales tab container
        sales_container = ctk.CTkFrame(self.sales_tab, fg_color="transparent")
        sales_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.create_date_filter_section(sales_container)
        
        content_area = ctk.CTkFrame(sales_container, fg_color="transparent")
        content_area.pack(fill="both", expand=True, pady=(15, 0))
        
        self.create_sales_input_panel(content_area)
        self.create_sales_display_panel(content_area)
        
    def create_date_filter_section(self, parent):
        # Date filter section
        filter_container = ctk.CTkFrame(
            parent, 
            height=100,
            fg_color=self.colors['light_gray'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['secondary']
        )
        filter_container.pack(fill="x", pady=(0, 15))
        filter_container.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            filter_container,
            text="Date Selection",
            font=("Arial", 16, "bold"),
            text_color=self.colors['secondary']
        )
        title_label.pack(pady=(15, 10))
        
        controls_frame = ctk.CTkFrame(filter_container, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        nav_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        nav_frame.pack(side="left", padx=(0, 15))
        
        prev_btn = ctk.CTkButton(
            nav_frame,
            text="< Previous Day",
            width=120,
            height=35,
            command=self.navigate_previous,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        prev_btn.pack(side="left", padx=2)
        
        self.date_display = ctk.CTkLabel(
            nav_frame,
            text=self.get_date_display_text(),
            font=("Arial", 12, "bold"),
            width=180,
            height=35,
            fg_color=self.colors['accent'],
            text_color=self.colors['primary'],
            corner_radius=0
        )
        self.date_display.pack(side="left", padx=10)
        
        next_btn = ctk.CTkButton(
            nav_frame,
            text="Next Day >",
            width=120,
            height=35,
            command=self.navigate_next,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        next_btn.pack(side="left", padx=2)
        
        action_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        action_frame.pack(side="right")
        
        today_btn = ctk.CTkButton(
            action_frame,
            text="Today",
            width=80,
            height=35,
            command=self.select_today,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        today_btn.pack(side="left", padx=5)
        
    def create_sales_input_panel(self, parent):
        # Sales input panel
        input_panel = ctk.CTkFrame(
            parent, 
            width=450,
            fg_color=self.colors['light_gray'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['secondary']
        )
        input_panel.pack(side="left", fill="y", padx=(0, 15))
        input_panel.pack_propagate(False)
        
        title_frame = ctk.CTkFrame(
            input_panel, 
            height=60,
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Add New Sale",
            font=("Arial", 16, "bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(expand=True)
        
        tip_label = ctk.CTkLabel(
            input_panel,
            text="Quick Entry: Document → Tab → Amount → Enter",
            font=("Arial", 11),
            text_color=self.colors['text_secondary'],
            fg_color=self.colors['primary'],
            corner_radius=0,
            height=30
        )
        tip_label.pack(fill="x", padx=20, pady=(10, 20))
        
        fields_container = ctk.CTkFrame(input_panel, fg_color="transparent")
        fields_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Date selection for sale
        date_label = ctk.CTkLabel(
            fields_container, 
            text="Sale Date:",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_primary']
        )
        date_label.pack(anchor="w", pady=(0, 8))
        
        self.sale_date_entry = DateEntry(
            fields_container,
            width=42,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.sale_date_entry.pack(pady=(0, 20))
        
        doc_label = ctk.CTkLabel(
            fields_container, 
            text="Document Number:",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_primary']
        )
        doc_label.pack(anchor="w", pady=(0, 8))
        
        self.doc_entry = ctk.CTkEntry(
            fields_container,
            placeholder_text="e.g., BC15213, INV2024001...",
            width=410,
            height=45,
            font=("Arial", 12),
            border_width=1,
            border_color=self.colors['secondary']
        )
        self.doc_entry.pack(pady=(0, 20))
        
        amount_label = ctk.CTkLabel(
            fields_container, 
            text="Amount (RON):",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_primary']
        )
        amount_label.pack(anchor="w", pady=(0, 8))
        
        self.amount_entry = ctk.CTkEntry(
            fields_container,
            placeholder_text="e.g., 1250.50",
            width=410,
            height=45,
            font=("Arial", 12),
            border_width=1,
            border_color=self.colors['secondary']
        )
        self.amount_entry.pack(pady=(0, 25))
        
        buttons_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 20))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save Sale",
            command=self.save_sale,
            width=410,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        save_btn.pack(pady=(0, 10))
        
        export_btn = ctk.CTkButton(
            buttons_frame,
            text="Export Sales CSV",
            command=self.export_sales,
            width=410,
            height=40,
            font=("Arial", 12),
            fg_color=self.colors['accent'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        export_btn.pack()
        
        self.doc_entry.bind('<Tab>', lambda e: (self.amount_entry.focus_set(), 'break')[1])
        self.amount_entry.bind('<Return>', lambda e: self.save_sale())
        
    def create_sales_display_panel(self, parent):
        # Sales display panel
        display_panel = ctk.CTkFrame(
            parent,
            fg_color=self.colors['light_gray'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['secondary']
        )
        display_panel.pack(side="right", fill="both", expand=True)
        
        header_frame = ctk.CTkFrame(
            display_panel,
            height=60,
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        self.sales_title_label = ctk.CTkLabel(
            header_frame,
            text="Sales for Selected Period",
            font=("Arial", 16, "bold"),
            text_color=self.colors['primary']
        )
        self.sales_title_label.pack(side="left", padx=20, expand=True)
        
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="Total: 0 sales | 0.00 RON",
            font=("Arial", 12),
            text_color=self.colors['primary']
        )
        self.stats_label.pack(side="right", padx=20)
        
        tree_container = ctk.CTkFrame(display_panel, fg_color=self.colors['primary'])
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                       background=self.colors['primary'],
                       foreground=self.colors['secondary'],
                       rowheight=35,
                       fieldbackground=self.colors['primary'],
                       font=("Arial", 11),
                       bordercolor=self.colors['secondary'],
                       borderwidth=1)
        style.configure("Custom.Treeview.Heading",
                       background=self.colors['dark_gray'],
                       foreground=self.colors['primary'],
                       font=("Arial", 11, "bold"),
                       relief="flat")
        style.map("Custom.Treeview.Heading",
                 background=[('active', self.colors['text_secondary'])])
        
        columns = ('ID', 'Document', 'Amount', 'Date', 'Time')
        self.sales_tree = ttk.Treeview(
            tree_container, 
            columns=columns, 
            show='headings',
            style="Custom.Treeview"
        )
        
        column_configs = {
            'ID': (60, 'center'),
            'Document': (180, 'w'),
            'Amount': (120, 'e'),
            'Date': (120, 'center'),
            'Time': (100, 'center')
        }
        
        for col, (width, anchor) in column_configs.items():
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=width, anchor=anchor)
        
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=v_scrollbar.set)
        
        self.sales_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        v_scrollbar.pack(side="right", fill="y", pady=10)
        
    def setup_offers_tab(self):
        # Offers tab container
        offers_container = ctk.CTkFrame(self.offers_tab, fg_color="transparent")
        offers_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Create a split view for creating offers and viewing saved offers
        split_frame = ctk.CTkFrame(offers_container, fg_color="transparent")
        split_frame.pack(fill="both", expand=True)
        
        # Left side - create new offer
        left_frame = ctk.CTkFrame(split_frame, fg_color="transparent", width=600)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        left_frame.pack_propagate(False)
        
        self.create_client_section(left_frame)
        self.create_product_input_section(left_frame)
        
        bottom_section = ctk.CTkFrame(left_frame, fg_color="transparent")
        bottom_section.pack(fill="both", expand=True, pady=(15, 0))
        
        self.create_products_display(bottom_section)
        self.create_offer_actions_panel(bottom_section)
        
        # Right side - saved offers list
        right_frame = ctk.CTkFrame(split_frame, fg_color=self.colors['light_gray'], width=400)
        right_frame.pack(side="right", fill="both")
        right_frame.pack_propagate(False)
        
        saved_offers_header = ctk.CTkFrame(
            right_frame,
            height=50,
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        saved_offers_header.pack(fill="x", padx=0, pady=0)
        saved_offers_header.pack_propagate(False)
        
        ctk.CTkLabel(
            saved_offers_header,
            text="Saved Offers",
            font=("Arial", 14, "bold"),
            text_color=self.colors['primary']
        ).pack(expand=True)
        
        # Treeview for saved offers
        tree_container = ctk.CTkFrame(right_frame, fg_color=self.colors['primary'])
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Client', 'Date', 'Total')
        self.saved_offers_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show='headings',
            style="Custom.Treeview"
        )
        
        saved_offers_column_configs = {
            'ID': (60, 'center'),
            'Client': (150, 'w'),
            'Date': (100, 'center'),
            'Total': (80, 'e')
        }
        
        for col, (width, anchor) in saved_offers_column_configs.items():
            self.saved_offers_tree.heading(col, text=col)
            self.saved_offers_tree.column(col, width=width, anchor=anchor)
        
        saved_offers_v_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.saved_offers_tree.yview)
        self.saved_offers_tree.configure(yscrollcommand=saved_offers_v_scroll.set)
        
        self.saved_offers_tree.pack(side="left", fill="both", expand=True)
        saved_offers_v_scroll.pack(side="right", fill="y")
        
        # Bind double-click event to open offer details
        self.saved_offers_tree.bind('<Double-1>', self.open_offer_details)
        
    def create_client_section(self, parent):
        # Client information section
        client_frame = ctk.CTkFrame(
            parent,
            height=90,
            fg_color=self.colors['light_gray'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['secondary']
        )
        client_frame.pack(fill="x", pady=(0, 15))
        client_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            client_frame,
            text="Client Information",
            font=("Arial", 16, "bold"),
            text_color=self.colors['secondary']
        )
        title_label.pack(pady=(15, 5))
        
        input_frame = ctk.CTkFrame(client_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        ctk.CTkLabel(
            input_frame,
            text="Client CIF:",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left", padx=(0, 15))
        
        self.client_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter client CIF number...",
            width=400,
            height=40,
            font=("Arial", 12),
            border_width=1,
            border_color=self.colors['secondary']
        )
        self.client_entry.pack(side="left")
        
        # Add button to fetch client data
        fetch_btn = ctk.CTkButton(
            input_frame,
            text="Fetch Client Data",
            command=self.fetch_client_data,
            width=120,
            height=40,
            font=("Arial", 11),
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        fetch_btn.pack(side="left", padx=(15, 0))
        
    def create_product_input_section(self, parent):
        # Product input section
        input_section = ctk.CTkFrame(
            parent,
            height=140,
            fg_color=self.colors['light_gray'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['secondary']
        )
        input_section.pack(fill="x", pady=(0, 15))
        input_section.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            input_section,
            text="Add Product to Offer",
            font=("Arial", 16, "bold"),
            text_color=self.colors['secondary']
        )
        title_label.pack(pady=(15, 10))
        
        fields_container = ctk.CTkFrame(input_section, fg_color="transparent")
        fields_container.pack(fill="x", padx=30, pady=(0, 15))
        
        row1 = ctk.CTkFrame(fields_container, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row1, text="Code:", width=80, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.product_code_entry = ctk.CTkEntry(row1, width=150, height=35, border_width=1, border_color=self.colors['secondary'])
        self.product_code_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Name:", width=80, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.product_name_entry = ctk.CTkEntry(row1, width=300, height=35, border_width=1, border_color=self.colors['secondary'])
        self.product_name_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Qty:", width=80, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.quantity_entry = ctk.CTkEntry(row1, width=100, height=35, border_width=1, border_color=self.colors['secondary'])
        self.quantity_entry.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(fields_container, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row2, text="Price:", width=80, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.unit_price_entry = ctk.CTkEntry(row2, width=120, height=35, border_width=1, border_color=self.colors['secondary'])
        self.unit_price_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row2, text="VAT %:", width=80, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.vat_entry = ctk.CTkEntry(row2, width=100, height=35, border_width=1, border_color=self.colors['secondary'])
        self.vat_entry.pack(side="left", padx=5)
        
        buttons_frame = ctk.CTkFrame(row2, fg_color="transparent")
        buttons_frame.pack(side="right", padx=20)
        
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="Add",
            command=self.add_product_to_offer,
            width=100,
            height=35,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary'],
            font=("Arial", 11, "bold")
        )
        add_btn.pack(side="left", padx=5)
        
        remove_btn = ctk.CTkButton(
            buttons_frame,
            text="Remove",
            command=self.remove_selected_product,
            width=100,
            height=35,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary'],
            font=("Arial", 11, "bold")
        )
        remove_btn.pack(side="left", padx=5)
        
    def create_products_display(self, parent):
        # Products display section
        products_panel = ctk.CTkFrame(
            parent,
            fg_color=self.colors['light_gray'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['secondary']
        )
        products_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        header = ctk.CTkFrame(
            products_panel,
            height=50,
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header,
            text="Current Offer Products",
            font=("Arial", 14, "bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(expand=True)
        
        tree_container = ctk.CTkFrame(products_panel, fg_color=self.colors['primary'])
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ('Code', 'Name', 'Qty', 'Unit Price', 'VAT%', 'Line Total')
        self.products_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show='headings',
            style="Custom.Treeview"
        )
        
        product_column_configs = {
            'Code': (100, 'w'),
            'Name': (200, 'w'),
            'Qty': (80, 'center'),
            'Unit Price': (100, 'e'),
            'VAT%': (80, 'center'),
            'Line Total': (120, 'e')
        }
        
        for col, (width, anchor) in product_column_configs.items():
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=width, anchor=anchor)
        
        products_v_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=products_v_scroll.set)
        
        self.products_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        products_v_scroll.pack(side="right", fill="y", pady=10)
        
    def create_offer_actions_panel(self, parent):
        # Offer actions panel
        actions_panel = ctk.CTkFrame(
            parent,
            width=400,
            fg_color=self.colors['light_gray'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['secondary']
        )
        actions_panel.pack(side="right", fill="y")
        actions_panel.pack_propagate(False)
        
        header = ctk.CTkFrame(
            actions_panel,
            height=50,
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header,
            text="Actions",
            font=("Arial", 14, "bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(expand=True)
        
        buttons_container = ctk.CTkFrame(actions_panel, fg_color="transparent")
        buttons_container.pack(fill="x", padx=20, pady=(20, 20))
        
        preview_internal_btn = ctk.CTkButton(
            buttons_container,
            text="Preview Internal",
            command=self.preview_offer_internal,
            width=360,
            height=40,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        preview_internal_btn.pack(pady=5)
        
        preview_client_btn = ctk.CTkButton(
            buttons_container,
            text="Preview Client",
            command=self.preview_offer_client,
            width=360,
            height=40,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        preview_client_btn.pack(pady=5)
        
        save_offer_btn = ctk.CTkButton(
            buttons_container,
            text="Save Offer",
            command=self.save_offer,
            width=360,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        save_offer_btn.pack(pady=(15, 5))
        
        clear_btn = ctk.CTkButton(
            buttons_container,
            text="Clear Offer",
            command=self.clear_offer,
            width=360,
            height=35,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        clear_btn.pack(pady=5)
    
    def get_date_display_text(self):
        """Return formatted date text for display"""
        pass
    
    def on_filter_mode_change(self):
        """Handle filter mode change"""
        pass
    
    def navigate_previous(self):
        """Navigate to previous day"""
        pass
    
    def navigate_next(self):
        """Navigate to next day"""
        pass
    
    def select_today(self):
        """Select today's date"""
        pass
    
    def update_date_display(self):
        """Update the date display label"""
        pass
    
    def save_sale(self):
        """Save a new sale to the database"""
        pass
    
    def refresh_sales_list(self):
        """Refresh the sales list with data from the database"""
        pass
    
    def export_sales(self):
        """Export sales data to a CSV file"""
        pass
    
    def fetch_client_data(self):
        """Fetch client data based on CIF"""
        pass
    
    def add_product_to_offer(self):
        """Add a product to the current offer"""
        pass
    
    def remove_selected_product(self):
        """Remove selected product from the current offer"""
        pass
    
    def preview_offer_internal(self):
        """Preview offer with internal product names"""
        pass
    
    def preview_offer_client(self):
        """Preview offer with client-facing product names"""
        pass
    
    def show_offer_preview(self, internal=True):
        """Show a preview of the current offer"""
        pass
    
    def export_offer_csv(self, internal=True):
        """Export offer to CSV format"""
        pass
    
    def export_offer_pdf(self):
        """Export offer to PDF format"""
        pass
    
    def save_offer(self):
        """Save the current offer to the database"""
        pass
    
    def load_saved_offers(self):
        """Load saved offers from the database"""
        pass
    
    def open_offer_details(self, event):
        """Open details of a saved offer"""
        pass
    
    def clear_offer(self):
        """Clear the current offer"""
        pass


class OfferDetailWindow(ctk.CTkToplevel):
    def __init__(self, parent, offer, offer_service):
        """Initialize offer detail window"""
        super().__init__(parent)
        self.offer = offer
        self.offer_service = offer_service
        self.title(f"Offer Details - {offer.client_cif}")
        self.geometry("1000x800")
        self.configure(fg_color=parent.colors['primary'])
        
        # Create the GUI elements for offer details
        pass
    
    def export_offer_csv(self, internal=True):
        """Export offer to CSV format"""
        pass
    
    def export_offer_pdf(self):
        """Export offer to PDF format"""
        pass