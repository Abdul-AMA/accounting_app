//a financial report showing the closing balances of all accounts in the general ledger at a point in time

frappe.query_reports["Trial Balance"] = {
    "filters": [
        {
            "fieldname": "as_on_date",
            "label": "As on Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
    ]
};
