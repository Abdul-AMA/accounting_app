# Copyright (c) 2025, abood-ama and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

class IntegrationTestPaymentEntry(IntegrationTestCase):


    def test_receive_payment(self):
        customer_name = "harvey"
        receivable_account_name = "Accounts Receivable"
        bank_account_name = "Cash"

        pe = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Receive",
            "posting_date": frappe.utils.today(),
            "party_type": "Customer",
            "party": customer_name,
            "account_paid_from": receivable_account_name,
            "account_paid_to": bank_account_name,
            "amount": 500
        }).insert()
        pe.submit()

        gl_entries = frappe.get_all("GL Entry", filters={"voucher_number": pe.name}, fields=["account", "debit_amount", "credit_amount"])
        self.assertEqual(len(gl_entries), 2)
        
        self.assertTrue(
            any(d.account == bank_account_name and d.debit_amount == 500 for d in gl_entries),
            f"Debit entry for '{bank_account_name}' not found or incorrect."
        )
        self.assertTrue(
            any(d.account == receivable_account_name and d.credit_amount == 500 for d in gl_entries),
            f"Credit entry for '{receivable_account_name}' not found or incorrect."
        )
        
    def test_pay_payment(self):
        supplier_name = "Amazon"
        payable_account_name = "Accounts Payable"
        bank_account_name = "Bank Accounts"

        pe = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Pay",
            "posting_date": frappe.utils.today(),
            "party_type": "Supplier",
            "party": supplier_name,
            "account_paid_from": bank_account_name,
            "account_paid_to": payable_account_name,
            "amount": 1200
        }).insert()
        pe.submit()

        gl_entries = frappe.get_all("GL Entry", filters={"voucher_number": pe.name}, fields=["account", "debit_amount", "credit_amount"])
        self.assertEqual(len(gl_entries), 2)

        self.assertTrue(
            any(d.account == payable_account_name and d.debit_amount == 1200 for d in gl_entries),
            f"Debit entry for '{payable_account_name}' not found or incorrect."
        )
        self.assertTrue(
            any(d.account == bank_account_name and d.credit_amount == 1200 for d in gl_entries),
            f"Credit entry for '{bank_account_name}' not found or incorrect."
        )