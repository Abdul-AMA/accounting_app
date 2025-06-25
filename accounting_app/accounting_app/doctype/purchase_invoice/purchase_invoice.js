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

        frm.set_query('stock_account', 'items', () => {
            return {
                filters: { 'account_type': 'Asset', 'is_group': 0 }
            };
        });

        frm.set_query('expense_account', 'items', () => {
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
    
    warehouse: function(frm) {
        if (frm.doc.items) {
            frm.doc.items.forEach(row => {
                if (row.is_stock_item) {
                    frappe.model.set_value(row.doctype, row.name, 'warehouse', frm.doc.warehouse);
                }
            });
        }
    },
    before_save: function(frm) {
        if (frm.doc.items) {
            frm.doc.items.forEach(row => {
                const grid_row = frm.fields_dict.items.grid.get_row(row.name);
                const is_stock = row.is_stock;
                if (!is_stock) {
                    frappe.model.set_value(row.doctype, row.name, 'warehouse', '');
                }
                if (grid_row) {
                    grid_row.toggle_display('warehouse', is_stock);
                    grid_row.toggle_display('stock_account', is_stock);
                    grid_row.toggle_display('expense_account', !is_stock);
                }
            });
        }
    },
    after_save: function(frm) {
        frm.refresh();
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
        frappe.model.set_value(cdt, cdn, 'warehouse', frm.doc.warehouse);
    },
    item: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];

        if (!row.item) return;
        frappe.db.get_value('Item', row.item, 'maintain_stock', (r) => {
            const is_stock_item = !!r.maintain_stock;

            frappe.model.set_value(cdt, cdn, 'is_stock_item', is_stock_item ? 1 : 0);

            const grid_row = frm.fields_dict.items.grid.get_row(cdn);
            if (grid_row) {
                grid_row.toggle_display('warehouse', is_stock_item);
                grid_row.toggle_display('stock_account', is_stock_item);
                grid_row.toggle_display('expense_account', !is_stock_item);
            }
        });
    },
});


