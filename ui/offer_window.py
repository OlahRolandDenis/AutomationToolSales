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