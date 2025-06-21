import frappe
from frappe.query_builder.functions import Sum
from pypika.terms import Case

def execute(filters):
    columns = get_columns()
    data, summary_data = get_data(filters)
    
    return columns, data, None, None, summary_data

def get_columns():
    return [
        {"label": "Assets", "fieldname": "asset_account", "fieldtype": "Link", "options": "Account", "width": 250},
        {"label": "Amount", "fieldname": "asset_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Liabilities", "fieldname": "liability_account", "fieldtype": "Link", "options": "Account", "width": 250},
        {"label": "Amount", "fieldname": "liability_amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    as_on_date = filters.get("as_on_date")
    
    transaction_totals = get_transaction_totals(as_on_date)
    
    assets = get_accounts_by_type("Asset", transaction_totals)
    liabilities = get_accounts_by_type("Liability", transaction_totals)
    

    data = []
    num_rows = max(len(assets), len(liabilities))

    for i in range(num_rows):
        row = {}
        if i < len(assets):
            row["asset_account"] = assets[i]["account"]
            row["asset_amount"] = assets[i]["balance"]
        
        if i < len(liabilities):
            row["liability_account"] = liabilities[i]["account"]
            row["liability_amount"] = liabilities[i]["balance"]
        
        data.append(row)

    total_assets = sum(d.get("balance", 0) for d in assets)
    total_liabilities = sum(d.get("balance", 0) for d in liabilities)

    summary_data = [
        {"label": "Total Assets", "value": total_assets,"indicator": "Green" if total_assets >= 0 else "Red", "datatype": "Currency"},
        {"label": "Total Liabilities", "value": total_liabilities,"indicator": "Green" if total_liabilities >= 0 else "Red", "datatype": "Currency"}
    ]

    return data, summary_data

def get_transaction_totals(as_on_date):
    gl_entry = frappe.qb.DocType("GL Entry")
    totals = (
        frappe.qb.from_(gl_entry)
        .select(gl_entry.account, (Sum(gl_entry.debit_amount) - Sum(gl_entry.credit_amount)).as_("balance"))
        .where(gl_entry.posting_date <= as_on_date)
        .groupby(gl_entry.account)
    ).run(as_dict=True)
    return {d.account: d.balance for d in totals}

def get_accounts_by_type(account_type, transactions_dict):

    accounts = frappe.get_all("Account", 
        filters={"account_type": account_type, "is_group": 0}, 
        fields=["name", "opening_balance"]
    )
    
    results = []
    for acc in accounts:
        opening = acc.get("opening_balance") or 0
        transactions = transactions_dict.get(acc.name, 0)
        final_balance = opening + transactions
        
        results.append({"account": acc.name, "balance": final_balance})
            
    return results