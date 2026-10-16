# Transaction Analyzer

Processes a list of financial transactions and returns per-account summaries plus
the top spender (highest total debits).

## Run

```bash
python3 -m unittest -v
```

No third-party dependencies; Python 3 stdlib only.

## Usage

```python

result = analyze_transactions(transactions)
# {"summaries": [...], "topSpender": "A100"}
```

## Assumptions

- All accounts start with a balance of `0`.
- A valid `amount` is a positive `int` or `float`.
- `accountId` must be a non-empty string; `type` must be exactly `"credit"` or `"debit"`.
- `timestamp` is accepted but ignored: credits/debits are commutative and
  largest-amount is order-independent, so totals are correct regardless of input order.

## Tradeoffs / Design Choices

- Single pure function with dict-based aggregation — no classes or external
  libraries.

- Python was a good choice because its standard library provides built-in support for JSON formatting, calculations, 
    and unit testing, reducing the need for external dependencies.
