import frappe
from ...tests.base import AccountingTestCase

class IntegrationTestPurchaseInvoice(AccountingTestCase):
    def test_purchase_gl_posting_and_cancellation(self):
        pi = frappe.get_doc({
            "doctype": "Purchase Invoice", "supplier": self.supplier,
            "posting_date": frappe.utils.today(), "credit_to": self.payable_account,
            "expense_account": self.expense_account,
            "items": [{"item_code": self.test_item, "qty": 10, "rate": 1500, "amount": 15000}]
        }).insert()
        pi.submit()

        self.assertVoucherBalanced(pi.doctype, pi.name)
        expected_entries = [
            {"account": self.expense_account, "debit": 15000},
            {"account": self.payable_account, "credit": 15000}
        ]
        self.assertGLEntries(pi.doctype, pi.name, expected_entries)

        pi.cancel()
        self.assertNetEffectIsZero(pi.doctype, pi.name)