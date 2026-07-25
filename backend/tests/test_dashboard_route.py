"""
Integration tests for all dashboard API routes.
conftest.py autouse fixture patches retriever I/O.
DashboardService CSV read is patched inline.
"""
import pytest
import pandas as pd
from unittest.mock import patch

FAKE_CSV = pd.DataFrame({
    "Date received":                ["2023-01", "2023-02", "2023-02"],
    "Sub-product":                  ["Mortgage", "Credit card", "Mortgage"],
    "Issue":                        ["Loan denial", "Billing error", "Loan denial"],
    "Company":                      ["Bank A", "Bank B", "Bank A"],
    "State":                        ["CA", "TX", "CA"],
    "Consumer complaint narrative": ["text one", "text two", "text three"],
})


@pytest.fixture
def client():
    with patch("services.dashboard_service.pd.read_csv", return_value=FAKE_CSV.copy()):
        # Force DashboardService to re-instantiate with the mock CSV
        import importlib
        import services.dashboard_service as ds_mod
        importlib.reload(ds_mod)
        import routes.dashboard as dash_mod
        dash_mod.service = ds_mod.DashboardService()

        from app import app
        app.config["TESTING"] = True
        yield app.test_client()


class TestDashboardKPIs:
    def test_kpis_returns_200(self, client):
        assert client.get("/api/dashboard/kpis").status_code == 200

    def test_kpis_has_required_keys(self, client):
        data = client.get("/api/dashboard/kpis").get_json()
        for key in ("total_complaints", "products", "companies", "states", "average_length"):
            assert key in data

    def test_total_complaints_is_correct(self, client):
        data = client.get("/api/dashboard/kpis").get_json()
        assert data["total_complaints"] == 3

    def test_companies_count(self, client):
        data = client.get("/api/dashboard/kpis").get_json()
        assert data["companies"] == 2  # Bank A, Bank B


class TestDashboardProducts:
    def test_returns_200(self, client):
        assert client.get("/api/dashboard/products").status_code == 200

    def test_is_list(self, client):
        assert isinstance(client.get("/api/dashboard/products").get_json(), list)

    def test_items_have_correct_keys(self, client):
        for item in client.get("/api/dashboard/products").get_json():
            assert "product" in item and "count" in item


class TestDashboardIssues:
    def test_returns_200(self, client):
        assert client.get("/api/dashboard/issues").status_code == 200

    def test_at_most_ten(self, client):
        assert len(client.get("/api/dashboard/issues").get_json()) <= 10


class TestDashboardCompanies:
    def test_returns_200(self, client):
        assert client.get("/api/dashboard/companies").status_code == 200

    def test_is_list(self, client):
        assert isinstance(client.get("/api/dashboard/companies").get_json(), list)


class TestDashboardTrends:
    def test_returns_200(self, client):
        assert client.get("/api/dashboard/trends").status_code == 200

    def test_items_have_month_and_count(self, client):
        for item in client.get("/api/dashboard/trends").get_json():
            assert "month" in item and "count" in item
