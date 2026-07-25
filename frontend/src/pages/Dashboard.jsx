import Layout from "../components/Layout/Layout";
import KPICards from "../components/Dashboard/KPICards";
import TrendChart from "../components/Dashboard/TrendChart";
import ProductChart from "../components/Dashboard/ProductChart";
import IssueChart from "../components/Dashboard/IssueChart";
import CompanyTable from "../components/Dashboard/CompanyTable";

export default function Dashboard() {
    return (
        <Layout>
            <div className="page-shell">
                <div className="page-header">
                    <div>
                        <p className="eyebrow">Customer complaint intelligence</p>
                        <h1>Executive dashboard</h1>
                        <p>Track complaint growth, product hotspots, and recurring issues in one view.</p>
                    </div>
                    <div className="page-badge">Live insights</div>
                </div>

                <KPICards />

                <div className="dashboard-grid">
                    <TrendChart />
                    <ProductChart />
                    <IssueChart />
                    <CompanyTable />
                </div>
            </div>
        </Layout>
    );
}