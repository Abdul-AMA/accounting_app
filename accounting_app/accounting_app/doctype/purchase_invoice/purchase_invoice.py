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


    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_reverse_gl_entries()

    def make_gl_entries():

        # Create the Debit Entry 
        debit_entry = frappe.new_doc("GL Entry")
        debit_entry.posting_date = self.posting_date
        debit_entry.account = self.expense_account
        debit_entry.party = self.supplier
        debit_entry.debit_amount = self.total_amount
        debit_entry.credit_amount = 0
        debit_entry.voucher_type = self.doctype
        debit_entry.voucher_number = self.name
        debit_entry.insert(ignore_permissions=True)
        debit_entry.submit()

        # Create the Credit Entry 
        credit_entry = frappe.new_doc("GL Entry")
        credit_entry.posting_date = self.posting_date
        credit_entry.due_date = self.payment_due_date 
        credit_entry.account = self.credit_to     
        credit_entry.party = self.supplier
        credit_entry.debit_amount = 0
        credit_entry.credit_amount = self.total_amount
        credit_entry.voucher_type = self.doctype
        credit_entry.voucher_number = self.name
        credit_entry.insert(ignore_permissions=True)
        credit_entry.submit()

    
    def make_reverse_gl_entries(self):
            original_entries = frappe.get_all("GL Entry",
                filters={
                    'voucher_type': self.doctype,
                    'voucher_number': self.name,
                    'is_cancelled': 0
                },
                fields=["name", "account", "party", "credit_amount", "debit_amount", "due_date"]
            )

            for entry in original_entries:
                reverse_entry = frappe.new_doc("GL Entry")
                reverse_entry.posting_date = self.posting_date
                reverse_entry.account = entry.account
                reverse_entry.party = entry.party
                reverse_entry.due_date = entry.due_date

                reverse_entry.debit_amount = entry.credit_amount
                reverse_entry.credit_amount = entry.debit_amount

                reverse_entry.voucher_type = self.doctype
                reverse_entry.voucher_number = self.name
                reverse_entry.remark = "Reversal entry for cancellation of " + self.name
                reverse_entry.insert(ignore_permissions=True)
                reverse_entry.submit()

                frappe.db.set_value("GL Entry", entry.name, "is_cancelled", 1)
