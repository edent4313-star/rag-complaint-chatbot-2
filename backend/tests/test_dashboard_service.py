"""
Unit tests for DashboardService.
Uses an in-memory DataFrame so no CSV file is required.
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from flask import Flask


# ── Build a minimal fake CSV DataFrame ────────────────────────────────────────

FAKE_CSV_DATA = {
    "Date received":               ["2023-01", "2023-02", "2023-02", "2023-03", "2023-03"],
    "Product":                     [None, None, None, None, None],  # always null in real data
    "Sub-product":                 ["Mortgage", "Credit card", "Mortgage", "Student loan", "Credit card"],
    "Issue":                       ["Loan denial", "Billing error", "Loan denial", "Payment issue", "Fraud"],
    "Sub-issue":                   ["", "", "", "", ""],
    "Consumer complaint narrative":["Long narrative one.", "Long narrative two.", "Three.", "Four.", "Five."],
    "Company public response":     ["", "", "", "", ""],
    "Company":                     ["Bank A", "Bank B", "Bank A", "Bank C", "Bank B"],
    "State":                       ["CA", "TX", "CA", "NY", "TX"],
    "ZIP code":                    ["90001", "75001", "90002", "10001", "75002"],
    "Tags":                        ["", "", "", "", ""],
    "Consumer consent provided?":  ["Yes", "Yes", "Yes", "Yes", "Yes"],
    "Submitted via":               ["Web", "Web", "Web", "Web", "Web"],
    "Date sent to company":        ["2023-01", "2023-02", "2023-02", "2023-03", "2023-03"],
    "Company response to consumer":["Closed", "Closed", "Closed", "Closed", "Closed"],
    "Timely response?":            ["Yes", "Yes", "Yes", "Yes", "Yes"],
    "Consumer disputed?":          ["No", "No", "No", "No", "No"],
    "Complaint ID":                [1, 2, 3, 4, 5],
    "word_count":                  [3, 3, 1, 1, 1],
    "cleaned_narrative":           ["narrative", "narrative", "narrative", "narrative", "narrative"],
}
FAKE_DF = pd.DataFrame(FAKE_CSV_DATA)


@pytest.fixture
def svc():
    """DashboardService with CSV reading patched out."""
    with patch("services.dashboard_service.pd.read_csv", return_value=FAKE_DF.copy()):
        from services.dashboard_service import DashboardService
        service = DashboardService()
    return service


@pytest.fixture
def flask_ctx():
    """Minimal Flask app context so jsonify works."""
    app = Flask(__name__)
    with app.app_context():
        yield


class TestGetKPIs:

    def test_total_complaints(self, svc, flask_ctx):
        data = svc.get_kpis().get_json()
        assert data["total_complaints"] == 5

    def test_companies_count(self, svc, flask_ctx):
        data = svc.get_kpis().get_json()
        assert data["companies"] == 3  # Bank A, B, C

    def test_states_count(self, svc, flask_ctx):
        data = svc.get_kpis().get_json()
        assert data["states"] == 3  # CA, TX, NY

    def test_products_count(self, svc, flask_ctx):
        data = svc.get_kpis().get_json()
        assert data["products"] == 3  # Mortgage, Credit card, Student loan

    def test_average_length_is_float(self, svc, flask_ctx):
        data = svc.get_kpis().get_json()
        assert isinstance(data["average_length"], float)
        assert data["average_length"] >= 0


class TestProductDistribution:

    def test_returns_list(self, svc, flask_ctx):
        data = svc.product_distribution().get_json()
        assert isinstance(data, list)

    def test_each_item_has_product_and_count(self, svc, flask_ctx):
        data = svc.product_distribution().get_json()
        for item in data:
            assert "product" in item
            assert "count" in item

    def test_counts_are_positive_integers(self, svc, flask_ctx):
        data = svc.product_distribution().get_json()
        for item in data:
            assert isinstance(item["count"], int)
            assert item["count"] > 0

    def test_mortgage_appears_twice(self, svc, flask_ctx):
        data = svc.product_distribution().get_json()
        mortgage = next((d for d in data if d["product"] == "Mortgage"), None)
        assert mortgage is not None
        assert mortgage["count"] == 2


class TestTopIssues:

    def test_returns_at_most_ten(self, svc, flask_ctx):
        data = svc.top_issues().get_json()
        assert len(data) <= 10

    def test_each_item_has_issue_and_count(self, svc, flask_ctx):
        data = svc.top_issues().get_json()
        for item in data:
            assert "issue" in item
            assert "count" in item

    def test_loan_denial_count_is_two(self, svc, flask_ctx):
        data = svc.top_issues().get_json()
        denial = next((d for d in data if d["issue"] == "Loan denial"), None)
        assert denial is not None
        assert denial["count"] == 2


class TestTopCompanies:

    def test_returns_at_most_ten(self, svc, flask_ctx):
        data = svc.top_companies().get_json()
        assert len(data) <= 10

    def test_bank_a_appears_twice(self, svc, flask_ctx):
        data = svc.top_companies().get_json()
        bank_a = next((d for d in data if d["company"] == "Bank A"), None)
        assert bank_a is not None
        assert bank_a["count"] == 2


class TestMonthlyTrend:

    def test_returns_list(self, svc, flask_ctx):
        data = svc.monthly_trend().get_json()
        assert isinstance(data, list)

    def test_each_item_has_month_and_count(self, svc, flask_ctx):
        data = svc.monthly_trend().get_json()
        for item in data:
            assert "month" in item
            assert "count" in item

    def test_months_are_sorted(self, svc, flask_ctx):
        data = svc.monthly_trend().get_json()
        months = [d["month"] for d in data]
        assert months == sorted(months)
