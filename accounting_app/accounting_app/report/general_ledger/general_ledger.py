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

    if filters.get("from_date"):
        query = query.where(gl_entry.posting_date >= filters.get("from_date"))
    if filters.get("to_date"):
        query = query.where(gl_entry.posting_date <= filters.get("to_date"))
    if filters.get("account"):
        query = query.where(gl_entry.account == filters.get("account"))
    if filters.get("party"):
        query = query.where(gl_entry.party == filters.get("party"))

    return query.run(as_dict=True)

