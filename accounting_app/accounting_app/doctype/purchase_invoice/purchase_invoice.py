import frappe
from frappe.model.document import Document

class PurchaseInvoice(Document):
    # This method is automatically called by Frappe just before saving the document
    def before_save(self):
        self.calculate_totals()

    def calculate_totals(self):
        
        total_qty = 0
        total_amount = 0
        for item_row in self.get("items"):
            total_qty += float(item_row.qty or 0)
            total_amount += float(item_row.amount or 0)

        self.total_qty = total_qty
        self.total_amount = total_amount
