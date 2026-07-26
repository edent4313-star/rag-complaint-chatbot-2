"""
Integration tests for all dashboard API routes.
CSV and retriever I/O are mocked via conftest fixtures — no files needed.
"""
import pytest


# Uses the shared app + client fixtures from conftest.py
# (which already mock pd.read_csv via mock_csv and reset the lazy service)


class TestDashboardKPIs:

    def test_kpis_returns_200(self, client):
        assert client.get("/api/dashboard/kpis").status_code == 200

    def test_kpis_has_required_keys(self, client):
        data = client.get("/api/dashboard/kpis").get_json()
        for key in ("total_complaints", "products", "companies", "states", "average_length"):
            assert key in data

    def test_total_complaints_is_correct(self, client):
        data = client.get("/api/dashboard/kpis").get_json()
        assert data["total_complaints"] == 2

    def test_companies_count(self, client):
        data = client.get("/api/dashboard/kpis").get_json()
        assert data["companies"] == 2


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
