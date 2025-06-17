from ...controllers.AccountingController import AccountingController

class PaymentEntry(AccountingController):

    def make_gl_entries(self):
        if self.payment_type == "Receive":
            self._create_gl_entry(
                posting_date=self.posting_date,
                account=self.account_paid_to,
                party=self.party,
                debit=self.amount,
                credit=0
            )
            self._create_gl_entry(
                posting_date=self.posting_date,
                account=self.account_paid_from,
                party=self.party,
                debit=0,
                credit=self.amount
            )
        elif self.payment_type == "Pay":
            self._create_gl_entry(
                posting_date=self.posting_date,
                account=self.account_paid_to,
                party=self.party,
                debit=self.amount,
                credit=0
            )

            self._create_gl_entry(
                posting_date=self.posting_date,
                account=self.account_paid_from,
                party=self.party,
                debit=0,
                credit=self.amount
            )
