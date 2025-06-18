// Copyright (c) 2025, abood-ama and contributors
// For license information, please see license.txt

frappe.query_reports["General Ledger"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Link",
            "options": "Account",
            "get_query": function() {
                return { filters: { "is_group": 0 } };
            }
        },
        {
            "fieldname": "party",
            "label": "Party",
            "fieldtype": "Link",
            "options": "Party"
        }
    ]
};