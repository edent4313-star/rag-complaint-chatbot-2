import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import Chatbot from "./pages/Chatbot";
import Evaluation from "./pages/Evaluation";

function App() {
    return (
        <BrowserRouter>
            <Routes>

                <Route path="/" element={<Dashboard />} />

                <Route path="/analytics" element={<Analytics />} />

                <Route path="/chat" element={<Chatbot />} />

                <Route path="/evaluation" element={<Evaluation />} />

            </Routes>
        </BrowserRouter>
    );
}

export default App;