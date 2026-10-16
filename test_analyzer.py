import unittest

from analyzer import analyze_transactions


class TestAnalyzeTransactions(unittest.TestCase):
    def test_example_input(self):
        transactions = [
            {"accountId": "A100", "type": "credit", "amount": 500, "timestamp": "2026-05-10T10:00:00Z"},
            {"accountId": "A100", "type": "debit", "amount": 200, "timestamp": "2026-05-10T12:00:00Z"},
            {"accountId": "B200", "type": "debit", "amount": 50, "timestamp": "2026-05-10T11:00:00Z"},
            {"accountId": "B200", "type": "credit", "amount": 20, "timestamp": "2026-05-10T13:00:00Z"},
            {"accountId": "", "type": "credit", "amount": 100, "timestamp": "2026-05-10T14:00:00Z"},
        ]
        expected = {
            "summaries": [
                {
                    "accountId": "A100",
                    "totalCredits": 500,
                    "totalDebits": 200,
                    "endingBalance": 300,
                    "largestTransaction": 500,
                    "transactionCount": 2,
                    "overdrawn": False,
                },
                {
                    "accountId": "B200",
                    "totalCredits": 20,
                    "totalDebits": 50,
                    "endingBalance": -30,
                    "largestTransaction": 50,
                    "transactionCount": 2,
                    "overdrawn": True,
                },
            ],
            "topSpender": "A100",
        }
        self.assertEqual(analyze_transactions(transactions), expected)

    def test_empty_input(self):
        self.assertEqual(analyze_transactions([]), {"summaries": [], "topSpender": None})

    def test_all_invalid(self):
        transactions = [
            {"type": "credit", "amount": 100},
            {"accountId": "", "type": "credit", "amount": 100},
            {"accountId": None, "type": "credit", "amount": 100},
            {"accountId": "A100", "type": "refund", "amount": 100},
            {"accountId": "A100", "type": "credit", "amount": 0},
            {"accountId": "A100", "type": "credit", "amount": -10},
            {"accountId": "A100", "type": "credit", "amount": "100"},
        ]
        self.assertEqual(analyze_transactions(transactions), {"summaries": [], "topSpender": None})

    def test_top_spender_tie_lexicographic(self):
        transactions = [
            {"accountId": "B200", "type": "debit", "amount": 100},
            {"accountId": "A100", "type": "debit", "amount": 100},
        ]
        result = analyze_transactions(transactions)
        self.assertEqual(result["topSpender"], "A100")

    def test_zero_balance_not_overdrawn(self):
        transactions = [
            {"accountId": "A100", "type": "credit", "amount": 100},
            {"accountId": "A100", "type": "debit", "amount": 100},
        ]
        summary = analyze_transactions(transactions)["summaries"][0]
        self.assertEqual(summary["endingBalance"], 0)
        self.assertFalse(summary["overdrawn"])

    def test_unsorted_timestamps(self):
        transactions = [
            {"accountId": "A100", "type": "debit", "amount": 200, "timestamp": "2026-05-10T12:00:00Z"},
            {"accountId": "A100", "type": "credit", "amount": 500, "timestamp": "2026-05-10T10:00:00Z"},
        ]
        summary = analyze_transactions(transactions)["summaries"][0]
        self.assertEqual(summary["totalCredits"], 500)
        self.assertEqual(summary["totalDebits"], 200)

    def test_float_amounts(self):
        transactions = [
            {"accountId": "A100", "type": "credit", "amount": 100.50},
            {"accountId": "A100", "type": "debit", "amount": 25.25},
        ]
        summary = analyze_transactions(transactions)["summaries"][0]
        self.assertEqual(summary["totalCredits"], 100.50)
        self.assertEqual(summary["endingBalance"], 75.25)

    def test_sorted_by_account_id(self):
        transactions = [
            {"accountId": "C300", "type": "credit", "amount": 1},
            {"accountId": "A100", "type": "credit", "amount": 1},
            {"accountId": "B200", "type": "credit", "amount": 1},
        ]
        ids = [s["accountId"] for s in analyze_transactions(transactions)["summaries"]]
        self.assertEqual(ids, ["A100", "B200", "C300"])

    def test_boolean_amount_rejected(self):
        transactions = [
            {"accountId": "A100", "type": "credit", "amount": True},
        ]
        self.assertEqual(analyze_transactions(transactions), {"summaries": [], "topSpender": None})


if __name__ == "__main__":
    unittest.main()
