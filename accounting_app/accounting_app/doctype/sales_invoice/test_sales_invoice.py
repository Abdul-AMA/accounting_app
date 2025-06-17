import frappe
from ...tests.base import AccountingTestCase

class IntegrationTestSalesInvoice(AccountingTestCase):
    
    def test_gl_posting_and_cancellation(self):
        si = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": self.customer,
            "posting_date": frappe.utils.today(),
            "debit_to": self.receivable_account,
            "income_account": self.income_account,
            "items": [{"item_code": self.test_item, "qty": 2, "rate": 5000, "amount": 10000}]
        }).insert()
        si.submit()

        self.assertVoucherBalanced(si.doctype, si.name)
        
        expected_entries = [
            {"account": self.receivable_account, "debit": 10000, "credit": 0},
            {"account": self.income_account, "debit": 0, "credit": 10000}
        ]
        self.assertGLEntries(si.doctype, si.name, expected_entries)

        si.cancel()
        
        self.assertNetEffectIsZero(si.doctype, si.name)