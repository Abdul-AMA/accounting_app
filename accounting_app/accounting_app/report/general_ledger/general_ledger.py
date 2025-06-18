import frappe
from frappe.query_builder.functions import Sum

def execute(filters):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
        {"label": "Debit", "fieldname": "debit_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Credit", "fieldname": "credit_amount", "fieldtype": "Currency", "width": 120},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 120},
        {"label": "Voucher Type", "fieldname": "voucher_type", "width": 120},
        {"label": "Voucher No", "fieldname": "voucher_number", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 150},
        {"label": "Party", "fieldname": "party", "fieldtype": "Link", "options": "Party", "width": 150},
        {"label": "Remark", "fieldname": "remark", "width": 200}
    ]

def get_data(filters):
    gl_entry = frappe.qb.DocType("GL Entry")
    
    conditions = []

    if filters.get("from_date"):
        conditions.append(gl_entry.posting_date >= filters.get("from_date"))
    if filters.get("to_date"):
        conditions.append(gl_entry.posting_date <= filters.get("to_date"))
    if filters.get("account"):
        conditions.append(gl_entry.account == filters.get("account"))
    if filters.get("party"):
        conditions.append(gl_entry.party == filters.get("party"))

    data = (
        frappe.qb.from_(gl_entry)
        .select(gl_entry.star)
        .where(conditions) 
        .orderby(gl_entry.posting_date, gl_entry.creation)
    ).run(as_dict=True)

    balance = 0
    if filters.get("account"):
        balance = get_opening_balance(filters.get("account"), filters.get("from_date"))
        if balance != 0:
            data.insert(0, {
                "posting_date": frappe.utils.add_days(filters.get("from_date"), -1) if filters.get("from_date") else "",
                "account": filters.get("account"), "voucher_number": "Opening Balance",
                "balance": balance
            })

    for row in data:
        if row.get("voucher_number") != "Opening Balance":
            if not row.get("is_cancelled"):
                balance += row.get("debit_amount", 0) - row.get("credit_amount", 0)
            row["balance"] = balance

    return data


def get_opening_balance(account, from_date):
    if not from_date:
        return 0

    gl_entry = frappe.qb.DocType("GL Entry")
    Sum = frappe.qb.functions.Sum

    opening = (
        frappe.qb.from_(gl_entry)
        .select((Sum(gl_entry.debit_amount) - Sum(gl_entry.credit_amount)).as_("balance"))
        .where(
            (gl_entry.account == account) &
            (gl_entry.is_cancelled == 0) & 
            (gl_entry.posting_date < from_date)
        )
    ).run(as_dict=True)
    
    return opening[0].balance if opening and opening[0].balance is not None else 0