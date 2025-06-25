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
            account=self.credit_to,
            party=self.supplier,
            debit=0,
            credit=self.total_amount,
            due_date=self.payment_due_date
        )
        debit_account_totals = {}

        for item in self.get("items"):
            if item.is_stock:
                debit_account = item.stock_account 
            else:
                debit_account = item.expense_account
            
            debit_account_totals.setdefault(debit_account, 0)
            debit_account_totals[debit_account] += item.amount

        for account, total_debit in debit_account_totals.items():
            if total_debit > 0:
                self._create_gl_entry(
                    posting_date=self.posting_date,
                    account=account,
                    party=self.supplier,
                    debit=total_debit,
                    credit=0
                )
            

    def make_stock_ledger_entries(self):
        for item in self.get("items"):
            maintain_stock = frappe.db.get_value("Item", item.item, "maintain_stock")

            if maintain_stock:
                sle = frappe.new_doc("Stock Ledger Entry")
                sle.item = item.item
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
            maintain_stock = frappe.db.get_value("Item", item.item, "maintain_stock")

            if maintain_stock:
                sle = frappe.new_doc("Stock Ledger Entry")
                sle.item = item.item
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



