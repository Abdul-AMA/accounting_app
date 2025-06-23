frappe.ui.form.on('Purchase Invoice', {

        refresh: function(frm) {

        frm.set_query('supplier', function() {
            return {
                filters: { 'party_type': 'Supplier' }
            };
        });

        frm.set_query('credit_to', function() {
            return {
                filters: { 'account_type': 'Liability', 'is_group': 0 }
            };
        });

        frm.set_query('expense_account', function() {
            return {
                filters: { 'account_type': 'Expense', 'is_group': 0 }
            };
        });

   },


    calculate_totals: function(frm) {
        let total_qty = 0;
        let total_amount = 0;
        if (frm.doc.items) {
            frm.doc.items.forEach(function(item_row) {
                total_qty += flt(item_row.qty);
                total_amount += flt(item_row.amount);
            });
        }
        frm.set_value('total_qty', total_qty);
        frm.set_value('total_amount', total_amount);
        frm.refresh_field('total_qty');
        frm.refresh_field('total_amount');
    },
    default_warehouse: function(frm) {
        if (frm.doc.items && frm.doc.items.length) {
            frm.doc.items.forEach(function(row) {
                row.warehouse = frm.doc.default_warehouse;
            });
        }
        frm.refresh_field('items');
    }
});

frappe.ui.form.on('Purchase Invoice Item', {
    qty: function(frm, cdt, cdn) {
        let item_row = locals[cdt][cdn];
        item_row.amount = flt(item_row.qty) * flt(item_row.rate);
        frm.refresh_field('items');
        frm.events.calculate_totals(frm);
    },
    rate: function(frm, cdt, cdn) {
        let item_row = locals[cdt][cdn];
        item_row.amount = flt(item_row.qty) * flt(item_row.rate);
        frm.refresh_field('items');
        frm.events.calculate_totals(frm);
    },
    items_remove: function(frm) {
        frm.events.calculate_totals(frm);
    },
    items_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.warehouse = frm.doc.default_warehouse;
        frm.refresh_field('items');
    }, 
});
