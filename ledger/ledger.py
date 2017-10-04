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
    """

    def __init__(self, file_path):
        """
        Ledger that exposes balances and daily balances for all parties included
        in the given file.

        :param file_path: Path to file with purchases to be processed
        """
        self._balances = {}
        self._day_balances = {}
        self.last_date = None

        with open(file_path) as ledger:
            for purchase in ledger:
                self._process_purchase_text(purchase)

    def balance(self, party):
        """
        Exposes final or current balance for the given party.
        ie: ledger.balance('john')

        :param party: desired party
        """
        if party in self._balances:
            return self._balances[party]
        return 0

    def day_balance(self, day, party):
        """
        Exposes balance for the given date/party.
        ie: ledger.balance('2015-01-16', 'john')

        Returns last balance for any future dates outside the known
        transaction dates.

        :param day: date with format 'YYYY-mm-dd'
        :param party: desired party
        """
        if day in self._day_balances and party in self._day_balances[day]:
            return self._day_balances[day][party]
        target_date = dt.strptime(day, "%Y-%m-%d")
        if target_date > self.last_date:
            target_date_str = self.last_date.strftime("%Y-%m-%d")
            if party in self._day_balances[target_date_str]:
                return self._day_balances[target_date_str][party]
        return 0

    def _update_current_balance(self, party, amount):
        if party not in self._balances:
            self._balances[party] = 0
        self._balances[party] += amount
        return self._balances[party]

    def _update_day_balance(self, day, party, amount):
        b = self._day_balances[day] if day in self._day_balances else {}
        b[party] = amount
        self._day_balances[day] = b

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
