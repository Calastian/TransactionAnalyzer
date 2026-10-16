import json


def analyze_transactions(transactions):
    accounts = {}

    for txn in transactions:
        account_id = txn.get("accountId")
        txn_type = txn.get("type")
        amount = txn.get("amount")

        if not isinstance(account_id, str) or account_id == "":
            continue
        if txn_type not in ("credit", "debit"):
            continue
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            continue

        account = accounts.setdefault(account_id, {
            "totalCredits": 0,
            "totalDebits": 0,
            "largestTransaction": 0,
            "transactionCount": 0,
        })

        if txn_type == "credit":
            account["totalCredits"] += amount
        else:
            account["totalDebits"] += amount

        account["largestTransaction"] = max(account["largestTransaction"], amount)
        account["transactionCount"] += 1

    summaries = []
    for account_id in sorted(accounts):
        account = accounts[account_id]
        ending_balance = account["totalCredits"] - account["totalDebits"]
        summaries.append({
            "accountId": account_id,
            "totalCredits": account["totalCredits"],
            "totalDebits": account["totalDebits"],
            "endingBalance": ending_balance,
            "largestTransaction": account["largestTransaction"],
            "transactionCount": account["transactionCount"],
            "overdrawn": ending_balance < 0,
        })

    top_spender = None
    top_debits = -1
    for summary in summaries:
        if summary["totalDebits"] > top_debits:
            top_debits = summary["totalDebits"]
            top_spender = summary["accountId"]
        elif summary["totalDebits"] == top_debits and summary["accountId"] < top_spender:
            top_spender = summary["accountId"]

    return {"summaries": summaries, "topSpender": top_spender}


if __name__ == "__main__":
    example = [
        {"accountId": "A100", "type": "credit", "amount": 500, "timestamp": "2026-05-10T10:00:00Z"},
        {"accountId": "A100", "type": "debit", "amount": 200, "timestamp": "2026-05-10T12:00:00Z"},
        {"accountId": "B200", "type": "debit", "amount": 50, "timestamp": "2026-05-10T11:00:00Z"},
        {"accountId": "B200", "type": "credit", "amount": 20, "timestamp": "2026-05-10T13:00:00Z"},
        {"accountId": "", "type": "credit", "amount": 100, "timestamp": "2026-05-10T14:00:00Z"},
    ]
    print(json.dumps(analyze_transactions(example), indent=2))
