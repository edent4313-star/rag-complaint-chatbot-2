import { useEffect, useState } from "react";
import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";
import api from "../../services/api";

const COLORS = [
    "#1b263b", "#415a77", "#778da9", "#a8c4d4",
    "#5c7a9f", "#2e4a6b", "#6b92b8", "#9ab4c8",
    "#3d6080", "#8faec3",
];

const RADIAN = Math.PI / 180;
const renderLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    if (percent < 0.04) return null;
    const r = innerRadius + (outerRadius - innerRadius) * 0.55;
    const x = cx + r * Math.cos(-midAngle * RADIAN);
    const y = cy + r * Math.sin(-midAngle * RADIAN);
    return (
        <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={11}>
            {`${(percent * 100).toFixed(1)}%`}
        </text>
    );
};

/**
 * Pie chart used on the Analytics page.
 */
export default function ProductChart() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get("/dashboard/products")
            .then((res) => {
                const normalised = res.data.map((d) => ({
                    name: d.product,
                    value: d.count ?? 0,
                }));
                setData(normalised.slice(0, 10));
            })
            .catch(() => setError("Failed to load product data."))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="chart-card">
            <div className="chart-card__header">
                <h3>Product Distribution</h3>
                <span className="chart-card__subtitle">Top 10 by complaint volume</span>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <ResponsiveContainer width="100%" height={320}>
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            outerRadius={110}
                            dataKey="value"
                            labelLine={false}
                            label={renderLabel}
                        >
                            {data.map((_, i) => (
                                <Cell key={i} fill={COLORS[i % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{ borderRadius: 8, fontSize: 13 }}
                            formatter={(v) => [v.toLocaleString(), "Complaints"]}
                        />
                        <Legend
                            iconType="circle"
                            iconSize={10}
                            wrapperStyle={{ fontSize: 11 }}
                        />
                    </PieChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}
