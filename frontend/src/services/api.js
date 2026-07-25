import axios from "axios";

const api = axios.create({
    baseURL: "/api",   // resolved through Vite proxy → http://localhost:5000/api
});

export default api;

// ─── Named helpers ────────────────────────────────────────────────────────────

/** POST /api/chat — send a question, receive {answer, sources} */
export const sendChat = (question) =>
    api.post("/chat", { question }).then((r) => r.data);

/** GET /api/dashboard/kpis */
export const getKPIs = () => api.get("/dashboard/kpis").then((r) => r.data);

/** GET /api/dashboard/products */
export const getProducts = () =>
    api.get("/dashboard/products").then((r) => r.data);

/** GET /api/dashboard/issues */
export const getIssues = () => api.get("/dashboard/issues").then((r) => r.data);

/** GET /api/dashboard/companies */
export const getCompanies = () =>
    api.get("/dashboard/companies").then((r) => r.data);

/** GET /api/dashboard/trends */
export const getTrends = () => api.get("/dashboard/trends").then((r) => r.data);

/** POST /api/evaluate — send {question, answer, contexts} */
export const evaluate = (payload) =>
    api.post("/evaluate", payload).then((r) => r.data);
