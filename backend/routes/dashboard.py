from flask import Blueprint

from services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")

# Lazy singleton — instantiated on first request so tests can mock pd.read_csv
_service = None


def _get_service():
    global _service
    if _service is None:
        _service = DashboardService()
    return _service


@dashboard_bp.get("/kpis")
def kpis():
    return _get_service().get_kpis()


@dashboard_bp.get("/products")
def products():
    return _get_service().product_distribution()


@dashboard_bp.get("/issues")
def issues():
    return _get_service().top_issues()


@dashboard_bp.get("/companies")
def companies():
    return _get_service().top_companies()


@dashboard_bp.get("/trends")
def trends():
    return _get_service().monthly_trend()
