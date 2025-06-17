# Copyright (c) 2025, abood-ama and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase

class IntegrationTestSalesInvoice(IntegrationTestCase):
    """
    Integration tests for SalesInvoice using existing database data.
    """

    def test_gl_posting_and_cancellation(self):

        
        customer_name = "ahmed" 
        receivable_account_name = "Accounts Receivable" 
        income_account_name = "Sales"   
        item_name = "milk"             
        

        si = create_sales_invoice(
            customer=customer_name,
            debit_to=receivable_account_name,
            income_account=income_account_name,
            item=item_name,
            rate=5000,
            qty=2
        )
        
        gl_entries = frappe.get_all("GL Entry", filters={"voucher_number": si.name}, fields=["account", "debit_amount", "credit_amount"])
        
        self.assertEqual(len(gl_entries), 2)
        self.assertGLEntry(gl_entries, receivable_account_name, 10000, 0)
        self.assertGLEntry(gl_entries, income_account_name, 0, 10000)
        
        si.cancel()
        all_gl_entries = frappe.get_all("GL Entry", filters={"voucher_number": si.name}, fields=["is_cancelled"])
        self.assertEqual(len(all_gl_entries), 4)
        cancelled_count = sum(1 for entry in all_gl_entries if entry.is_cancelled)
        self.assertEqual(cancelled_count, 2)

    def assertGLEntry(self, gl_entries, account, debit, credit):
        self.assertTrue(
            any(d.account == account and d.debit_amount == debit and d.credit_amount == credit for d in gl_entries),
            f"GL Entry not found for Account '{account}' with Debit={debit}, Credit={credit}"
        )

def create_sales_invoice(**args):
    si = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": args.get("customer"),
        "posting_date": frappe.utils.today(),
        "payment_due_date": frappe.utils.today(),
        "debit_to": args.get("debit_to"),
        "income_account": args.get("income_account"),
		"items": [{"item": args.get("item"), "qty": args.get("qty"), "rate": args.get("rate"), "amount": args.get("qty") * args.get("rate")}]
    })
    si.insert()
    si.submit()
    return si