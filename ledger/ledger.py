# -*- coding: utf-8 -*-
from decimal import *
from datetime import datetime as dt

class LedgerOrderError(Exception):
    pass

class Ledger(object):
    """
    Utility to process purchases from a ledger file with the following format:

    2015-01-16,john,mary,125.00
    2015-01-17,john,supermarket,20.00
    2015-01-17,mary,insurance,100.00

    Raises ``LedgerOrderError`` when purchases are not ordered from least to
    most recent.

    Exposes ``balances`` with final or current balances for all parties.
    ie: ledger.balances['john']

    Exposes ``day_balances`` with day balances for all parties.
    ie: ledger.day_balances['2015-01-16']['john']
    """

    def __init__(self, file_path):
        """
        Ledger that exposes balances and daily balances for the given file.

        :param file_path: Path to file with purchases to be processed
        """
        self.balances = {}
        self.day_balances = {}
        self.last_date = None

        with open(file_path) as ledger:
            for purchase in ledger:
                self._process_purchase_text(purchase)

    def _update_current_balance(self, party, amount):
        if party not in self.balances:
            self.balances[party] = 0
        self.balances[party] += amount
        return self.balances[party]

    def _update_day_balance(self, day, party, amount):
        b = self.day_balances[day] if day in self.day_balances else {}
        b[party] = amount
        self.day_balances[day] = b

    def _process_party(self, date, party, amount):
        current_balance = self._update_current_balance(party, amount)
        self._update_day_balance(date, party, current_balance)

    def _process_purchase(self, date, payer, payee, amount):
        self._process_party(date, payer, -amount)
        self._process_party(date, payee, amount)

    def _process_purchase_text(self, purchase):
        [date, payer, payee, amount] = purchase.split(',')
        current_date = dt.strptime(date, "%Y-%m-%d")
        if self.last_date and current_date < self.last_date:
            raise LedgerOrderError()
        self._process_purchase(date, payer, payee, Decimal(amount))
        self.last_date = current_date
