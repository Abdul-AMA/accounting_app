
frappe.ui.form.on('Payment Entry', {
  
    refresh: function(frm) {
        frm.set_query('party', function() {
            return {
                filters: {
                    'party_type': frm.doc.party_type
                }
            };
        });
        
        frm.set_query('account_paid_from', function() {
            let account_filters = [
                ['Account', 'is_group', '=', 0]
            ];
            if (frm.doc.payment_type === 'Receive') {
                account_filters.push(['Account', 'account_type', '=', 'Asset']);
            } else if (frm.doc.payment_type === 'Pay') {
                account_filters.push(['Account', 'account_type', '=', 'Asset']);
            }
            return { filters: account_filters };
        });

        frm.set_query('account_paid_to', function() {
            let account_filters = [
                ['Account', 'is_group', '=', 0]
            ];
            if (frm.doc.payment_type === 'Receive') {
                account_filters.push(['Account', 'account_type', '=', 'Asset']);
            } else if (frm.doc.payment_type === 'Pay') {
                account_filters.push(['Account', 'account_type', '=', 'Liability']);
            }
            return { filters: account_filters };
        });        
    },

    party_type: function(frm) {
        frm.set_value('party', '');
    },

  
    on_load: function(frm) {
        frm.trigger('setup_dynamic_fields');
    },

    payment_type: function(frm) {
        frm.set_value('account_paid_from', '');
        frm.set_value('account_paid_to', '');
        frm.trigger('setup_dynamic_fields');
    },

    setup_dynamic_fields: function(frm) {
        const payment_type = frm.doc.payment_type;

        if (payment_type === 'Receive') {
            frm.get_field('account_paid_from').set_label('Received From Account'); 
            frm.get_field('account_paid_to').set_label('Deposited To Account');  
        } else if (payment_type === 'Pay') {
            frm.get_field('account_paid_from').set_label('Paid From Account');   
            frm.get_field('account_paid_to').set_label('Paid To Account');      
        } else {
            throw new Error("not listed paymeny_type");            
        }
        frm.refresh(); 

y
    }
});