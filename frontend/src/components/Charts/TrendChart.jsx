import { useEffect, useState } from "react";
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";
import api from "../../services/api";

/**
 * Full-width trend chart used on the Analytics page.
 * Shows the complete monthly complaint history (not capped to 24).
 */
export default function TrendChart() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get("/dashboard/trends")
            .then((res) => setData(res.data))
            .catch(() => setError("Failed to load trend data."))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="chart-card chart-card--full">
            <div className="chart-card__header">
                <h3>Full Complaint History</h3>
                <span className="chart-card__subtitle">All months on record</span>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 50 }}>
                        <defs>
                            <linearGradient id="fullTrendGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#1b263b" stopOpacity={0.25} />
                                <stop offset="95%" stopColor="#1b263b" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e8edf3" />
                        <XAxis dataKey="month" tick={{ fontSize: 10 }} angle={-45} textAnchor="end" interval={5} />
                        <YAxis tick={{ fontSize: 11 }} width={55} />
                        <Tooltip
                            contentStyle={{ borderRadius: 8, fontSize: 13 }}
                            formatter={(v) => [v.toLocaleString(), "Complaints"]}
                        />
                        <Legend verticalAlign="top" />
                        <Area
                            type="monotone"
                            dataKey="count"
                            name="Complaints"
                            stroke="#1b263b"
                            strokeWidth={2}
                            fill="url(#fullTrendGrad)"
                            dot={false}
                            activeDot={{ r: 5 }}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}
