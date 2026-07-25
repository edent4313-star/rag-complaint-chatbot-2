import { useEffect, useState } from "react";
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";
import api from "../../services/api";

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

    // Show only the last 24 months to keep the chart readable
    const displayData = data.slice(-24);

    return (
        <div className="chart-card">
            <div className="chart-card__header">
                <h3>Monthly Complaint Trend</h3>
                <span className="chart-card__subtitle">Last 24 months</span>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <ResponsiveContainer width="100%" height={260}>
                    <AreaChart
                        data={displayData}
                        margin={{ top: 10, right: 20, left: 0, bottom: 40 }}
                    >
                        <defs>
                            <linearGradient id="trendGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#415a77" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#415a77" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e8edf3" />
                        <XAxis
                            dataKey="month"
                            tick={{ fontSize: 11 }}
                            angle={-45}
                            textAnchor="end"
                            interval={2}
                        />
                        <YAxis tick={{ fontSize: 11 }} width={50} />
                        <Tooltip
                            contentStyle={{ borderRadius: 8, fontSize: 13 }}
                            formatter={(v) => [v.toLocaleString(), "Complaints"]}
                        />
                        <Area
                            type="monotone"
                            dataKey="count"
                            stroke="#415a77"
                            strokeWidth={2}
                            fill="url(#trendGrad)"
                            dot={false}
                            activeDot={{ r: 5 }}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}
