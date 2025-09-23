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
import random

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
        self.product_quantity_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.product_quantity_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Unit Price:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.product_unit_price_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.product_unit_price_entry.pack(pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="VAT %:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.product_vat_entry = ctk.CTkEntry(form_frame, width=350, height=35)
        self.product_vat_entry.pack(pady=(0, 10))
    
    def create_action_buttons(self, parent):
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=20)
        
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="Add Product",
            command=self.add_product,
            width=340,
            height=40,
            fg_color=self.colors['dark_gray'],
            hover_color=self.colors['text_secondary']
        )
        add_btn.pack(pady=5)
        
        update_btn = ctk.CTkButton(
            buttons_frame,
            text="Update Selected",
            command=self.update_selected_product,
            width=340,
            height=40,
            fg_color=self.colors['accent'],
            hover_color=self.colors['text_secondary']
        )
        update_btn.pack(pady=5)
        
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_selected_product,
            width=340,
            height=40,
            fg_color=self.colors['dark_gray'],
            hover_color=self.colors['text_secondary']
        )
        delete_btn.pack(pady=5)
        
        
        delete_offer_btn = ctk.CTkButton(
            buttons_frame,
            text="Delete Offer",
            command=self.delete_offer,
            width=340,
            height=40,
            fg_color=self.colors['dark_gray'],
            hover_color=self.colors['text_secondary']
        )
        delete_offer_btn.pack(pady=5)
        
        fill_btn = ctk.CTkButton(
            buttons_frame,
            text="Fill Form from Selection",
            command=self.fill_form_from_selection,
            width=340,
            height=35,
            fg_color=self.colors['text_secondary'],
            hover_color=self.colors['dark_gray']
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
        
        offer_doc_btn = ctk.CTkButton(
            export_frame,
            text="Generate Offer Document",
            command=self.generate_offer_document,
            width=340,
            height=40,
            fg_color=self.colors['accent'],
            hover_color=self.colors['text_secondary']
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
            for prod in self.offer.products:
                price_total = self.calculate_offer_price(prod.quantity,prod.unit_price,prod.vat)

                self.products_tree.insert('', 'end', values=(
                    prod.id,                          
                    prod.product_code,                
                    prod.product_name,               
                    prod.quantity,                    
                    f"{prod.unit_price:.2f}",        
                    f"{prod.vat:.1f}",               
                    f"{price_total:.2f}"                
                ))
            total = self.calculate_total_price()
            self.total_label.configure(text=f"Total: {total['final_total']:.2f} RON")

    def calculate_offer_price(self,quantity, unit_price, vat):
        subtotal = quantity * unit_price
        total_with_vat = subtotal * (1 + vat / 100)
        return round(total_with_vat, 2)
    
    def calculate_total_price(self):
        total = 0.0
        vat_total = 0.0

        if self.offer.products:
            for prod in self.offer.products:

                prod_total = prod.quantity * prod.unit_price
                prod_total_vat = prod_total * (prod.vat / 100)

                total = total + prod_total
                vat_total = vat_total + prod_total_vat

        final_total = total + vat_total
        return {
            'subtotal': round(total, 2),      
            'vat_total': round(vat_total, 2),    
            'final_total': round(final_total, 2) 
        }


    def reload_offer(self):
        try:
            offers = self.offer_service.get_offers_by_user_by_id(self.offer.user_id)

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
        is_valid  = self.validate_form()

        if not is_valid:
            messagebox.showerror("Error", "Form is not ok")
            return
        
        code = self.product_code_entry.get().strip()
        name = self.product_name_entry.get().strip()
        quantity = float(self.product_quantity_entry.get().strip())
        unit_price = float(self.product_unit_price_entry.get().strip())
        vat = float(self.product_vat_entry.get().strip())


        try:
            success = self.offer_service.add_product(self.offer.id,code, name, quantity,unit_price,vat)

            if success:
                
                messagebox.showinfo("Success", "Product added")
                self.reload_offer()
                self.load_offer_data()
                self.parent_window.load_saved_offers()
            else:
                messagebox.showerror("Error", "Product not added")
        except Exception as e:
            messagebox.showerror("Error", "Failed to add product")


    def validate_form(self):
        code = self.product_code_entry.get().strip()
        name = self.product_name_entry.get().strip()
        quantity = self.product_quantity_entry.get().strip()
        unit_price = self.product_unit_price_entry.get().strip()
        vat = self.product_vat_entry.get().strip()

        if not code or not name or not quantity or not unit_price or not vat:
            messagebox.showerror("Error", "Please fill all fields")
            return False

        try:
            quantity = float(quantity)
            unit_price = float(unit_price)
            vat = float(vat)

            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return False

            if unit_price <= 0:
                messagebox.showerror("Error", "Price must be positive")
                return False

            if vat <= 0 or vat >=100:
                messagebox.showerror("Error", "Vat must be between 0 and 100")
                return False
        except Exception as e:
        

            messagebox.showerror("Error", "Invalid number format")
            return False
        
        return True
    
    def update_selected_product(self):
        selection = self.products_tree.selection()

        if not selection:
            messagebox.showerror("Error", "Select offer")
            return

        is_valid = self.validate_form()

        if not is_valid:
            messagebox.showerror("Error", "Complete all forms")
            return

        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]

        code = self.product_code_entry.get().strip()
        name = self.product_name_entry.get().strip()
        quantity = float(self.product_quantity_entry.get().strip())
        unit_price = float(self.product_unit_price_entry.get().strip())
        vat = float(self.product_vat_entry.get().strip())

        try:
            success = self.offer_service.update_product(product_id, code, name, quantity, unit_price, vat)

            if success:

                messagebox.showinfo("Success", "Product updated")
                self.reload_offer()
                self.load_offer_data()
                self.parent_window.load_saved_offers()
            else:
                messagebox.showerror("Error", "Failed to update product")
        except Exception as e:
            messagebox.showerror("Error", "Failed to update product")

    def delete_selected_product(self):
        selection = self.products_tree.selection()

        if not selection:
            messagebox.showerror("Error", "Select offer")
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            return


        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]

        try:
            success = self.offer_service.delete_product(product_id)

            if success:
                messagebox.showinfo("Success", "Product deleted")
                self.reload_offer()
                self.load_offer_data()
                self.parent_window.load_saved_offers()
            else:
                messagebox.showerror("Error", "Failed to delete product")
        except Exception as e:
            messagebox.showerror("Error", "Failed to delete product")


    def fill_form_from_selection(self):
        selection = self.products_tree.selection()

        if not selection:
            messagebox.showerror("Error", "Select offer")
            return

        item = self.products_tree.item(selection[0])
        values = item['values']

        self.clear_form()

            
        self.product_code_entry.insert(0, values[1])
        self.product_name_entry.insert(0, values[2])
        self.product_quantity_entry.insert(0,str(values[3]))
        self.product_unit_price_entry.insert(0,str(values[4]))
        self.product_vat_entry.insert(0,str(values[5]))

    def clear_form(self):
        self.product_code_entry.delete(0, 'end')
        self.product_name_entry.delete(0, 'end')
        self.product_quantity_entry.delete(0, 'end')
        self.product_unit_price_entry.delete(0, 'end')
        self.product_vat_entry.delete(0, 'end')

    def generate_invoice_number(self):
        return str(random.randint(1000000,9999999))

    def delete_offer(self):
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this offer?"):
            return

        try:
            if not self.offer_service.delete_offer(self.offer.id):
                messagebox.showerror("Error", "Could not delete offer")
                return
            else:
                self.parent_window.load_saved_offers()
                self.destroy()
                messagebox.showinfo("Success", "Offer deleted")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete offer: {e}")




    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.units import cm
    from datetime import datetime
    from tkinter import filedialog, messagebox

    def generate_offer_document(self):
        """Generate professional offer document identical to reference image (with logo)"""
        try:
            # Save file dialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save Offer Document"
            )
            if not file_path:
                return

            doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
            styles = getSampleStyleSheet()
            story = []

            # === HEADER COMPANIE ===
            header_left = [
                [Paragraph("<b>SC AUTO & AGRO MAGMANN SRL</b>", styles['Normal'])],
                [Paragraph(f"Nr.ord.reg.com.: {self.company_data['registration_number']}", styles['Normal'])],
                [Paragraph(f"C.I.F.: {self.company_data['cif']}", styles['Normal'])],
                [Paragraph(f"Sediul: {self.company_data['address']}", styles['Normal'])],
                [Paragraph(f"Contul: {self.company_data['account']}", styles['Normal'])],
                [Paragraph(f"Banca: {self.company_data['bank']}", styles['Normal'])],
                [Paragraph("Contul: RO70INGB0000999908841201", styles['Normal'])],
                [Paragraph("Banca: ING BANK ARAD", styles['Normal'])],
                [Paragraph(f"Capital social (RON): {self.company_data['capital']}", styles['Normal'])],
                [Paragraph(f"Telefon: {self.company_data['phone']}", styles['Normal'])],
            ]

            # === Logo + info dreapta ===
            logo_path = "utils/logo.png"  # aici pui path-ul real către logo-ul tău
            logo = Image(logo_path, width=3*cm, height=3*cm)

            header_right = [
                [logo],
                [Paragraph("<b>AGRO MAGMANN</b>", styles['Normal'])],
                [Paragraph("www.agromagmann.ro", styles['Normal'])],
                [Paragraph("<b>OFERTA DE PRET</b>", styles['Normal'])],
                [Paragraph("Seria MAG", styles['Normal'])],
                [Paragraph(f"Factura nr. {self.generate_invoice_number()}", styles['Normal'])],
                [Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal'])],
                [Paragraph(f"Pozitii factura: {len(self.offer.products) if hasattr(self.offer, 'products') else 0}", styles['Normal'])]
            ]

            company_table = Table([[header_left, header_right]], colWidths=[10*cm, 7*cm])
            company_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
            ]))
            story.append(company_table)
            story.append(Spacer(1, 10))

            # === CLIENT ===
            client_title = Paragraph("<i>Cumparator - Client</i>", ParagraphStyle(
                'ClientTitle', fontSize=9, textColor=colors.grey, alignment=TA_LEFT
            ))
            story.append(client_title)

            client_data = [
                [f"{getattr(self.offer, 'client_name', 'ZETOR TRACTOR SRL')}", "", "", f"C.I.F. {self.offer.cif}"],
                [f"Adresa: {getattr(self.offer, 'client_address', 'STR. CARTIERUL NOU 19')}", "", "", "Nr.reg.com.:"],
                [f"Tara/Localitate: RO / {getattr(self.offer, 'client_city', 'NADLAC')} Judetul: ARAD", "", "", "Contul:"],
                [f"Adresa de livrare: IDEM", "", "", f"Telefon: {getattr(self.offer, 'client_phone', '0726353544')}"],
            ]

            client_table = Table(client_data, colWidths=[9*cm, 2*cm, 2*cm, 5*cm])
            client_table.setStyle(TableStyle([
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(client_table)
            story.append(Spacer(1, 15))

            # === PRODUSE ===
            products_header = [[
                'Nr crt.', 'Denumirea produselor sau a serviciilor', 'U.M.',
                'Cantitate', 'Pret unitar fara TVA RON', 'Valoare fara TVA RON',
                'Cota TVA %', 'Valoare T.V.A. RON'
            ]]

            totals = self.calculate_total_price()

            if hasattr(self.offer, 'products') and self.offer.products:
                for idx, product in enumerate(self.offer.products, 1):
                    value_without_vat = product.quantity * product.unit_price
                    vat_value = value_without_vat * (product.vat / 100)

                    products_header.append([
                        str(idx),
                        f"{product.product_code} - {product.product_name}",
                        "BUC",
                        f"{product.quantity:.4f}",
                        f"{product.unit_price:.4f}",
                        f"{value_without_vat:.2f}",
                        str(int(product.vat)),
                        f"{vat_value:.2f}"
                    ])

            # Subtotal + TVA
            products_header.append([
                "", "", "", "", "", f"{totals['subtotal']:.2f}", "", f"{totals['vat_total']:.2f}"
            ])

            # Total RON
            products_header.append([
                "", "", "", "", "TOTAL RON:", "", "", f"{totals['final_total']:.2f}"
            ])

            products_table = Table(products_header,
                                colWidths=[1.2*cm, 6*cm, 1.2*cm, 2*cm, 3*cm, 3*cm, 1.5*cm, 2.5*cm])
            products_table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),

                # Rows
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (2, 1), (7, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -3), 'LEFT'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),

                # Totals
                ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, -2), (-1, -2), colors.whitesmoke),
                ('BACKGROUND', (0, -1), (-1, -1), colors.whitesmoke),

                # Borders
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))

            story.append(products_table)

            # Build PDF
            doc.build(story)
            messagebox.showinfo("Success", f"Offer document generated successfully at {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate offer document: {str(e)}")


        

















            

        


        


            


        

    





