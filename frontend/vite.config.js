import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000,
        proxy: {
            "/api": {
                target: "http://localhost:5000",
                changeOrigin: true,
            },
        },
    },
    test: {
        globals: true,
        environment: "jsdom",
        setupFiles: "./src/test/setup.js",
        css: false,               // skip CSS parsing — not needed in unit tests
        coverage: {
            provider: "v8",
            reporter: ["text", "lcov"],
            include: ["src/components/**", "src/pages/**", "src/services/**"],
            exclude: ["src/test/**"],
        },
    },
});
