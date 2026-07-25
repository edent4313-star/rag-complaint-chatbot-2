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
    "#778da9", "#415a77", "#1b263b", "#a8c4d4",
    "#5c7a9f", "#2e4a6b", "#6b92b8", "#9ab4c8",
    "#3d6080", "#8faec3",
];

export default function IssueChart() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get("/dashboard/issues")
            .then((res) => {
                const normalised = res.data.map((d) => ({
                    name: d.issue,
                    count: d.count ?? d["issue"] ?? 0,
                }));
                setData(normalised.slice(0, 10));
            })
            .catch(() => setError("Failed to load issue data."))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="chart-card">
            <div className="chart-card__header">
                <h3>Top Complaint Issues</h3>
                <span className="chart-card__subtitle">Top 10</span>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <ResponsiveContainer width="100%" height={280}>
                    <BarChart
                        data={data}
                        margin={{ top: 10, right: 20, left: 0, bottom: 80 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#e8edf3" />
                        <XAxis
                            dataKey="name"
                            tick={{ fontSize: 10 }}
                            angle={-35}
                            textAnchor="end"
                            interval={0}
                        />
                        <YAxis tick={{ fontSize: 11 }} width={55} />
                        <Tooltip
                            contentStyle={{ borderRadius: 8, fontSize: 13 }}
                            formatter={(v) => [v.toLocaleString(), "Complaints"]}
                        />
                        <Bar dataKey="count" radius={[4, 4, 0, 0]}>
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
