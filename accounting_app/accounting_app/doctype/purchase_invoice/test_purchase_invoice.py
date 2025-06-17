# Copyright (c) 2025, abood-ama and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

class IntegrationTestPurchaseInvoice(IntegrationTestCase):


    def test_purchase_gl_posting_and_cancellation(self):
        
        supplier_name = "Costco"
        payable_account_name = "Accounts Payable"
        expense_account_name = "COGS"    
        item_name = "coffe"      
        

        pi = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": supplier_name,
            "posting_date": frappe.utils.today(),
            "payment_due_date": frappe.utils.today(),
            "credit_to": payable_account_name,
            "expense_account": expense_account_name,
            "items": [{
                "item": item_name,
                "qty": 1500,
                "rate": 10,
				"amount": 15000 

            }]
        }).insert()
        pi.submit()
        
        gl_entries = frappe.get_all("GL Entry", filters={"voucher_number": pi.name}, fields=["account", "debit_amount", "credit_amount"])
        self.assertEqual(len(gl_entries), 2)
        
        self.assertTrue(
            any(d.account == expense_account_name and d.debit_amount == 15000 for d in gl_entries),
            f"Debit entry for '{expense_account_name}' not found or incorrect."
        )
        self.assertTrue(
            any(d.account == payable_account_name and d.credit_amount == 15000 for d in gl_entries),
            f"Credit entry for '{payable_account_name}' not found or incorrect."
        )
        
        pi.cancel()
        all_gl_entries = frappe.get_all("GL Entry", filters={"voucher_number": pi.name}, fields=["is_cancelled"])
        self.assertEqual(len(all_gl_entries), 4) 
        
        cancelled_count = sum(1 for entry in all_gl_entries if entry.is_cancelled)
        self.assertEqual(cancelled_count, 2)