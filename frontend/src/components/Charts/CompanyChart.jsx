import { useEffect, useState } from "react";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Cell,
    ResponsiveContainer,
} from "recharts";
import api from "../../services/api";

const COLORS = [
    "#1b263b", "#2e4a6b", "#415a77", "#5c7a9f",
    "#778da9", "#8faec3", "#a8c4d4", "#6b92b8",
    "#9ab4c8", "#3d6080",
];

/**
 * Bar chart of top companies — used on the Analytics page.
 */
export default function CompanyChart() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get("/dashboard/companies")
            .then((res) => {
                const normalised = res.data.map((d) => ({
                    name: d.company.length > 20 ? d.company.slice(0, 20) + "…" : d.company,
                    count: d.count ?? 0,
                }));
                setData(normalised.slice(0, 10));
            })
            .catch(() => setError("Failed to load company data."))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="chart-card">
            <div className="chart-card__header">
                <h3>Company Complaint Volume</h3>
                <span className="chart-card__subtitle">Top 10 companies</span>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <ResponsiveContainer width="100%" height={320}>
                    <BarChart
                        data={data}
                        layout="vertical"
                        margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#e8edf3" horizontal={false} />
                        <XAxis type="number" tick={{ fontSize: 11 }} />
                        <YAxis type="category" dataKey="name" width={150} tick={{ fontSize: 11 }} />
                        <Tooltip
                            contentStyle={{ borderRadius: 8, fontSize: 13 }}
                            formatter={(v) => [v.toLocaleString(), "Complaints"]}
                        />
                        <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                            {data.map((_, i) => (
                                <Cell key={i} fill={COLORS[i % COLORS.length]} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}
