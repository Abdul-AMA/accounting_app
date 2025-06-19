import frappe
from frappe.query_builder.functions import Sum

def execute(filters):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Account", "fieldname": "account", "fieldtype": "data", "options": "Account", "width": 400},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 150},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    accounts = frappe.get_all("Account", filters={"is_group": 0}, fields=["name"])
    
    data = []
    total_debit = 0
    total_credit = 0

    as_on_date = filters.get("as_on_date")

    gl_entry = frappe.qb.DocType("GL Entry")
    
    all_balances = (
        frappe.qb.from_(gl_entry)
        .select(
            gl_entry.account,
            (Sum(gl_entry.debit_amount) - Sum(gl_entry.credit_amount)).as_("balance")
            )
        .where(
            (gl_entry.posting_date <= as_on_date)
        )
        .groupby(gl_entry.account)
    ).run(as_dict=True)

    balances_dict = {d.account: d.balance for d in all_balances}


    for acc in accounts:
        account_name = acc.get("name")
        
        balance = balances_dict.get(account_name, 0)

        row = {"account": account_name}
        if balance >= 0:  
            row["debit"] = balance
            row["credit"] = 0
            total_debit += balance
        else:
            row["debit"] = 0
            row["credit"] = abs(balance) 
            total_credit += abs(balance)
        
        data.append(row)

    if data:
        data.append({
            "account": "Total",
            "debit": total_debit,
            "credit": total_credit
        })
    
    return data


