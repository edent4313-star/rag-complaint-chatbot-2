import { useEffect, useState } from "react";
import {
    RadarChart,
    Radar,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";
import api from "../../services/api";

/**
 * Radar chart of top complaint issues — used on the Analytics page.
 */
export default function IssueChart() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.get("/dashboard/issues")
            .then((res) => {
                const normalised = res.data.map((d) => ({
                    subject: d.issue.length > 28 ? d.issue.slice(0, 28) + "…" : d.issue,
                    count: d.count ?? 0,
                }));
                setData(normalised.slice(0, 8));
            })
            .catch(() => setError("Failed to load issue data."))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="chart-card">
            <div className="chart-card__header">
                <h3>Issue Radar</h3>
                <span className="chart-card__subtitle">Top 8 complaint categories</span>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <ResponsiveContainer width="100%" height={320}>
                    <RadarChart data={data} margin={{ top: 10, right: 30, left: 30, bottom: 10 }}>
                        <PolarGrid stroke="#e8edf3" />
                        <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10 }} />
                        <PolarRadiusAxis tick={{ fontSize: 9 }} />
                        <Tooltip
                            contentStyle={{ borderRadius: 8, fontSize: 13 }}
                            formatter={(v) => [v.toLocaleString(), "Complaints"]}
                        />
                        <Radar
                            name="Complaints"
                            dataKey="count"
                            stroke="#415a77"
                            fill="#415a77"
                            fillOpacity={0.35}
                        />
                    </RadarChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}
