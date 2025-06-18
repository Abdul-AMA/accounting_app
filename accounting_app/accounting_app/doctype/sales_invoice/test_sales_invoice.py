import frappe
from ...tests.base import AccountingTestCase


class IntegrationTestSalesInvoice(AccountingTestCase):
    
    def test_submission_creates_balanced_gl_entries(self):
        si = frappe.get_doc({
            "doctype": "Sales Invoice", "customer": self.customer,
            "posting_date": frappe.utils.today(), "payment_due_date": frappe.utils.today(),  
            "debit_to": self.receivable_account, "income_account": self.income_account,
            "items": [{"item": self.test_item, "qty": 2, "rate": 5000, "amount": 10000}]
        }).insert()
        si.submit()

        self.assertVoucherBalanced(si.doctype, si.name)
        expected_entries = [
            {"account": self.receivable_account, "debit": 10000},
            {"account": self.income_account, "credit": 10000}
        ]
        self.assertGLEntries(si.doctype, si.name, expected_entries)

    def test_cancellation_reverses_gl_entries(self):
        si = frappe.get_doc({
            "doctype": "Sales Invoice", "customer": self.customer,
            "posting_date": frappe.utils.today(), "payment_due_date": frappe.utils.today(),
            "debit_to": self.receivable_account, "income_account": self.income_account,
            "items": [{"item": self.test_item, "qty": 1, "rate": 100, "amount": 100}]
        }).insert()
        si.submit()

        si.cancel()

        self.assertNetEffectIsZero(si.doctype, si.name)