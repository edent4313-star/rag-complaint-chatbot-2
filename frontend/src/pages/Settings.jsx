import { useState } from "react";
import Layout from "../components/Layout/Layout";
import {
    MdCheckCircle,
    MdStorage,
    MdSmartToy,
    MdTune,
    MdSearch,
} from "react-icons/md";

const MODEL_OPTIONS = [
    { id: "qwen", label: "Qwen2.5-0.5B-Instruct", tag: "default", note: "Runs on CPU. Fast but compact." },
    { id: "flan", label: "google/flan-t5-large", tag: "alt", note: "Seq2Seq model. Lower memory use." },
];

const EMBEDDING_OPTIONS = [
    { id: "minilm", label: "all-MiniLM-L6-v2", tag: "default", note: "Fast, 384-dim sentence embeddings." },
    { id: "mpnet", label: "all-mpnet-base-v2", tag: "high quality", note: "768-dim, slower but more accurate." },
];

function SettingsSection({ icon, title, children }) {
    return (
        <section className="settings-section">
            <div className="settings-section__header">
                {icon}
                <h3>{title}</h3>
            </div>
            <div className="settings-section__body">{children}</div>
        </section>
    );
}

function RadioGroup({ options, value, onChange }) {
    return (
        <div className="settings-radio-group">
            {options.map((opt) => (
                <label
                    key={opt.id}
                    className={`settings-radio-option ${value === opt.id ? "settings-radio-option--active" : ""}`}
                >
                    <input
                        type="radio"
                        name={opt.id}
                        value={opt.id}
                        checked={value === opt.id}
                        onChange={() => onChange(opt.id)}
                    />
                    <div className="settings-radio-option__content">
                        <div className="settings-radio-option__label">
                            {opt.label}
                            <span className="settings-tag">{opt.tag}</span>
                        </div>
                        <p className="settings-radio-option__note">{opt.note}</p>
                    </div>
                    {value === opt.id && (
                        <MdCheckCircle className="settings-radio-option__check" />
                    )}
                </label>
            ))}
        </div>
    );
}

export default function Settings() {
    const [llmModel, setLlmModel] = useState("qwen");
    const [embeddingModel, setEmbeddingModel] = useState("minilm");
    const [topK, setTopK] = useState(5);
    const [temperature, setTemperature] = useState(0.7);
    const [maxNewTokens, setMaxNewTokens] = useState(300);
    const [saved, setSaved] = useState(false);

    function handleSave(e) {
        e.preventDefault();
        // In a real integration these values would POST to /api/settings
        setSaved(true);
        setTimeout(() => setSaved(false), 2500);
    }

    return (
        <Layout>
            <div className="page-shell">
                <div className="page-header">
                    <div>
                        <p className="eyebrow">Configuration</p>
                        <h1>Settings</h1>
                        <p>
                            Adjust the language model, embedding model, retrieval depth,
                            and generation parameters for the RAG pipeline.
                        </p>
                    </div>
                    <div className="page-badge">Local only</div>
                </div>

                <form className="settings-form" onSubmit={handleSave}>
                    {/* LLM */}
                    <SettingsSection icon={<MdSmartToy />} title="Language Model">
                        <RadioGroup
                            options={MODEL_OPTIONS}
                            value={llmModel}
                            onChange={setLlmModel}
                        />
                    </SettingsSection>

                    {/* Embeddings */}
                    <SettingsSection icon={<MdStorage />} title="Embedding Model">
                        <RadioGroup
                            options={EMBEDDING_OPTIONS}
                            value={embeddingModel}
                            onChange={setEmbeddingModel}
                        />
                    </SettingsSection>

                    {/* Retrieval */}
                    <SettingsSection icon={<MdSearch />} title="Retrieval">
                        <div className="settings-sliders">
                            <div className="settings-slider-field">
                                <label htmlFor="top-k">
                                    Top-K retrieved documents
                                    <span className="settings-slider-value">{topK}</span>
                                </label>
                                <input
                                    id="top-k"
                                    type="range"
                                    min={1}
                                    max={20}
                                    step={1}
                                    value={topK}
                                    onChange={(e) => setTopK(Number(e.target.value))}
                                />
                                <div className="settings-slider-range">
                                    <span>1</span><span>20</span>
                                </div>
                            </div>
                        </div>
                    </SettingsSection>

                    {/* Generation */}
                    <SettingsSection icon={<MdTune />} title="Generation">
                        <div className="settings-sliders">
                            <div className="settings-slider-field">
                                <label htmlFor="temperature">
                                    Temperature
                                    <span className="settings-slider-value">{temperature}</span>
                                </label>
                                <input
                                    id="temperature"
                                    type="range"
                                    min={0.1}
                                    max={1.5}
                                    step={0.05}
                                    value={temperature}
                                    onChange={(e) => setTemperature(Number(e.target.value))}
                                />
                                <div className="settings-slider-range">
                                    <span>0.1 (precise)</span><span>1.5 (creative)</span>
                                </div>
                            </div>

                            <div className="settings-slider-field">
                                <label htmlFor="max-tokens">
                                    Max new tokens
                                    <span className="settings-slider-value">{maxNewTokens}</span>
                                </label>
                                <input
                                    id="max-tokens"
                                    type="range"
                                    min={64}
                                    max={1024}
                                    step={32}
                                    value={maxNewTokens}
                                    onChange={(e) => setMaxNewTokens(Number(e.target.value))}
                                />
                                <div className="settings-slider-range">
                                    <span>64</span><span>1024</span>
                                </div>
                            </div>
                        </div>
                    </SettingsSection>

                    <div className="settings-form__actions">
                        <button type="submit" className="settings-form__save-btn">
                            {saved ? "✓ Saved" : "Save settings"}
                        </button>
                        <p className="settings-form__note">
                            Note: model changes take effect only after restarting the Flask backend.
                        </p>
                    </div>
                </form>
            </div>
        </Layout>
    );
}
