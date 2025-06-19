frappe.ui.form.on('Journal Entry', {

    refresh: function(frm) {
        frm.set_query('account', 'accounting_entries', function(doc, cdt, cdn) {
            return {
                filters: {
                    'is_group': 0
                }
            };
        });
    },
    calculate_totals: function(frm) {
        let total_debit = 0;
        let total_credit = 0;

        if (frm.doc.accounting_entries) {
            frm.doc.accounting_entries.forEach(function(entry) {
                total_debit += flt(entry.debit);
                total_credit += flt(entry.credit);
            });
        }

        frm.set_value('total_debit', total_debit);
        frm.set_value('total_credit', total_credit);
        frm.set_value('difference', total_debit - total_credit);

        if (frm.doc.difference != 0) {
            frm.get_field('difference').$wrapper.addClass('text-danger');
        } else {
            frm.get_field('difference').$wrapper.removeClass('text-danger');
        }
    }
});

frappe.ui.form.on('Journal Entry Account', {
    debit: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if(row.debit > 0) {
            row.credit = 0;
        }
        frm.refresh_field('accounting_entries');
        frm.events.calculate_totals(frm);
    },
    credit: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if(row.credit > 0) {
            row.debit = 0;
        }
        frm.refresh_field('accounting_entries');
        frm.events.calculate_totals(frm);
    },
    accounting_entries_add: function(frm) {
        frm.events.calculate_totals(frm);
    },
    accounting_entries_remove: function(frm) {
        frm.events.calculate_totals(frm);
    }
});