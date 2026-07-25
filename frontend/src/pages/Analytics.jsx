import Layout from "../components/Layout/Layout";
import TrendChart from "../components/Charts/TrendChart";
import ProductChart from "../components/Charts/ProductChart";
import IssueChart from "../components/Charts/IssueChart";
import CompanyChart from "../components/Charts/CompanyChart";

export default function Analytics() {
    return (
        <Layout>
            <div className="page-shell">
                <div className="page-header">
                    <div>
                        <p className="eyebrow">Deep dive</p>
                        <h1>Analytics</h1>
                        <p>
                            Explore complaint volumes across time, products, companies, and
                            issue categories with interactive charts.
                        </p>
                    </div>
                    <div className="page-badge">Interactive</div>
                </div>

                {/* Full-width trend at the top */}
                <TrendChart />

                {/* 2-column grid for the remaining charts */}
                <div className="dashboard-grid" style={{ marginTop: "1.5rem" }}>
                    <ProductChart />
                    <IssueChart />
                    <CompanyChart />
                </div>
            </div>
        </Layout>
    );
}
