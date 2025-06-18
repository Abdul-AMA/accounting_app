import frappe
from ...tests.base import AccountingTestCase

class IntegrationTestJournalEntry(AccountingTestCase):

    def test_journal_entry_posting(self):
        je = frappe.get_doc({
            "doctype": "Journal Entry", "posting_date": frappe.utils.today(),
            "accounting_entries": [
                { "account": self.bank_account, "debit": 10000},
                { "account": self.expense_account, "credit": 10000}
            ]
        }).insert()
        je.submit()
        
        self.assertVoucherBalanced(je.doctype, je.name)
        expected_entries = [
            {"account": self.bank_account, "debit": 10000},
            {"account": self.expense_account, "credit": 10000}
        ]
        self.assertGLEntries(je.doctype, je.name, expected_entries)

    def test_journal_entry_cancellation(self):
        je = frappe.get_doc({
            "doctype": "Journal Entry", "posting_date": frappe.utils.today(),
            "accounting_entries": [
                { "account": self.receivable_account, "debit": 250},
                { "account": self.income_account, "credit": 250}
            ]
        }).insert()
        je.submit()

        je.cancel()
        self.assertNetEffectIsZero(je.doctype, je.name)


    def test_unbalanced_journal_entry_is_rejected(self):
        """Tests that creating an unbalanced Journal Entry raises a ValidationError."""

        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Journal Entry",
                "posting_date": frappe.utils.today(),
                "accounting_entries": [
                    { "account": self.bank_account, "debit": 1000},
                    { "account": self.expense_account, "credit": 999} 
                ]
            }).insert()