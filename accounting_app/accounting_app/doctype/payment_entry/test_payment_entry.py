import frappe
from ...tests.base import AccountingTestCase

class IntegrationTestPaymentEntry(AccountingTestCase):
    
    def test_receive_payment(self):
        pe = frappe.get_doc({
            "doctype": "Payment Entry", "payment_type": "Receive",
            "posting_date": frappe.utils.today(), "party": self.customer,
            "account_paid_from": self.receivable_account, "account_paid_to": self.bank_account,
            "amount": 500
        }).insert()
        pe.submit()

 
        self.assertVoucherBalanced(pe.doctype, pe.name)

        expected_entries = [
            {"account": self.bank_account, "debit": 500},
            {"account": self.receivable_account, "credit": 500}
        ]
        self.assertGLEntries(pe.doctype, pe.name, expected_entries)
        
    def test_pay_payment(self):
        pe = frappe.get_doc({
            "doctype": "Payment Entry", "payment_type": "Pay",
            "posting_date": frappe.utils.today(), "party": self.supplier,
            "account_paid_from": self.bank_account, "account_paid_to": self.payable_account,
            "amount": 1200
        }).insert()
        pe.submit()

        self.assertVoucherBalanced(pe.doctype, pe.name)

        expected_entries = [
            {"account": self.payable_account, "debit": 1200},
            {"account": self.bank_account, "credit": 1200}
        ]
        self.assertGLEntries(pe.doctype, pe.name, expected_entries)