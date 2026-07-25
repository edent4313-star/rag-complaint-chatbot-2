from flask import Blueprint

from services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")

service = DashboardService()


@dashboard_bp.get("/kpis")
def kpis():
    return service.get_kpis()


@dashboard_bp.get("/products")
def products():
    return service.product_distribution()


@dashboard_bp.get("/issues")
def issues():
    return service.top_issues()


@dashboard_bp.get("/companies")
def companies():
    return service.top_companies()


@dashboard_bp.get("/trends")
def trends():
    return service.monthly_trend()
