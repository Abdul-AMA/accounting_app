import frappe

def execute(filters):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
       {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 150},
        {"label": "Debit", "fieldname": "debit_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Credit", "fieldname": "credit_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Voucher Type", "fieldname": "voucher_type", "width": 200},
        {"label": "Voucher No", "fieldname": "voucher_number", "fieldtype": "Dynamic Link", "options": "voucher_type", "width": 200},
        {"label": "Party", "fieldname": "party", "fieldtype": "Link", "options": "Party", "width": 170},
        {"label": "Remark", "fieldname": "remark", "width": 400}    
    ]

def get_data(filters):
    gl_entry = frappe.qb.DocType("GL Entry")

    query = (
        frappe.qb.from_(gl_entry)
        .select(gl_entry.star)
        .orderby(gl_entry.posting_date, gl_entry.creation)
    )

    if filters.get("from_date"):
        query = query.where(gl_entry.posting_date >= filters.get("from_date"))
    if filters.get("to_date"):
        query = query.where(gl_entry.posting_date <= filters.get("to_date"))
    if filters.get("account"):
        query = query.where(gl_entry.account == filters.get("account"))
    if filters.get("party"):
        query = query.where(gl_entry.party == filters.get("party"))

    return query.run(as_dict=True)

