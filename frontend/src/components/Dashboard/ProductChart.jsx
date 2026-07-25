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
    "#1b263b", "#415a77", "#778da9", "#a8c4d4",
    "#5c7a9f", "#2e4a6b", "#6b92b8", "#9ab4c8",
    "#3d6080", "#8faec3",
];

export default function ProductChart() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get("/dashboard/products")
            .then((res) => {
                // Normalise: backend returns [{product, count}] or [{product: "x", "product": n}]
                const normalised = res.data.map((d) => ({
                    name: d.product,
                    count: d.count ?? d["product"] ?? 0,
                }));
                setData(normalised.slice(0, 10));
            })
            .catch(() => setError("Failed to load product data."))
            .finally(() => setLoading(false));
    }, []);

    const CustomTick = ({ x, y, payload }) => {
        const words = payload.value.split(" ");
        return (
            <text x={x} y={y} textAnchor="end" fill="#555" fontSize={11}>
                {words.map((w, i) => (
                    <tspan key={i} x={x} dy={i === 0 ? 0 : 12}>
                        {w}
                    </tspan>
                ))}
            </text>
        );
    };

    return (
        <div className="chart-card">
            <div className="chart-card__header">
                <h3>Complaints by Product</h3>
                <span className="chart-card__subtitle">Top 10</span>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <ResponsiveContainer width="100%" height={280}>
                    <BarChart
                        data={data}
                        layout="vertical"
                        margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#e8edf3" horizontal={false} />
                        <XAxis type="number" tick={{ fontSize: 11 }} />
                        <YAxis
                            type="category"
                            dataKey="name"
                            width={160}
                            tick={{ fontSize: 11 }}
                        />
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
