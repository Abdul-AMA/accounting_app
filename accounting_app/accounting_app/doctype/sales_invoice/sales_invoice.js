// Copyright (c) 2025, abood-ama and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Sales Invoice", {
 	refresh(frm) {

 	},
 });

// calculate the total quantity and total amount  of the items in the items list 

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

// Script for the Child Table 'Sal rowes Invoice Item' (within the Sales Invoice form context)
frappe.ui.form.on('Sales Invoice Item', {
    // When quantity change in any row of the table the amount is recalculated and the total calculate is triggerd `
    qty: function(frm, cdt, cdn) {
        let item_row = locals[cdt][cdn];
        item_row.amount = flt(item_row.quantity) * flt(item_row.rate);
        frm.refresh_field('items'); // Refresh the whole items table to show updated amount
        frm.events.calculate_totals(frm); // Recalculate grand totals
    },
	
    // When rate change in any row of the table the amount is recalculated and the total calculate is triggerd `
    rate: function(frm, cdt, cdn) {
        let item_row = locals[cdt][cdn];
        item_row.amount = flt(item_row.quantity) * flt(item_row.rate);
        frm.refresh_field('items');
        frm.events.calculate_totals(frm);
    },
    // When an item is removed from the items table everything is recalculated, everything is calculated we dont leave anything to chance
    items_remove: function(frm) {
        frm.events.calculate_totals(frm);
    }
});
