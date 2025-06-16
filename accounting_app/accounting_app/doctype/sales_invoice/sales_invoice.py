from accounting_app.accounting_app.controllers.accounting_controller import AccountingController

class SalesInvoice(AccountingController):
    
    def before_save(self):
        self.calculate_totals()

    def make_gl_entries(self):

        #debit entry
        self._create_gl_entry(
            posting_date=self.posting_date,
            account=self.debit_to,
            party=self.customer,
            debit=self.total_amount,
            credit=0,
            due_date=self.payment_due_date
        )

        #credit entry
        self._create_gl_entry(
            posting_date=self.posting_date,
            account=self.income_account,
            party=self.customer,
            debit=0,
            credit=self.total_amount
        )

    def calculate_totals(self):
        total_qty = 0
        total_amount = 0
        for item_row in self.get("items"):
            total_qty += float(item_row.qty or 0)
            total_amount += float(item_row.amount or 0)
        self.total_qty = total_qty
        self.total_amount = total_amount