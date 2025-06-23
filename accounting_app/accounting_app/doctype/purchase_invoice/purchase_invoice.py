import frappe
from ...controllers.AccountingController import AccountingController

class PurchaseInvoice(AccountingController):

    def before_save(self):
        self.calculate_totals()

    def on_submit(self):
        self.make_gl_entries()
        self.make_stock_ledger_entries()

    def on_cancel(self):
        super().on_cancel()
        self.make_reverse_stock_ledger_entries()

    def make_gl_entries(self):        
        self._create_gl_entry(
            posting_date=self.posting_date,
            account= self.debit_to,
            party=self.supplier,
            debit=self.total_amount,
            credit=0
        )

        self._create_gl_entry(
            posting_date=self.posting_date,
            account=self.credit_to,
            party=self.supplier,
            debit=0,
            credit=self.total_amount,
            due_date=self.payment_due_date
        )

    def make_stock_ledger_entries(self):
        for item in self.get("items"):
            maintain_stock = frappe.db.get_value("Item", item.item_code, "maintain_stock")

            if maintain_stock:
                sle = frappe.new_doc("Stock Ledger Entry")
                sle.item = item.item_code
                sle.warehouse = item.warehouse
                sle.posting_date = self.posting_date
                sle.actual_qty = item.qty  
                sle.valuation_rate = item.rate 
                sle.voucher_type = self.doctype
                sle.voucher_number = self.name
                sle.insert(ignore_permissions=True)
                sle.submit()

    def make_reverse_stock_ledger_entries(self):
        for item in self.get("items"):
            maintain_stock = frappe.db.get_value("Item", item.item_code, "maintain_stock")

            if maintain_stock:
                sle = frappe.new_doc("Stock Ledger Entry")
                sle.item = item.item_code
                sle.warehouse = item.warehouse
                sle.posting_date = self.posting_date
                sle.actual_qty = -item.qty
                sle.valuation_rate = item.rate
                sle.voucher_type = self.doctype
                sle.voucher_number = self.name
                sle.remark = f"Reversal for cancellation of {self.name}"
                sle.insert(ignore_permissions=True)
                sle.submit()


    def calculate_totals(self):

        total_qty = 0
        total_amount = 0
        for item_row in self.get("items"):
            total_qty += float(item_row.qty or 0)
            total_amount += float(item_row.amount or 0)
            
        self.total_qty = total_qty
        self.total_amount = total_amount



