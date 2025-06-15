frappe.ui.form.on('Payment Entry', {
    refresh: function(frm) {
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
           
            frm.get_field('account_paid_from').set_label('Account paid from');
            frm.get_field('account_paid_to').set_label('Account Paid to');
        }
        frm.refresh(); 

        frm.set_query('account_paid_from', function() {
            let filters = {'is_group': 0}; 
            if (payment_type === 'Receive') {
                filters['account_type'] = 'Asset';
            } else if (payment_type === 'Pay') {
               filters['account_type'] = 'Asset';
            }
            return { filters: filters };
        });

        // Filter for the target account
        frm.set_query('account_paid_to', function() {
            let filters = {'is_group': 0};
		if (payment_type === 'Receive') {
               filters['account_type'] = 'Asset';
            } else if (payment_type === 'Pay') {
                filters['account_type'] = 'Liability';
            }
            return { filters: filters };
        });
    }
});
