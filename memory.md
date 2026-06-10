# Project Memory & Change Log

## Current State (As of Jun 10, 2026)
- **Backend (Blender & Python Pipeline):** The core 3D conversion pipeline (`blender/convert.py`) now features a completely operational **Two-Stage AI Material Mapping** system. 
  - **Stage 1:** Lightning-fast Text-Only LLM Mapping via Gemini 2.5 Flash using semantic logic.
  - **Stage 2:** A Visual Language Model (VLM) fallback triggered automatically when names are arbitrary. It securely generates synthetic neon emission masks using Eevee in headless mode to completely bypass Blender C++ crashes.
  - **Output:** Outputs `.usd` files perfectly and writes dual copies of the mapped `texture_map.json` to both the original asset folder and the converted library directory.
  - **Stability:** Hardened with auto-retries for Google API server overloads (e.g., 503, 429), dynamic Blender 4.2+ engine detection (`EEVEE_NEXT`), recursive deep-folder texture scraping (`os.walk`), and a dedicated `debug_log.txt` for catching silent Tauri process failures.
- **Frontend (Tauri + React + Vite):** A pristine, hyper-modern interface leveraging Tailwind CSS and Shadcn UI components. Features dedicated screens for Asset Browsing, Queue processing, Logging, and App Configuration.

---

## Change Log

### [Jun 10, 2026] Massive UI Revamp (Merge PR #4)
**Context:** Pulled `frontend_design` from `manisha1124`.
- **Frontend Overhaul:** Completely scrapped the legacy MVP UI (`src/App.tsx`, `src/index.css`) in favor of a vastly expanded, component-driven architecture.
- **Frameworks Integrated:** Added **TailwindCSS** (`styles/tailwind.css`) and over 40+ **Shadcn UI** components (`app/components/ui/*` including sidebars, dialogs, charts, and carousels).
- **Screens Added/Refactored:**
  - `Library.tsx`: Now an advanced 500+ line grid with asset browsing and fallback image handlers (`ImageWithFallback.tsx`).
  - `Settings.tsx`: Beautifully designed configuration hub for the Blender path, Output Library, and Gemini API Keys.
  - `Queue.tsx` & `Logs.tsx`: Robust monitoring views for backend conversion tasks.
- **Global State:** Created a comprehensive React context (`AppContext.tsx`) and global `Layout.tsx` for state sharing.
- **Backend Tweaks:** Minor dependency bumps in `src-tauri/Cargo.toml` and subtle adjustments to `main.rs` to keep the Python execution calls compatible with the new Settings state.

### [Jun 09-10, 2026] The "Headless AI" Pipeline Rewrite
**Context:** Building the generative 3D pipeline on the backend.
- Hand-coded the Two-Stage AI architecture into `convert.py` without breaking the original, perfectly functioning mesh extraction logic.
- Traced and destroyed a hidden `Segmentation Fault` triggered by Blender's Headless Workbench engine. Invented a novel workaround that replaces object materials with flat Eevee Emission shaders to snap VLM screenshots dynamically.
- Intercepted a fatal Python `os` scope bug and a hardcoded folder-search bug that was causing the script to bypass folders misspelled as `texure`.
- Patched in comprehensive crash and debug logging directly to `ASSET LIB APP/src-tauri/` to communicate with the frontend gracefully.
