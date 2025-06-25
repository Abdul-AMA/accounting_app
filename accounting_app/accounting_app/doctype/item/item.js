// Copyright (c) 2025, abood-ama and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item", {
        refresh: function(frm) {

        frm.set_query('expense_account', function() {
            return {
                filters: { 'account_type': 'Expense', 'is_group': 0 }
            };
        });

   },
});
