import { useState, useRef, useEffect } from "react";
import api from "../../services/api";
import Message from "./Message";
import SourceCard from "./SourceCard";
import ChatInput from "./ChatInput";
import { MdExpandMore, MdExpandLess } from "react-icons/md";

const SUGGESTED_QUESTIONS = [
    "What are the most common mortgage complaints?",
    "Which companies have the most credit card complaints?",
    "What issues do customers report about student loans?",
    "Are there patterns in debt collection complaints?",
    "What states have the highest complaint volumes?",
];

export default function ChatWindow() {
    const [messages, setMessages] = useState([
        {
            role: "assistant",
            content:
                "Hello! I'm your AI Financial Complaint Analyst. I can answer questions about consumer complaints using retrieved records from the CFPB dataset.\n\nTry one of the suggested questions below, or ask your own.",
            sources: [],
        },
    ]);
    const [loading, setLoading] = useState(false);
    const [expandedSources, setExpandedSources] = useState({});
    const bottomRef = useRef(null);

    // Auto-scroll to the latest message
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    async function sendMessage(question) {
        // Append the user message immediately
        setMessages((prev) => [
            ...prev,
            { role: "user", content: question, sources: [] },
        ]);
        setLoading(true);

        try {
            const { data } = await api.post("/chat", { question });
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: data.answer || "No answer returned.",
                    sources: data.sources || [],
                },
            ]);
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content:
                        "Sorry, I couldn't reach the backend. Make sure the Flask server is running on port 5000.",
                    sources: [],
                },
            ]);
        } finally {
            setLoading(false);
        }
    }

    function toggleSources(index) {
        setExpandedSources((prev) => ({
            ...prev,
            [index]: !prev[index],
        }));
    }

    return (
        <div className="chat-window">
            {/* ── Suggested questions ── */}
            <div className="chat-suggestions">
                {SUGGESTED_QUESTIONS.map((q) => (
                    <button
                        key={q}
                        className="chat-suggestion-btn"
                        onClick={() => sendMessage(q)}
                        disabled={loading}
                    >
                        {q}
                    </button>
                ))}
            </div>

            {/* ── Message thread ── */}
            <div className="chat-messages">
                {messages.map((msg, i) => (
                    <div key={i} className="chat-turn">
                        <Message role={msg.role} content={msg.content} />

                        {/* Sources accordion — only for assistant messages that have sources */}
                        {msg.role === "assistant" &&
                            msg.sources &&
                            msg.sources.length > 0 && (
                                <div className="chat-sources">
                                    <button
                                        className="chat-sources__toggle"
                                        onClick={() => toggleSources(i)}
                                        aria-expanded={!!expandedSources[i]}
                                    >
                                        {expandedSources[i] ? (
                                            <>
                                                <MdExpandLess size={16} /> Hide{" "}
                                                {msg.sources.length} source
                                                {msg.sources.length !== 1 ? "s" : ""}
                                            </>
                                        ) : (
                                            <>
                                                <MdExpandMore size={16} /> Show{" "}
                                                {msg.sources.length} retrieved record
                                                {msg.sources.length !== 1 ? "s" : ""}
                                            </>
                                        )}
                                    </button>

                                    {expandedSources[i] && (
                                        <div className="chat-sources__list">
                                            {msg.sources.map((src, j) => (
                                                <SourceCard
                                                    key={j}
                                                    source={src}
                                                    index={j}
                                                />
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                    </div>
                ))}

                {/* Loading indicator */}
                {loading && (
                    <div className="chat-turn">
                        <div className="message message--assistant">
                            <div className="message__avatar">
                                <span className="typing-dot" />
                            </div>
                            <div className="message__bubble message__bubble--loading">
                                <span className="typing-dot" />
                                <span className="typing-dot" />
                                <span className="typing-dot" />
                            </div>
                        </div>
                    </div>
                )}

                <div ref={bottomRef} />
            </div>

            {/* ── Input bar ── */}
            <ChatInput onSend={sendMessage} disabled={loading} />
        </div>
    );
}
