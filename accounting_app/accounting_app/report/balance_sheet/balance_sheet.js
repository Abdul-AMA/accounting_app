// Copyright (c) 2025, abood-ama and contributors
// For license information, please see license.txt

frappe.query_reports["Balance Sheet"] = {
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
