import frappe
from frappe.model.document import Document

class JournalEntry(Document):
    def validate(self):
        total_debit = 0
        total_credit = 0
        for entry in self.get("accounting_entries"):
            total_debit += float(entry.debit or 0)
            total_credit += float(entry.credit or 0)

        self.total_debit = total_debit
        self.total_credit = total_credit

        if self.total_debit != self.total_credit:
            frappe.throw("Total Debit must equal Total Credit.")