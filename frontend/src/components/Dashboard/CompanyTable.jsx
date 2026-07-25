import { useEffect, useState } from "react";
import api from "../../services/api";

export default function CompanyTable() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [sortDir, setSortDir] = useState("desc");

    useEffect(() => {
        api.get("/dashboard/companies")
            .then((res) => {
                const normalised = res.data.map((d) => ({
                    name: d.company,
                    count: d.count ?? d["company"] ?? 0,
                }));
                setData(normalised);
            })
            .catch(() => setError("Failed to load company data."))
            .finally(() => setLoading(false));
    }, []);

    const sorted = [...data].sort((a, b) =>
        sortDir === "desc" ? b.count - a.count : a.count - b.count
    );

    const max = sorted[0]?.count || 1;

    return (
        <div className="chart-card">
            <div className="chart-card__header">
                <h3>Top Companies by Complaints</h3>
                <button
                    className="sort-btn"
                    onClick={() => setSortDir((d) => (d === "desc" ? "asc" : "desc"))}
                    aria-label="Toggle sort direction"
                >
                    {sortDir === "desc" ? "↓ Most first" : "↑ Least first"}
                </button>
            </div>

            {loading && <div className="chart-placeholder">Loading…</div>}
            {error && <div className="chart-error">{error}</div>}

            {!loading && !error && (
                <div className="company-table">
                    <table aria-label="Companies by complaint count">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Company</th>
                                <th>Complaints</th>
                                <th style={{ width: "30%" }}>Share</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sorted.map((row, i) => (
                                <tr key={row.name}>
                                    <td className="company-table__rank">{i + 1}</td>
                                    <td className="company-table__name">{row.name}</td>
                                    <td className="company-table__count">
                                        {row.count.toLocaleString()}
                                    </td>
                                    <td>
                                        <div className="company-table__bar-wrap">
                                            <div
                                                className="company-table__bar"
                                                style={{
                                                    width: `${(row.count / max) * 100}%`,
                                                }}
                                                aria-label={`${((row.count / max) * 100).toFixed(1)}%`}
                                            />
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
