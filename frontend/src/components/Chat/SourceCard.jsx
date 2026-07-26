/**
 * Displays a retrieved complaint document used as RAG context.
 * source: one record from the retrieved_df (backend returns sources array)
 */
export default function SourceCard({ source, index }) {
    const {
        document,
        product,
        company,
        issue,
        state,
        score,
    } = source;

    // Truncate long narratives for the card preview
    const preview =
        document && document.length > 200
            ? document.slice(0, 200) + "…"
            : document || "No narrative available.";

    const relevance = score != null ? (score * 100).toFixed(1) : null;

    return (
        <div className="source-card">
            <div className="source-card__header">
                <span className="source-card__index">#{index + 1}</span>
                {relevance && (
                    <span className="source-card__score">{relevance}% match</span>
                )}
            </div>

            <p className="source-card__preview">{preview}</p>

            <div className="source-card__meta">
                {product && <span className="source-tag">{product}</span>}
                {company && <span className="source-tag">{company}</span>}
                {issue && <span className="source-tag source-tag--issue">{issue}</span>}
                {state && <span className="source-tag source-tag--state">{state}</span>}
            </div>
        </div>
    );
}
