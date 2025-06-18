import frappe
from ...tests.base import AccountingTestCase

class IntegrationTestPurchaseInvoice(AccountingTestCase):

    def test_submission_creates_balanced_gl_entries(self):
        pi = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": self.supplier,
            "posting_date": frappe.utils.today(),
            "payment_due_date": frappe.utils.today(),
            "credit_to": self.payable_account,
            "expense_account": self.expense_account,
            "items": [{"item": self.test_item, "qty": 10, "rate": 1500, "amount": 15000}]
        }).insert()
        pi.submit()

        self.assertVoucherBalanced(pi.doctype, pi.name)
        expected_entries = [
            {"account": self.expense_account, "debit": 15000},
            {"account": self.payable_account, "credit": 15000}
        ]
        self.assertGLEntries(pi.doctype, pi.name, expected_entries)

    def test_cancellation_reverses_gl_entries(self):
        pi = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": self.supplier,
            "posting_date": frappe.utils.today(),
            "payment_due_date": frappe.utils.today(),
            "credit_to": self.payable_account,
            "expense_account": self.expense_account,
            "items": [{"item": self.test_item, "qty": 5, "rate": 100, "amount": 500}]
        }).insert()
        pi.submit()

        pi.cancel()
        self.assertNetEffectIsZero(pi.doctype, pi.name)