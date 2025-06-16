import frappe
from frappe.model.document import Document
from utils.gl_entries_control import create_gl_entry,reverse_gl_entries

class SalesInvoice(Document):
    def before_save(self):
        self.calculate_totals()


    def on_submit(self):
        # Debit Entry
        create_gl_entry(self.posting_date,self.debit_to,self.customer,self.total_amount,0,self.doctype,self.name,self.payment_due_date ,None)


        # Credit Entry
        create_gl_entry(self.posting_date,self.income_account,self.customer,0,self.total_amount,self.doctype,self.name, None ,None)


    def on_cancel(self):
        #create reverse entry
        reverse_gl_entries(self.doctype,self.name,self.posting_date)

 

    def calculate_totals(self):
        
        total_qty = 0
        total_amount = 0
        for item_row in self.get("items"):
            total_qty += float(item_row.qty or 0)
            total_amount += float(item_row.amount or 0)

        self.total_qty = total_qty
        self.total_amount = total_amount
