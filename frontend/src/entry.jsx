import React from "react";
import { createRoot } from "react-dom/client";
import App from "../app";

const root = document.getElementById("root");
if (!root) {
  throw new Error("Root element not found. Ensure index.html includes <div id=\"root\"></div>");
}

createRoot(root).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
