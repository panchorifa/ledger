"""
service tests
"""
from ledger.ledger import Ledger, LedgerOrderError
from nose.tools import *

def test_balances():
    ledger = Ledger('./tests/samples/ledger.txt')
    assert(ledger.balances['john'] == -145.00)
    assert(ledger.balances['mary'] == 25.00)
    assert(ledger.balances['supermarket'] == 20.00)
    assert(ledger.balances['insurance'] == 100.00)

@raises(LedgerOrderError)
def test_invalid_order_purchases():
    Ledger('./tests/samples/invalid_ledger.txt')
