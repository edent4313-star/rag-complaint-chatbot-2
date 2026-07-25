import { useState } from "react";
import { MdSend } from "react-icons/md";

/**
 * Controlled text input for the chat.
 * Props:
 *   onSend(question: string) — called when user submits
 *   disabled: bool — true while the assistant is loading
 */
export default function ChatInput({ onSend, disabled }) {
    const [value, setValue] = useState("");

    function handleSubmit(e) {
        e.preventDefault();
        const trimmed = value.trim();
        if (!trimmed || disabled) return;
        onSend(trimmed);
        setValue("");
    }

    function handleKeyDown(e) {
        // Submit on Enter, allow Shift+Enter for newline
        if (e.key === "Enter" && !e.shiftKey) {
            handleSubmit(e);
        }
    }

    return (
        <form className="chat-input" onSubmit={handleSubmit}>
            <textarea
                className="chat-input__textarea"
                placeholder="Ask about complaints, products, companies, or trends…"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={2}
                disabled={disabled}
                aria-label="Chat message input"
            />
            <button
                type="submit"
                className="chat-input__btn"
                disabled={disabled || !value.trim()}
                aria-label="Send message"
            >
                <MdSend size={20} />
            </button>
        </form>
    );
}
