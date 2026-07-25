import { useState } from "react";
import Layout from "../components/Layout/Layout";
import api from "../services/api";

const METRICS_INFO = {
    faithfulness:
        "Measures how factually consistent the answer is with the retrieved sources. Score: 0–1.",
    answer_relevance:
        "Measures how relevant the answer is to the question asked. Score: 0–1.",
    context_recall:
        "Measures how much of the expected answer is covered by the retrieved context. Score: 0–1.",
    context_precision:
        "Measures the signal-to-noise ratio of retrieved documents. Score: 0–1.",
};

function ScoreBar({ label, value, description }) {
    const pct = Math.round((value ?? 0) * 100);
    const color =
        pct >= 75 ? "#2d7a4f" : pct >= 50 ? "#b07d2e" : "#c0392b";

    return (
        <div className="eval-metric">
            <div className="eval-metric__header">
                <span className="eval-metric__label">{label}</span>
                <span className="eval-metric__score" style={{ color }}>
                    {value != null ? value.toFixed(3) : "—"}
                </span>
            </div>
            <div className="eval-metric__bar-track">
                <div
                    className="eval-metric__bar-fill"
                    style={{ width: `${pct}%`, background: color }}
                    role="progressbar"
                    aria-valuenow={pct}
                    aria-valuemin={0}
                    aria-valuemax={100}
                />
            </div>
            <p className="eval-metric__desc">{description}</p>
        </div>
    );
}

export default function Evaluation() {
    const [question, setQuestion] = useState("");
    const [groundTruth, setGroundTruth] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    async function handleEvaluate(e) {
        e.preventDefault();
        if (!question.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            // Step 1 — get the RAG answer + sources
            const chatRes = await api.post("/chat", { question });
            const { answer, sources } = chatRes.data;

            const contexts = (sources || [])
                .map((s) => s.document)
                .filter(Boolean);

            // Step 2 — run evaluation
            const evalRes = await api.post("/evaluate", {
                question,
                answer,
                contexts,
                ground_truth: groundTruth.trim() || null,
            });

            setResult({ answer, sources, metrics: evalRes.data });
        } catch (err) {
            if (err.response?.status === 404) {
                setError(
                    "Could not reach /api/evaluate. Make sure the Flask backend is running " +
                    "(python app.py) and has been restarted after the latest changes."
                );
            } else if (err.response?.data?.error) {
                setError(err.response.data.error);
            } else {
                setError(err.message || "An unexpected error occurred.");
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <Layout>
            <div className="page-shell">
                <div className="page-header">
                    <div>
                        <p className="eyebrow">RAG quality</p>
                        <h1>Evaluation</h1>
                        <p>
                            Enter a question to run the full RAG pipeline and score the output
                            on faithfulness, relevance, context recall, and precision.
                        </p>
                    </div>
                    <div className="page-badge">RAGAS metrics</div>
                </div>

                {/* ── Input form ── */}
                <form className="eval-form" onSubmit={handleEvaluate}>
                    <div className="eval-form__field">
                        <label htmlFor="eval-question">Question</label>
                        <textarea
                            id="eval-question"
                            rows={3}
                            placeholder="e.g. What are the most common mortgage complaints?"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            required
                        />
                    </div>

                    <div className="eval-form__field">
                        <label htmlFor="eval-ground-truth">
                            Ground-truth answer{" "}
                            <span className="eval-form__optional">(optional — improves context_recall score)</span>
                        </label>
                        <textarea
                            id="eval-ground-truth"
                            rows={3}
                            placeholder="Provide the ideal answer if you know it…"
                            value={groundTruth}
                            onChange={(e) => setGroundTruth(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        className="eval-form__btn"
                        disabled={loading || !question.trim()}
                    >
                        {loading ? "Evaluating…" : "Run Evaluation"}
                    </button>
                </form>

                {error && (
                    <div className="eval-error" role="alert">
                        {error}
                    </div>
                )}

                {/* ── Results ── */}
                {result && (
                    <div className="eval-results">
                        <section className="eval-results__section">
                            <h3>Generated Answer</h3>
                            <div className="eval-answer-box">{result.answer}</div>
                        </section>

                        <section className="eval-results__section">
                            <h3>RAG Scores</h3>
                            <div className="eval-metrics-grid">
                                {Object.entries(result.metrics).map(([key, value]) => (
                                    <ScoreBar
                                        key={key}
                                        label={key.replace(/_/g, " ")}
                                        value={value}
                                        description={METRICS_INFO[key] ?? ""}
                                    />
                                ))}
                            </div>
                        </section>

                        {result.sources?.length > 0 && (
                            <section className="eval-results__section">
                                <h3>Retrieved Records ({result.sources.length})</h3>
                                <div className="eval-sources">
                                    {result.sources.map((s, i) => (
                                        <div key={i} className="eval-source-item">
                                            <span className="eval-source-item__index">#{i + 1}</span>
                                            <div>
                                                <p className="eval-source-item__meta">
                                                    {[s.product, s.company, s.issue]
                                                        .filter(Boolean)
                                                        .join(" · ")}
                                                </p>
                                                <p className="eval-source-item__text">
                                                    {s.document?.slice(0, 250)}
                                                    {s.document?.length > 250 ? "…" : ""}
                                                </p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </section>
                        )}
                    </div>
                )}
            </div>
        </Layout>
    );
}
