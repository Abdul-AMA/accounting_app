import frappe
from accounting_app.accounting_app.controllers.accounting_controller import AccountingController

class JournalEntry(AccountingController):

    def validate(self):
        self.calculate_and_validate_totals()

    def make_gl_entries(self):
        for entry in self.get("accounting_entries"):
            if entry.debit or entry.credit:
                self._create_gl_entry(
                    posting_date=self.posting_date,
                    account=entry.account,
                    party=entry.party,
                    debit=entry.debit,
                    credit=entry.credit,
                    remark=entry.description_of_transaction
                )

    def calculate_and_validate_totals(self):
        total_debit = 0
        total_credit = 0
        for entry in self.get("accounting_entries"):
            total_debit += float(entry.debit or 0)
            total_credit += float(entry.credit or 0)

        self.total_debit = total_debit
        self.total_credit = total_credit

        if self.total_debit != self.total_credit:
            frappe.throw("Total debit should equal total credit !!!!!!")