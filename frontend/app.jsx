import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./src/pages/Dashboard";
import Analytics from "./src/pages/Analytics";
import Chatbot from "./src/pages/Chatbot";
import Evaluation from "./src/pages/Evaluation";
import Settings from "./src/pages/Settings";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/chat" element={<Chatbot />} />
                <Route path="/evaluation" element={<Evaluation />} />
                <Route path="/settings" element={<Settings />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
