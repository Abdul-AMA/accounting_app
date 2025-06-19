import frappe
from frappe.query_builder.functions import Sum

def execute(filters):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 400},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 150},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    accounts = frappe.get_all("Account", filters={"is_group": 0}, fields=["name"])
    
    data = []
    total_debit = 0
    total_credit = 0

    as_on_date = filters.get("as_on_date")

    for acc in accounts:
        account_name = acc.get("name")
        
        closing_balance = get_account_balance(account_name, as_on_date)

        row = {"account": account_name}
        if closing_balance > 0:  
            row["debit"] = closing_balance
            row["credit"] = 0
            total_debit += closing_balance
        else:
            row["debit"] = 0
            row["credit"] = abs(closing_balance) 
            total_credit += abs(closing_balance)
        
        data.append(row)

    if data:
        data.append({
            "account": "Total",
            "debit": total_debit,
            "credit": total_credit
        })
    
    return data

def get_account_balance(account, to_date):
    gl_entry = frappe.qb.DocType("GL Entry")
    
    balance = (
        frappe.qb.from_(gl_entry)
        .select(Sum(gl_entry.debit_amount) - Sum(gl_entry.credit_amount))
        .where(
            (gl_entry.account == account) &
            (gl_entry.posting_date <= to_date)
        )
    ).run()
    
    return balance[0][0] if balance and balance[0] and balance[0][0] is not None else 0
