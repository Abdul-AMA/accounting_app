# Copyright (c) 2025, abood-ama and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesInvoice(Document):
    def before_save(self):
        self.calculate_totals()

    def calculate_totals(self):
        total_qty = 0
        total_amount = 0
        for item_row in self.get("items"): 
            
            item_row.amount = flt(item_row.quantity) * flt(item_row.rate) 

            total_qty += float(item_row.quantity or 0)
            total_amount += float(item_row.amount or 0)

        self.total_qty = total_qty
        self.total_amount = total_amount
