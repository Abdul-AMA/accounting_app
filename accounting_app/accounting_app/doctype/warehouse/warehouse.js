frappe.ui.form.on("Warehouse", {
        refresh: function(frm) {

        frm.set_query('account', function() {
            return {
                filters: { 'account_type': 'asset', 'is_group': 0 }
            };
        });

   },
});
