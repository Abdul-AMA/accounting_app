
import frappe
from frappe.model.document import Document

class AccountingController(Document):


    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_reverse_gl_entries()

    def make_gl_entries(self):

        frappe.throw(f"The 'make_gl_entries' method has not been implemented for {self.doctype}")

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
            self._create_gl_entry(
                posting_date=self.posting_date,
                due_date=entry.due_date,
                account=entry.account,
                party=entry.party,
                debit=entry.credit_amount, 
                credit=entry.debit_amount, 
                remark=f"Reversal for cancellation of {self.name}"
            )

            original_gl_doc = frappe.get_doc("GL Entry", entry.name)
            original_gl_doc.is_cancelled = 1
            original_gl_doc.save(ignore_permissions=True)



    def _create_gl_entry(self, posting_date, account, party, debit, credit, due_date=None, remark=None):

        entry = frappe.new_doc("GL Entry")
        entry.posting_date = posting_date
        entry.due_date = due_date
        entry.account = account
        entry.party = party
        entry.debit_amount = debit
        entry.credit_amount = credit
        entry.voucher_type = self.doctype
        entry.voucher_number = self.name
        entry.remark = remark
        entry.insert(ignore_permissions=True)
        entry.submit()
        return entry.name