"""
service tests
"""
from ledger.ledger import Ledger

def test_balances():
    ledger = Ledger('./ledger/ledger.txt')
    assert(ledger.balance['john'] == -145.00)
    assert(ledger.balance['mary'] == 25.00)
    assert(ledger.balance['supermarket'] == 20.00)
    assert(ledger.balance['insurance'] == 100.00)
