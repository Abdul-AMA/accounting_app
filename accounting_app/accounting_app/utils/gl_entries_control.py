# accounting_app/gl_entry_control.py

import frappe

def create_gl_entry(posting_date, account, party, debit, credit, voucher_type, voucher_number, due_date=None, remark=None):
    entry = frappe.new_doc("GL Entry")
    entry.posting_date = posting_date
    entry.due_date = due_date
    entry.account = account
    entry.party = party
    entry.debit_amount = debit
    entry.credit_amount = credit
    entry.voucher_type = voucher_type
    entry.voucher_number = voucher_number
    entry.remark = remark
    entry.insert(ignore_permissions=True)
    entry.submit()
    return entry.name



def reverse_gl_entries(voucher_type, voucher_number, posting_date, remark_prefix="Reversal entry for cancellation of "):
    original_entries = frappe.get_all("GL Entry",
        filters={
            'voucher_type': voucher_type,
            'voucher_number': voucher_number,
            'is_cancelled': 0
        },
        fields=["name", "account", "party", "credit_amount", "debit_amount"]
    )

    for entry in original_entries:
        create_gl_entry(
            posting_date=posting_date,
            due_date=None,
            account=entry.account,
            party=entry.party,
            debit=entry.credit_amount,
            credit=entry.debit_amount,
            voucher_type=voucher_type,
            voucher_number=voucher_number,
            remark=f"{remark_prefix} {voucher_number}"
        )

        doc = frappe.get_doc("GL Entry", entry.name)
        doc.is_cancelled = 1
        doc.save(ignore_permissions=True)
