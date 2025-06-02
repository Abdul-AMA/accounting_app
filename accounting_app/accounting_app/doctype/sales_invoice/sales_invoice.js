// Copyright (c) 2025, abood-ama and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Sales Invoice", {
 	refresh(frm) {

 	},
 });
 


    // here we  calculate totals of quantity and amount based on the items in the table and we can call whenever any item changes
    calculate_totals: function(frm) {
        let total_qty = 0;
        let total_amount = 0;

        if (frm.doc.items) {
            frm.doc.items.forEach(function(item_row) {
                total_qty += flt(item_row.quantity);
                total_amount += flt(item_row.amount);
            });
        }

        frm.set_value('total_qty', total_qty);
        frm.set_value('total_amount', total_amount);
        frm.refresh_field('total_qty');
        frm.refresh_field('total_amount');
    }
});

// Script for the Child Table 'Sales Invoice Item' (within the Sales Invoice form context)
frappe.ui.form.on('Sales Invoice Item', {
    // When quantity changes we do some recalculations of the amouny and then call for toatl recalculate
    qty: function(frm, cdt, cdn) {
        let item_row = locals[cdt][cdn];
        item_row.amount = flt(item_row.quantity) * flt(item_row.rate);
        frm.refresh_field('items');
        frm.events.calculate_totals(frm); 
    },
	// When rate(price) changes we do some recalculations of the amount and then call for toatl recalculate
    rate: function(frm, cdt, cdn) {
        let item_row = locals[cdt][cdn];
        item_row.amount = flt(item_row.quantity) * flt(item_row.rate);
        frm.refresh_field('items');
        frm.events.calculate_totals(frm);
    },
    // When an item is removed from the items table we also make recalculation, as you see we don't leave anything to chance
    items_remove: function(frm) {
        frm.events.calculate_totals(frm);
    }
});
