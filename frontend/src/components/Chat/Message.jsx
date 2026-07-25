import { MdPerson, MdSmartToy } from "react-icons/md";

/**
 * Renders a single chat bubble.
 * role: "user" | "assistant"
 */
export default function Message({ role, content }) {
    const isUser = role === "user";

    return (
        <div className={`message ${isUser ? "message--user" : "message--assistant"}`}>
            <div className="message__avatar">
                {isUser ? <MdPerson size={20} /> : <MdSmartToy size={20} />}
            </div>
            <div className="message__bubble">
                {content.split("\n").map((line, i) => (
                    <p key={i} className="message__line">
                        {line}
                    </p>
                ))}
            </div>
        </div>
    );
}
