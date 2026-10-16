# Master Plan: Transaction Analyzer

## Goal
Process a list of financial transactions and produce per-account summaries plus a
`topSpender` (highest total debits; ties broken lexicographically).

## Stack & Dependencies
- **Language:** Python 3.14 (stdlib only — no third-party dependencies)
- **Testing:** `unittest` (stdlib)
- **Runner:** `python3 -m unittest`

| Purpose         | Tool                  | Dep? |
|-----------------|-----------------------|------|
| Core logic      | `analyzer.py`         | none |
| Unit tests      | `test_analyzer.py`    | `unittest` |
| Docs            | `README.md`, `PLAN.md`| none |

## File Structure
```
TransactionAnalyzer/
├── analyzer.py        # analyze_transactions(transactions) -> dict
├── test_analyzer.py   # unittest coverage
├── README.md          # run instructions, assumptions, tradeoffs
├── PLAN.md            # this plan
└── AGENTS.md          # (existing)
```

## Design
- Single pure function `analyze_transactions(transactions)`.
- No classes, no external libs, no sorting dependency on timestamp.
- Validate + aggregate in one pass.

## Validation rules (ignore a transaction if)
- `accountId` missing, empty, or not a string
- `type` not `"credit"` or `"debit"`
- `amount` not an int/float, or `<= 0`

## Per-account summary
- `totalCredits`, `totalDebits`, `endingBalance = credits - debits`
- `largestTransaction` = max valid amount
- `transactionCount` = number of valid transactions
- `overdrawn` = `endingBalance < 0`

## topSpender
- Max `totalDebits`; tie → lexicographically smaller `accountId`; `None` if no valid txns.

## Test cases
1. Example input → example output
2. Empty input → `summaries: []`, `topSpender: None`
3. All-invalid input → same as empty
4. Each invalid field type ignored
5. topSpender tie → lexicographic smaller
6. Overdrawn: negative → true, zero → false
7. Unsorted timestamps → correct totals
8. Float amounts

## Assumptions / Tradeoffs
- Timestamp is accepted but unused: credits/debits are commutative, so order
  doesn't affect totals/largest. Keeps output deterministic without sorting.
- Balance starts at 0; `amount` is positive when valid.
- Simple dict-based aggregation chosen over dataclasses/classes for minimal code.
