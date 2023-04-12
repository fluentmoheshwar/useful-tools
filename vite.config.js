import { defineConfig } from "vite";

export default defineConfig({
    root: "./web",
    build: {
        emptyOutDir: true,
        outDir: "../tmp/web",
    },
});
