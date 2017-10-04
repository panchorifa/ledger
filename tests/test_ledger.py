"""
service tests
"""
from ledger.ledger import Ledger, LedgerOrderError
from nose.tools import *

def test_balances():
    ledger = Ledger('./tests/samples/ledger.txt')
    assert(ledger.balance('john') == -145.00)
    assert(ledger.balance('mary') == 25.00)
    assert(ledger.balance('supermarket') == 20.00)
    assert(ledger.balance('insurance') == 100.00)
    assert(ledger.balance('inexistent') == 0)

def test_day_balances():
    ledger = Ledger('./tests/samples/ledger.txt')
    assert(ledger.day_balance('2015-01-16', 'john') == -125.00)
    assert(ledger.day_balance('2015-01-16', 'mary') ==  125.00)
    assert(ledger.day_balance('2015-01-17', 'john') == -145.00)
    assert(ledger.day_balance('2015-01-17', 'supermarket') ==  20.00)
    assert(ledger.day_balance('2015-01-17', 'mary') ==  25.00)
    assert(ledger.day_balance('2015-01-17', 'insurance') == 100.00)

def test_before_and_after_dates():
    ledger = Ledger('./tests/samples/ledger.txt')
    assert(ledger.day_balance('2015-01-15', 'insurance') == 0)
    assert(ledger.day_balance('2015-01-17', 'supermarket') == 20.00)
    assert(ledger.day_balance('2015-01-18', 'supermarket') == 20.00)

@raises(LedgerOrderError)
def test_invalid_order_purchases():
    Ledger('./tests/samples/invalid_ledger.txt')
