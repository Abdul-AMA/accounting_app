frappe.ui.form.on('Sales Invoice', {
    // This will run when the form is refreshed or when an item is added/removed
    refresh: function(frm) {
        calculate_totals(frm);
    },
    items_add: function(frm) {
        calculate_totals(frm);
    },
    items_remove: function(frm) {
        calculate_totals(frm);
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    // This will run when qty or rate is changed in the child table
    quantity: function(frm, cdt, cdn) {
        var item_row = locals[cdt][cdn];
        item_row.amount = item_row.quantity * item_row.rate;
        frm.refresh_field('items');
        calculate_totals(frm);
    },
    rate: function(frm, cdt, cdn) {
        var item_row = locals[cdt][cdn];
        item_row.amount = item_row.quantity * item_row.rate;
        frm.refresh_field('items');
        calculate_totals(frm);  
    }
});

// Function to calculate totals
function calculate_totals(frm) {
    var total_qty = 0;
    var total_amount = 0;
    if (frm.doc.items) {
        frm.doc.items.forEach(function(item) {
            total_qty += item.qty;
            total_amount += item.amount;
        });
    }
    frm.set_value('total_qty', total_qty);
    frm.set_value('total_amount', total_amount);
    frm.refresh_field('total_qty');
    frm.refresh_field('total_amount');
}