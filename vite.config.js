import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
    root: "./web",
    build: {
        emptyOutDir: true,
        outDir: "../tmp/web",
    },
    plugins: [tailwindcss()],
});
