import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

class OfferDetailWindow(ctk.CTkToplevel):
    def __init__(self, parent, offer, offer_service):
        super().__init__(parent)
        self.offer = offer
        self.offer_service = offer_service
        self.parent_window = parent
        
        self.title(f"Offer Details - {offer.cif}")
        self.geometry("1200x800")
        self.configure(fg_color=parent.colors['primary'])
        
        self.colors = parent.colors
        
        # Company data (you should replace this with your actual company data)
        self.company_data = {
            'name': 'SC AUTO & AGRO MAGMANN SRL',
            'registration_number': 'Nr.ord.reg.com.: 02/52/21/2014',
            'cif': 'RO-33249865',
            'address': 'ARAD Str. CALE A RADNEI Nr.237 Judet ARAD',
            'account': 'RO36BTRLRONCRT0257372202',
            'bank': 'TRANSILVANIA RON / BRD',
            'phone': '0720961818-ARAD; 0790687201-INEU',
            'capital': '200'
        }
        
        self.create_widgets()
        self.load_offer_data()
        
    def create_widgets(self):
        header_frame = ctk.CTkFrame(
            self,
            height=80,
            fg_color=self.colors['dark_gray'],
            corner_radius=0
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_info = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_info.pack(side="left", fill="y", padx=25, pady=15)
        
        title_label = ctk.CTkLabel(
            header_info,
            text=f"Offer Details - CIF: {self.offer.cif}",
            font=("Arial", 20, "bold"),
            text_color=self.colors['primary']
        )
        title_label.pack(anchor="w")
        
        date_label = ctk.CTkLabel(
            header_info,
            text=f"Created: {datetime.fromisoformat(self.offer.timestamp).strftime('%Y-%m-%d %H:%M')}",
            font=("Arial", 12),
            text_color=self.colors['primary']
        )
        date_label.pack(anchor="w")
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        products_header = ctk.CTkLabel(
            left_frame,
            text="Products in Offer",
            font=("Arial", 16, "bold"),
            text_color=self.colors['secondary']
        )
        products_header.pack(pady=15)
        
        tree_frame = ctk.CTkFrame(left_frame, fg_color=self.colors['primary'])
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ('ID', 'Code', 'Name', 'Qty', 'Unit Price', 'VAT%', 'Total')
        self.products_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings'
        )
        
        column_configs = {
            'ID': (50, 'center'),
            'Code': (100, 'w'),
            'Name': (200, 'w'),
            'Qty': (80, 'center'),
            'Unit Price': (100, 'e'),
            'VAT%': (80, 'center'),
            'Total': (120, 'e')
        }
        
        for col, (width, anchor) in column_configs.items():
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=width, anchor=anchor)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        right_frame = ctk.CTkFrame(main_frame, width=400)
        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(right_frame, width=380)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        add_section = ctk.CTkFrame(self.scrollable_frame)
        add_section.pack(fill="x", padx=10, pady=20)
        
        add_header = ctk.CTkLabel(
            add_section,
            text="Add New Product",
            font=("Arial", 14, "bold"),
            text_color=self.colors['secondary']
        )
        add_header.pack(pady=10)
        
        self.create_product_form(add_section)
        
        self.create_action_buttons(self.scrollable_frame)
        
        self.create_export_buttons(self.scrollable_frame)
        
        self.create_total_section(self.scrollable_frame)
    
    def create_product_form(self, parent):
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(form_frame, text="Code:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.product_code_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.product_code_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Name:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.product_name_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.product_name_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Quantity:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.quantity_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.quantity_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Unit Price:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.unit_price_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.unit_price_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="VAT %:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.vat_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.vat_entry.pack(pady=(0, 10))
    
    def create_action_buttons(self, parent):
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=20)
        
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="Add Product",
            command=self.add_product,
            width=340,
            height=40,
            fg_color="#28a745",
            hover_color="#218838"
        )
        add_btn.pack(pady=5)
        
        update_btn = ctk.CTkButton(
            buttons_frame,
            text="Update Selected",
            command=self.update_selected_product,
            width=340,
            height=40,
            fg_color="#17a2b8",
            hover_color="#138496"
        )
        update_btn.pack(pady=5)
        
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_selected_product,
            width=340,
            height=40,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(pady=5)
        
        fill_btn = ctk.CTkButton(
            buttons_frame,
            text="Fill Form from Selection",
            command=self.fill_form_from_selection,
            width=340,
            height=35,
            fg_color="#6c757d",
            hover_color="#545b62"
        )
        fill_btn.pack(pady=5)
    
    def create_export_buttons(self, parent):
        export_frame = ctk.CTkFrame(parent, fg_color="transparent")
        export_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        export_header = ctk.CTkLabel(
            export_frame,
            text="Export Options",
            font=("Arial", 14, "bold"),
            text_color=self.colors['secondary']
        )
        export_header.pack(pady=(10, 15))
        
        csv_btn = ctk.CTkButton(
            export_frame,
            text="📊 Export CSV",
            command=self.export_csv,
            width=340,
            height=40,
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        csv_btn.pack(pady=5)
        
        pdf_btn = ctk.CTkButton(
            export_frame,
            text="📄 Export PDF",
            command=self.export_pdf,
            width=340,
            height=40,
            fg_color="#fd7e14",
            hover_color="#e8650e"
        )
        pdf_btn.pack(pady=5)
        
        offer_doc_btn = ctk.CTkButton(
            export_frame,
            text="📋 Generate Offer Document",
            command=self.generate_offer_document,
            width=340,
            height=40,
            fg_color="#20c997",
            hover_color="#17a085"
        )
        offer_doc_btn.pack(pady=5)
    
    def create_total_section(self, parent):
        total_frame = ctk.CTkFrame(parent)
        total_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        self.total_label = ctk.CTkLabel(
            total_frame,
            text="Total: 0.00 RON",
            font=("Arial", 16, "bold"),
            text_color=self.colors['secondary']
        )
        self.total_label.pack(pady=20)

    def load_offer_data(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        if self.offer.products:
            for prod in products:
                price_total = self.calulate_offer_price(prod.quantity,prod.unit_price,prod.vat)

                self.products_tree.insert('', 'end', values=(
                    product.id,                          
                    product.product_code,                
                    product.product_name,               
                    product.quantity,                    
                    f"{product.unit_price:.2f}",        
                    f"{product.vat:.1f}",               
                    f"{line_total:.2f}"                
                ))
            total = self.calculate_total_price()
            self.total_label.configure(text=f"Total: {total['final_total']:.2f} RON")

    def reload_offer(self):
        try:
            offers = self.offer_service.get_offers_by_user(self.offer.user_id)

            new_offer = None

            for o in offers :
                if self.offer.id == o.id:
                    new_offer = o
                    break
            if new_offer:
                self.offer = new_offer
                self.load_offer_data()
            else:
                messagebox.showerror("Error", "Offer no longer exists")
                self.destroy() 
        except Exception as e:
            messagebox.showerror("Error", "Failed to reload")

    def  add_product(self):
        is_valid, message  = slef.vallidate_form()

        if not valid:
            messagebox.showerror("Error", "Form is not ok")
            return
        
        code = self.product_code_entry.get().strip()
        name = self.product_name_entry.get().strip()
        quantity = float(self.product_quantity_entry.get().strip())
        unit_price = float(self.product_unit_price_entry.get().strip())
        vat = float(self.product_vat_entry.get().strip())


        try:
            success = slef.offer_service.add_product(self.offer.id,code, name, quantity,unit_price,vat)
            # i need to create the add_product() function in the offer_serivice

            if success:
                 messagebox.showeinfo("Success", "Product added")
                 self.reload_offer()
                 self.load_offer_data()
                 self.parent_window.load_offer_data()
            else:
                messagebox.showeerror("Error", "Product not added")
        except Exception as e:
            messagebox.showeerror("Error", "Failed to add product")

        


            


        

    





