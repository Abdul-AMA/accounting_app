import frappe
from ...tests.base import AccountingTestCase

class IntegrationTestPaymentEntry(AccountingTestCase):

    def test_receive_payment_submission(self):
        pe = frappe.get_doc({
            "doctype": "Payment Entry", "payment_type": "Receive",
            "posting_date": frappe.utils.today(), "party": self.customer,
            "account_paid_from": self.receivable_account, "account_paid_to": self.bank_account,
            "amount": 500
        }).insert()
        pe.submit()
        self.assertVoucherBalanced(pe.doctype, pe.name)

    def test_receive_payment_cancellation(self):
        pe = frappe.get_doc({
            "doctype": "Payment Entry", "payment_type": "Receive",
            "posting_date": frappe.utils.today(), "party": self.customer,
            "account_paid_from": self.receivable_account, "account_paid_to": self.bank_account,
            "amount": 500
        }).insert()
        pe.submit()
        pe.cancel()
        self.assertNetEffectIsZero(pe.doctype, pe.name)

    def test_pay_payment_submission(self):
        pe = frappe.get_doc({
            "doctype": "Payment Entry", "payment_type": "Pay",
            "posting_date": frappe.utils.today(), "party": self.supplier,
            "account_paid_from": self.bank_account, "account_paid_to": self.payable_account,
            "amount": 1200
        }).insert()
        pe.submit()
        self.assertVoucherBalanced(pe.doctype, pe.name)
        
    def test_pay_payment_cancellation(self):
        pe = frappe.get_doc({
            "doctype": "Payment Entry", "payment_type": "Pay",
            "posting_date": frappe.utils.today(), "party": self.supplier,
            "account_paid_from": self.bank_account, "account_paid_to": self.payable_account,
            "amount": 1200
        }).insert()
        pe.submit()
        pe.cancel()
        self.assertNetEffectIsZero(pe.doctype, pe.name)