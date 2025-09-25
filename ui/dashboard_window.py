import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime, timedelta
from ui.offer_window import OfferDetailWindow
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DashboardWindow(ctk.CTk):
    def __init__(self, user, sales_service, offer_service):
        super().__init__()
        self.user = user
        self.sales_service = sales_service
        self.offer_service = offer_service
        
      
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
        self.saved_offers = []
        
        self.title(f"Sales & Offers Dashboard - {user.username}")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(fg_color=self.colors['primary'])
        
        self.create_widgets()
        self.after_idle(self.initial_data_load)

    def initial_data_load(self):
        self.refresh_sales_list()
        self.load_saved_offers()
        
    def create_widgets(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_header(main_container)
        
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
        
        self.sales_tab = self.notebook.add("Sales Management")
        self.offers_tab = self.notebook.add("Offers Management")
        
        self.setup_sales_tab()
        self.setup_offers_tab()
        
    def create_header(self, parent):
        header_frame = ctk.CTkFrame(
            parent, 
            height=70, 
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
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
        sales_container = ctk.CTkFrame(self.sales_tab, fg_color="transparent")
        sales_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.create_date_filter_section(sales_container)
        
        content_area = ctk.CTkFrame(sales_container, fg_color="transparent")
        content_area.pack(fill="both", expand=True, pady=(15, 0))
        
        self.create_sales_input_panel(content_area)
        self.create_sales_display_panel(content_area)
        
        
    def create_date_filter_section(self, parent):
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

        scrollable_input = ctk.CTkScrollableFrame(parent, width=400)
        scrollable_input.pack(side="left", fill="y", padx=(0, 15))

        def on_mousewheel(event):
            scrollable_input._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        

        scrollable_input.bind("<MouseWheel>", on_mousewheel)
        scrollable_input.bind("<Button-4>", lambda e: scrollable_input._parent_canvas.yview_scroll(-1, "units"))
        scrollable_input.bind("<Button-5>", lambda e: scrollable_input._parent_canvas.yview_scroll(1, "units"))

        scrollable_input.bind_all("<MouseWheel>", on_mousewheel)

        input_panel = ctk.CTkFrame( 
        scrollable_input,
        fg_color=self.colors['light_gray'],
        corner_radius=0,
        border_width=1,
        border_color=self.colors['secondary']
        )
        input_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
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
        
        date_label = ctk.CTkLabel(
            fields_container, 
            text="Sale Date:",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_primary']
        )
        date_label.pack(anchor="w", pady=(0, 8))
        
        date_input_frame = ctk.CTkFrame(fields_container, fg_color="transparent")
        date_input_frame.pack(pady=(0, 20))

        ctk.CTkLabel(date_input_frame, text="Year:", font=("Arial", 11)).pack(side="left", padx=(0, 5))
        self.year_entry = ctk.CTkEntry(
            date_input_frame,
            width=80,
            height=35,
            placeholder_text="2024"
        )
        self.year_entry.pack(side="left", padx=(0, 15))
        self.year_entry.insert(0, str(date.today().year))

        ctk.CTkLabel(date_input_frame, text="Month:", font=("Arial", 11)).pack(side="left", padx=(0, 5))
        self.month_entry = ctk.CTkEntry(
            date_input_frame,
            width=60,
            height=35,
            placeholder_text="12"
        )
        self.month_entry.pack(side="left", padx=(0, 15))
        self.month_entry.insert(0, str(date.today().month).zfill(2))

        ctk.CTkLabel(date_input_frame, text="Day:", font=("Arial", 11)).pack(side="left", padx=(0, 5))
        self.day_entry = ctk.CTkEntry(
            date_input_frame,
            width=60,
            height=35,
            placeholder_text="25"
        )
        self.day_entry.pack(side="left", padx=(0, 15))
        self.day_entry.insert(0, str(date.today().day).zfill(2))
        
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
        
        export_day_btn = ctk.CTkButton(
            buttons_frame,
            text="Export Day PDF",
            command=self.export_day_pdf,
            width=410,
            height=40,
            font=("Arial", 12),
            fg_color=self.colors['accent'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        export_day_btn.pack(pady=(0, 5))

        export_month_btn = ctk.CTkButton(
            buttons_frame,
            text="Export Month PDF",
            command=self.export_month_pdf,
            width=410,
            height=40,
            font=("Arial", 12),
            fg_color=self.colors['accent'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary']
        )
        export_month_btn.pack()
        
        self.doc_entry.bind('<Tab>', lambda e: (self.amount_entry.focus_set(), 'break')[1])
        self.amount_entry.bind('<Return>', lambda e: self.save_sale())
        
    def create_sales_display_panel(self, parent):
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
        self.sales_tree.bind('<Double-1>', self.open_sales_to_delete)
        
    def setup_offers_tab(self):
        offers_container = ctk.CTkFrame(self.offers_tab, fg_color="transparent")
        offers_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        split_frame = ctk.CTkFrame(offers_container, fg_color="transparent")
        split_frame.pack(fill="both", expand=True)
        
        left_frame = ctk.CTkFrame(split_frame, fg_color="transparent", width=600)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        left_frame.pack_propagate(False)
        
        self.create_client_section(left_frame)
        self.create_product_input_section(left_frame)
        
        bottom_section = ctk.CTkFrame(left_frame, fg_color="transparent")
        bottom_section.pack(fill="both", expand=True, pady=(15, 0))
        
        self.create_products_display(bottom_section)
        self.create_offer_actions_panel(bottom_section)
        
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
        
        self.saved_offers_tree.bind('<Double-1>', self.open_offer_details)
        
    def create_client_section(self, parent):
        client_frame = ctk.CTkFrame(
            parent,
            height=130,  # Reduced height since we only need 2 rows now
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
        
        # Create container for all input fields
        input_frame = ctk.CTkFrame(client_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        # Row 1: CIF, Name, Phone
        row1 = ctk.CTkFrame(input_frame, fg_color="transparent")
        row1.pack(fill="x", pady=3)
        
        ctk.CTkLabel(row1, text="CIF:", width=50, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.client_cif_entry = ctk.CTkEntry(row1, width=120, height=35, border_width=1, border_color=self.colors['secondary'])
        self.client_cif_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Name:", width=50, font=("Arial", 11, "bold")).pack(side="left", padx=(15, 5))
        self.client_name_entry = ctk.CTkEntry(row1, width=200, height=35, border_width=1, border_color=self.colors['secondary'])
        self.client_name_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="Phone:", width=50, font=("Arial", 11, "bold")).pack(side="left", padx=(15, 5))
        self.client_phone_entry = ctk.CTkEntry(row1, width=150, height=35, border_width=1, border_color=self.colors['secondary'])
        self.client_phone_entry.pack(side="left", padx=5)
        
        row2 = ctk.CTkFrame(input_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(10, 3))
        
        ctk.CTkLabel(row2, text="Address:", width=50, font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.client_address_entry = ctk.CTkEntry(row2, width=600, height=35, border_width=1, border_color=self.colors['secondary'])
        self.client_address_entry.pack(side="left", padx=5)
        
    def create_product_input_section(self, parent):
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
        self.vat_entry.insert(0, "21")
        
        buttons_frame = ctk.CTkFrame(row2, fg_color="transparent")
        buttons_frame.pack(side="right", padx=20)
        
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="Add",
            command=self.add_product_to_offer,
            width=100,
            height=50,
            fg_color=self.colors['dark_gray'],
            text_color=self.colors['primary'],
            hover_color=self.colors['text_secondary'],
            font=("Arial", 11, "bold")
        )
        add_btn.pack(side="left", padx=5)
        
        
    def create_products_display(self, parent):
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


    #
    
    def get_date_display_text(self):
        return self.selected_date.strftime('%A, %B %d, %Y')
    
    def navigate_previous(self):
        self.selected_date = self.selected_date - timedelta(days=1)
        self.update_date_display()
        self.update_manual_date_inputs()  
        self.refresh_sales_list()
    
    def navigate_next(self):
        self.selected_date = self.selected_date + timedelta(days=1)
        self.update_date_display()
        self.update_manual_date_inputs()  
        self.refresh_sales_list()
    
    def select_today(self):
        self.selected_date = date.today()
        self.update_date_display()
        self.update_manual_date_inputs()  
        self.refresh_sales_list()
    
    def update_date_display(self):
        self.date_display.configure(text=self.get_date_display_text())

    def update_manual_date_inputs(self):
        self.year_entry.delete(0, 'end')
        self.year_entry.insert(0, str(self.selected_date.year))

        self.month_entry.delete(0, 'end')
        self.month_entry.insert(0, str(self.selected_date.month).zfill(2))

        self.day_entry.delete(0, 'end')
        self.day_entry.insert(0, str(self.selected_date.day).zfill(2))
       
    
    def save_sale(self):
        doc = self.doc_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        year_str = self.year_entry.get().strip()
        month_str = self.month_entry.get().strip() 
        day_str = self.day_entry.get().strip()

        if not doc or not amount_str or not year_str or not month_str or not day_str:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        try:
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)
            amount = float(amount_str)
            sale_date = date(year, month, day)
        except ValueError:
            messagebox.showerror("Error", "Invalid Format")
            return
        
        sale_datetime = datetime.combine(sale_date, datetime.now().time())


        if self.sales_service.create_sale(doc,amount,self.user,sale_datetime):
            messagebox.showinfo("Success", "Sale Created")
            self.doc_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')
            self.refresh_sales_list()
        else:
            messagebox.showerror("Error", "Failed creating sale")

        

    def refresh_sales_list(self):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        sales = self.sales_service.get_sales_by_date(self.user, self.selected_date)

        total_amount = 0

        for sale in sales:
            dt = datetime.fromisoformat(sale.timestamp)
            self.sales_tree.insert('', 'end', values=(
                sale.id,
                sale.doc,
                f"{sale.amount:.2f}",
                dt.strftime('%Y-%m-%d'),
                dt.strftime('%H:%M')
            ))
            total_amount += sale.amount
        self.stats_label.configure(text=f"Total: {len(sales)} sales | {total_amount:.2f} RON")
        

    def add_product_to_offer(self):
        code = self.product_code_entry.get().strip()
        name = self.product_name_entry.get().strip()
        qty_str = self.quantity_entry.get().strip()
        price_str = self.unit_price_entry.get().strip()
        vat_str = self.vat_entry.get().strip()

        if not code or not name or not qty_str or not price_str or not vat_str:
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            quantity = float(qty_str)
            unit_price = float(price_str)
            vat = float(vat_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid Format")
            return

        product = {
            'product_code': code,
            'product_name': name,
            'quantity': quantity,
            'unit_price': unit_price,
            'vat': vat
        }
        self.current_offer_positions.append(product)
        self.refresh_products_display()
        self.clear_product_fields()


    
    # def remove_selected_product(self):

    #     selection = self.products_tree.selection()
    #     if not selection:
    #         messagebox.showerror("Error", "Select profuct to remove")
    #         return

    #     item = self.products_tree.item(selection[0])
    #     product_code = item['values'][0]

    #     new_positions = []
    #     for p in self.current_offer_positions:
    #         if p['product_code'] != product_code:
    #             new_positions.append(p)

    #     self.current_offer_positions = new_positions
    #     self.refresh_products_display()

    def refresh_products_display(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)


        for product in self.current_offer_positions:
            line_total = product['quantity'] * product['unit_price'] * (1 + product['vat']/100)
            self.products_tree.insert('', 'end', values=(
                product['product_code'],
                product['product_name'],
                product['quantity'],
                f"{product['unit_price']:.2f}",
                f"{product['vat']:.1f}",
                f"{line_total:.2f}"
            ))


    def clear_product_fields(self):
        self.product_code_entry.delete(0, 'end')
        self.product_name_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.unit_price_entry.delete(0, 'end')
        self.vat_entry.delete(0, 'end')
        self.vat_entry.insert(0, "21")
        
    
    def save_offer(self):
        try:
            cif = self.client_cif_entry.get() or ""
            name = self.client_name_entry.get() or ""
            address = self.client_address_entry.get() or ""
            phone = self.client_phone_entry.get() or ""
            
            cif = cif.strip()
            name = name.strip()
            address = address.strip()
            phone = phone.strip()
            
            print(f"Debug - CIF: '{cif}' (len: {len(cif)})")
            print(f"Debug - Name: '{name}' (len: {len(name)})")
            print(f"Debug - Address: '{address}' (len: {len(address)})")
            print(f"Debug - Phone: '{phone}' (len: {len(phone)})")
            print(f"Debug - Products: {len(self.current_offer_positions)}")
            
            if not cif:
                print("CIF is empty")
            if not name:
                print("Name is empty")
            if not address:
                print("Address is empty")
            if not phone:
                print("Phone is empty")
            if not self.current_offer_positions:
                print("No products")
            
            if not cif or not name or not address or not phone or not self.current_offer_positions:
                messagebox.showerror("Error", "Please fill all fields and add at least one product")
                return
            
            print("All fields are filled, proceeding to create offer...")
            
            if self.offer_service.create_offer(cif, name, address, phone, self.current_offer_positions, self.user):
                messagebox.showinfo("Success", "Offer created successfully")
                self.clear_offer()
                self.load_saved_offers()
            else:
                messagebox.showerror("Error", "Failed to create offer")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"Exception in save_offer: {e}")
            
    def load_saved_offers(self):
        for item in self.saved_offers_tree.get_children():
            self.saved_offers_tree.delete(item)

        offers = self.offer_service.get_offers_by_user(self.user)
        for offer in offers:
            total = sum(
                p.quantity * p.unit_price * (1 + p.vat/100)
                for p in offer.products
            )
            dt = datetime.fromisoformat(offer.timestamp)
            self.saved_offers_tree.insert('', 'end', values=(
                offer.id,
                offer.name if offer.name else offer.cif,
                dt.strftime('%Y-%m-%d'),
                f"{total:.2f}"
            ))
    
    def open_offer_details(self, event):
        selection = self.saved_offers_tree.selection()
        if not selection :
            messagebox.showerror("Error", "No selected offer")
            return

        item = self.saved_offers_tree.item(selection[0])
        offer_id = item['values'][0]

        offers = self.offer_service.get_offers_by_user(self.user)
        offer_data = None
        for o in offers:
            if o.id == offer_id:
                offer_data = o
                break
    
        if offer_data:
            detail_window = OfferDetailWindow(self, offer_data, self.offer_service)

    
    def clear_offer(self):
        self.client_cif_entry.delete(0, 'end')
        self.client_name_entry.delete(0, 'end')
        self.client_address_entry.delete(0, 'end')
        self.client_phone_entry.delete(0, 'end')
        self.current_offer_positions = []
        self.refresh_products_display()
        self.clear_product_fields()

    

    # def fetch_client_data(self):
    #     cif = self.client_entry.get().strip()

    #     if not cif:
    #         messagebox.showerror("Error", "Introduce CIF")
    #         return
    #     try:
    #         client_service = ClientData(cif)
    #         client_data = client_service.get_data()

    #         if client_data:
    #             name = client_data[0]
    #             code = client_data[1]
    #             addres = client_data[2]
    #             info_text = f"Company: {name}\nNumber: {code}\nAddress: {addres}"
    #             messagebox.showinfo("Client Data", info_text)
    #         else:
    #             messagebox.showerror("Error", "Could not fetch client data. Check CIF number or try again later.")
    #     except Exception as e:
    #         messagebox.showerror("Error", "Failed to fetch client data")


    def open_sales_to_delete(self,event):
        selection = self.sales_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Select sale")
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this sale?"):
            return

        try:
            item = self.sales_tree.item(selection[0])
            id = item["values"][0]
            if not self.sales_service.delete_sale(id):
                messagebox.showerror("Error", "Could not delete sale")
                return
            else:
                self.refresh_sales_list()
                messagebox.showinfo("Success", "Sale deleted")

        except Exception as e:
            messagebox.showerror("Error", f"Could not delete sale: {e}")

    def export_day_pdf(self):
        """Export sales for selected day to PDF"""
        try:
            sales = self.sales_service.get_sales_by_date(self.user, self.selected_date)
            
            if not sales:
                messagebox.showinfo("Info", "No sales data to export for selected date")
                return
            
            # Open file save dialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Daily Sales Report",
                initialfile=f"daily_sales_{self.selected_date.strftime('%Y-%m-%d')}.pdf"
            )
            
            if not file_path:
                return
            
            doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                alignment=TA_CENTER,
                spaceAfter=20
            )
            story.append(Paragraph(f"Daily Sales Report", title_style))
            
            # Header info
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_LEFT,
                spaceAfter=10
            )
            
            story.append(Paragraph(f"<b>User:</b> {self.user.username}", header_style))
            story.append(Paragraph(f"<b>Date:</b> {self.selected_date.strftime('%A, %B %d, %Y')}", header_style))
            story.append(Paragraph(f"<b>Total Sales:</b> {len(sales)}", header_style))
            
            total_amount = sum(sale.amount for sale in sales)
            story.append(Paragraph(f"<b>Total Amount:</b> {total_amount:.2f} RON", header_style))
            story.append(Spacer(1, 20))
            
            # Sales table
            data = [['Nr.', 'Document', 'Amount (RON)', 'Time']]
            
            for idx, sale in enumerate(sales, 1):
                dt = datetime.fromisoformat(sale.timestamp)
                data.append([
                    str(idx),
                    sale.doc,
                    f"{sale.amount:.2f}",
                    dt.strftime('%H:%M:%S')
                ])
            
            table = Table(data, colWidths=[1*cm, 8*cm, 3*cm, 3*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Document column left aligned
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # Amount column right aligned
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
            
            # Summary
            summary_style = ParagraphStyle(
                'SummaryStyle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                spaceAfter=10
            )
            story.append(Paragraph(f"<b>TOTAL: {total_amount:.2f} RON</b>", summary_style))
            story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            
            doc.build(story)
            messagebox.showinfo("Success", f"Daily sales report exported to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export daily sales:\n{str(e)}")


    def export_month_pdf(self):
        """Export sales for selected month to PDF"""
        try:
            # Get first and last day of the month
            first_day = self.selected_date.replace(day=1)
            if self.selected_date.month == 12:
                last_day = self.selected_date.replace(year=self.selected_date.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                last_day = self.selected_date.replace(month=self.selected_date.month + 1, day=1) - timedelta(days=1)
            
            # Get all sales for the month
            all_month_sales = []
            current_date = first_day
            
            while current_date <= last_day:
                daily_sales = self.sales_service.get_sales_by_date(self.user, current_date)
                if daily_sales:
                    all_month_sales.append((current_date, daily_sales))
                current_date += timedelta(days=1)
            
            if not all_month_sales:
                messagebox.showinfo("Info", "No sales data to export for selected month")
                return
            
            # Open file save dialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Monthly Sales Report",
                initialfile=f"monthly_sales_{self.selected_date.strftime('%Y-%m')}.pdf"
            )
            
            if not file_path:
                return
            
            doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                alignment=TA_CENTER,
                spaceAfter=20
            )
            story.append(Paragraph(f"Monthly Sales Report", title_style))
            
            # Header info
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_LEFT,
                spaceAfter=10
            )
            
            story.append(Paragraph(f"<b>User:</b> {self.user.username}", header_style))
            story.append(Paragraph(f"<b>Month:</b> {self.selected_date.strftime('%B %Y')}", header_style))
            
            total_days_with_sales = len(all_month_sales)
            total_sales_count = sum(len(daily_sales) for _, daily_sales in all_month_sales)
            total_month_amount = sum(sale.amount for _, daily_sales in all_month_sales for sale in daily_sales)
            
            story.append(Paragraph(f"<b>Days with Sales:</b> {total_days_with_sales}", header_style))
            story.append(Paragraph(f"<b>Total Sales:</b> {total_sales_count}", header_style))
            story.append(Paragraph(f"<b>Total Amount:</b> {total_month_amount:.2f} RON", header_style))
            story.append(Spacer(1, 20))
            
            # Daily breakdown
            day_style = ParagraphStyle(
                'DayStyle',
                parent=styles['Heading2'],
                fontSize=14,
                alignment=TA_LEFT,
                spaceAfter=10,
                spaceBefore=15
            )
            
            normal_style = ParagraphStyle(
                'NormalStyle',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_LEFT,
                spaceAfter=5
            )
            
            for date, daily_sales in all_month_sales:
                # Day header
                daily_total = sum(sale.amount for sale in daily_sales)
                story.append(Paragraph(
                    f"{date.strftime('%A, %B %d, %Y')} - {len(daily_sales)} sales - {daily_total:.2f} RON", 
                    day_style
                ))
                
                # Sales for that day
                for idx, sale in enumerate(daily_sales, 1):
                    dt = datetime.fromisoformat(sale.timestamp)
                    story.append(Paragraph(
                        f"&nbsp;&nbsp;&nbsp;&nbsp;{idx}. {sale.doc} - {sale.amount:.2f} RON ({dt.strftime('%H:%M')})", 
                        normal_style
                    ))
                
                story.append(Spacer(1, 10))
            
            # Final summary
            summary_style = ParagraphStyle(
                'SummaryStyle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                spaceAfter=10,
                spaceBefore=20
            )
            story.append(Paragraph(f"<b>MONTHLY TOTAL: {total_month_amount:.2f} RON</b>", summary_style))
            story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            
            doc.build(story)
            messagebox.showinfo("Success", f"Monthly sales report exported to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export monthly sales:\n{str(e)}")


