import Layout from "../components/Layout/Layout";
import ChatWindow from "../components/Chat/ChatWindow";

export default function Chatbot() {
    return (
        <Layout>
            <div className="page-shell">
                <div className="page-header">
                    <div>
                        <p className="eyebrow">AI copilot</p>
                        <h1>Prompt-engineered complaint assistant</h1>
                        <p>Ask questions about complaints, products, companies, and emerging trends.</p>
                    </div>
                </div>

                <ChatWindow />
            </div>
        </Layout>
    );
}