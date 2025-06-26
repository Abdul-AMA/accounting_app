frappe.ui.form.on("Warehouse", {
        refresh: function(frm) {

        frm.set_query('account', function() {
            return {
                filters: { 'account_type': 'asset', 'is_group': 0 }
            };
        });
        frm.set_query('cogs_account', function() {
            return {
                filters: { 'account_type': 'expense', 'is_group': 0 }
            };
        });

   },
});
