# Copyright (c) 2025, abood-ama and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

class IntegrationTestJournalEntry(IntegrationTestCase):
    """
    Integration tests for JournalEntry using existing database data.
    """

    def test_journal_entry_posting(self):

        
        cash_account_name = "Cash"           
        asset_account_name = "Stock"    
        equity_account_name = "Service Income"      
        
        je = frappe.get_doc({
            "doctype": "Journal Entry",
            "posting_date": frappe.utils.today(),
            "accounting_entries": [
                { "account": cash_account_name, "debit": 100000, "credit": 0 },
                { "account": asset_account_name, "debit": 15000, "credit": 0 },
                { "account": equity_account_name, "debit": 0, "credit": 115000 }
            ]
        }).insert()
        je.submit()
        
        gl_entries = frappe.get_all("GL Entry", filters={"voucher_number": je.name}, fields=["account", "debit_amount", "credit_amount"])
        
        self.assertEqual(len(gl_entries), 3)

        self.assertTrue(
            any(d.account == cash_account_name and d.debit_amount == 100000 for d in gl_entries),
            f"GL Entry for '{cash_account_name}' debit not found or incorrect."
        )
        self.assertTrue(
            any(d.account == asset_account_name and d.debit_amount == 15000 for d in gl_entries),
            f"GL Entry for '{asset_account_name}' debit not found or incorrect."
        )
        self.assertTrue(
            any(d.account == equity_account_name and d.credit_amount == 115000 for d in gl_entries),
            f"GL Entry for '{equity_account_name}' credit not found or incorrect."
        )