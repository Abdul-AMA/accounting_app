import frappe
from frappe.query_builder.functions import Sum

def execute(filters):
    columns = get_columns()
    data, summary_data = get_data(filters)

    return columns, data, None, None, summary_data

def get_columns():
    return [
        {"label": "Income", "fieldname": "income_account", "fieldtype": "Link", "options": "Account", "width": 250},
        {"label": "Amount", "fieldname": "income_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Expenses", "fieldname": "expense_account", "fieldtype": "Link", "options": "Account", "width": 250},
        {"label": "Amount", "fieldname": "expenses_amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    as_on_date = filters.get("as_on_date")

    transaction_totals = get_transaction_totals(as_on_date)

    incomes = get_accounts_by_type("Income", transaction_totals)
    expenses = get_accounts_by_type("Expense", transaction_totals)


    data = []
    num_rows = max(len(incomes), len(expenses))

    for i in range(num_rows):
        row = {}
        if i < len(incomes):
            row["income_account"] = incomes[i]["account"]
            row["income_amount"] = incomes[i]["balance"]

        if i < len(expenses):
            row["expense_account"] = expenses[i]["account"]
            row["expenses_amount"] = expenses[i]["balance"]

        data.append(row)
	
    total_incomes = sum(d.get("balance", 0) for d in incomes)
    total_expenses = sum(d.get("balance", 0) for d in expenses)
    net_profit = total_incomes - total_expenses

    summary_data = [
        {"label": "Total Incomes", "value": total_incomes,"indicator": "Green", "datatype": "Currency"},
        {"label": "Total Expenses", "value": total_expenses,"indicator": "Red", "datatype": "Currency"},
        {"label": "Net Profit", "value": net_profit,"indicator": "Green" if net_profit >= 0 else "Red", "datatype": "Currency"}
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
