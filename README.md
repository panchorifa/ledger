Ledger Processor
=================
Processes purchases from ledger file in the following format:

```
2015-01-16,john,mary,125.00
2015-01-17,john,supermarket,20.00
2015-01-17,mary,insurance,100.00
```

### Setup

```
	pip install -r requirements_dev.txt;
```

### Testing

```
nosetests -c .noserc_local
```

Then check `test_results/coverage/index.html` for the HTML report.


### REPL

```
python market.py coins > market-"$(date +"%b-%d-%y[%H:%M:%S]")".log
```

Generates text file. ie: market-Jul-07-17[16:29:44].log
