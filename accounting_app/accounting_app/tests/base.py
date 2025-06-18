
import frappe
from frappe.tests import IntegrationTestCase

class AccountingTestCase(IntegrationTestCase):
    def setUp(self):

        self.receivable_account = self.get_or_create_account("Debtors - Test", "Asset")
        self.payable_account = self.get_or_create_account("Creditors - Test", "Liability")
        self.income_account = self.get_or_create_account("Sales - Test", "Income")
        self.expense_account = self.get_or_create_account("Expenses - Test", "Expense")
        self.bank_account = self.get_or_create_account("Bank - Test", "Asset")

        self.customer = self.get_or_create_party("Test Customer", "Customer")
        self.supplier = self.get_or_create_party("Test Supplier", "Supplier")

        self.test_item = self.get_or_create_item("Test Item")


    def assertVoucherBalanced(self, voucher_doctype, voucher_name):
        gl_entries = frappe.get_all("GL Entry", 
            filters={"voucher_type": voucher_doctype, "voucher_number": voucher_name, "is_cancelled": 0},
            fields=["debit_amount", "credit_amount"]
        )
        total_debit = sum(d.debit_amount or 0 for d in gl_entries)
        total_credit = sum(d.credit_amount or 0 for d in gl_entries)
        self.assertEqual(total_debit, total_credit, f"Voucher {voucher_name} is unbalanced.")


    def assertNetEffectIsZero(self, voucher_doctype, voucher_name):

        gl_entries = frappe.get_all("GL Entry",
            filters={"voucher_type": voucher_doctype, "voucher_number": voucher_name},
            fields=["debit_amount", "credit_amount","is_cancelled"]
        )

        total_debit_on_submisson = sum(d.debit_amount or 0 for d in gl_entries if d.is_cancelled == 1)
        total_credit_on_submisson = sum(d.credit_amount or 0 for d in gl_entries if d.is_cancelled == 1)
        total_debit_on_cancel = sum(d.debit_amount or 0 for d in gl_entries if d.is_cancelled == 0)
        total_credit_on_cancel = sum(d.credit_amount or 0 for d in gl_entries if d.is_cancelled == 0)

        self.assertEqual(
            total_debit_on_submisson,
            total_credit_on_cancel,
            f"Reversal credits ({total_credit_on_cancel}) do not match original debits ({total_debit_on_submisson}) for {voucher_name}."

        )
        self.assertEqual(
            total_credit_on_submisson,
            total_debit_on_cancel,
            f"Reversal debits ({total_debit_on_cancel}) do not match original credits ({total_credit_on_submisson}) for {voucher_name}."

        )

    def assertGLEntries(self, voucher_doctype, voucher_name, expected_entries):
        gl_entries = frappe.get_all("GL Entry", 
            filters={"voucher_type": voucher_doctype, "voucher_number": voucher_name, "is_cancelled": 0},
            fields=["account", "debit_amount", "credit_amount"]
        )
        self.assertEqual(len(gl_entries), len(expected_entries), "Number of GL entries does not match expected.")
        for expected in expected_entries:
            self.assertTrue(
                any(
                    d.account == expected.get("account") and
                    d.debit_amount == expected.get("debit", 0) and
                    d.credit_amount == expected.get("credit", 0)
                    for d in gl_entries
                ),
                f"Expected GL entry not found: {expected}"
            )

    def get_or_create_account(self, account_name, account_type):
        if not frappe.db.exists("Account", account_name):
            frappe.get_doc({"doctype": "Account", "account_name": account_name, "account_type": account_type, "is_group": 0}).insert()
        return account_name

    def get_or_create_party(self, party_name, party_type):
        if not frappe.db.exists("Party", party_name):
            frappe.get_doc({"doctype": "Party", "party_name": party_name, "party_type": party_type}).insert()
        return party_name

    def get_or_create_item(self, item_code):
        if not frappe.db.exists("Item", item_code):
            frappe.get_doc({
                "doctype": "Item",
                "item_code": item_code,
                "item_name": item_code
            }).insert()
        return item_code