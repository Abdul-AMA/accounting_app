import frappe
from ...tests.base import AccountingTestCase

class IntegrationTestJournalEntry(AccountingTestCase):
    def test_journal_entry_posting(self):
        je = frappe.get_doc({
            "doctype": "Journal Entry", "posting_date": frappe.utils.today(),
            "accounting_entries": [
                { "account": self.bank_account, "debit": 100000},
                { "account": self.expense_account, "debit": 15000},
                { "account": self.payable_account, "credit": 115000}
            ]
        }).insert()
        je.submit()

        self.assertVoucherBalanced(je.doctype, je.name)
        expected_entries = [
            {"account": self.bank_account, "debit": 100000},
            {"account": self.expense_account, "debit": 15000},
            {"account": self.payable_account, "credit": 115000}
        ]
        self.assertGLEntries(je.doctype, je.name, expected_entries)