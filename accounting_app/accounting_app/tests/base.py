import frappe
from frappe.tests import IntegrationTestCase

class AccountingTestCase(IntegrationTestCase):

    def setUp(self):
        self.company = frappe.db.get_single_value('Global Defaults', 'default_company')
        if not self.company:
            self.company = "_Test Company"
            if not frappe.db.exists("Company", self.company):
                frappe.get_doc({"doctype": "Company", "company_name": self.company, "default_currency": "INR", "country": "China"}).insert()
            frappe.db.set_single_value('Global Defaults', 'default_company', self.company)

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
            fields=["debit", "credit"]
        )
        total_debit = sum(d.debit for d in gl_entries)
        total_credit = sum(d.credit for d in gl_entries)
        self.assertEqual(total_debit, total_credit, f"Voucher {voucher_name} is unbalanced.")

    def assertNetEffectIsZero(self, voucher_doctype, voucher_name):
        gl_entries = frappe.get_all("GL Entry",
            filters={"voucher_type": voucher_doctype, "voucher_number": voucher_name},
            fields=["debit", "credit"]
        )
        total_debit = sum(d.debit for d in gl_entries)
        total_credit = sum(d.credit for d in gl_entries)
        self.assertEqual(total_debit, total_credit, f"Net effect for cancelled voucher {voucher_name} is not zero.")
    
    def assertGLEntries(self, voucher_doctype, voucher_name, expected_entries):
        gl_entries = frappe.get_all("GL Entry", 
            filters={"voucher_type": voucher_doctype, "voucher_number": voucher_name, "is_cancelled": 0},
            fields=["account", "debit", "credit"]
        )
        self.assertEqual(len(gl_entries), len(expected_entries), "Number of GL entries does not match expected.")
        for expected in expected_entries:
            self.assertTrue(
                any(
                    d.account == expected.get("account") and
                    d.debit == expected.get("debit", 0) and
                    d.credit == expected.get("credit", 0)
                    for d in gl_entries
                ),
                f"Expected GL entry not found: {expected}"
            )

    def get_or_create_account(self, account_name, account_type):
        if not frappe.db.exists("Account", {"account_name": account_name, "company": self.company}):
            frappe.get_doc({
                "doctype": "Account", "account_name": account_name,
                "account_type": account_type, "company": self.company,
                "is_group": 0
            }).insert()
        return account_name

    def get_or_create_party(self, party_name, party_type):
        if not frappe.db.exists("Party", party_name):
            frappe.get_doc({"doctype": "Party", "party_name": party_name, "party_type": party_type}).insert()
        return party_name

    def get_or_create_item(self, item_code):
        if not frappe.db.exists("Item", item_code):
            frappe.get_doc({"doctype": "Item", "item_code": item_code}).insert()
        return item_code