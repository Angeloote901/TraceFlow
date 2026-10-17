# app.py

import html

import streamlit as st
import streamlit.components.v1 as components

from ai_engine import ArchitectureAIEngine, MODEL_NAME
from presets import PRESETS, PREBAKED_CACHE, CUSTOM_PRESET
from tracer import run_trace

st.set_page_config(layout="wide", page_title="Code & Architecture Visualizer")


@st.cache_resource
def get_engine() -> ArchitectureAIEngine:
    return ArchitectureAIEngine()


def render_mermaid(code: str, height: int = 550):
    """Streamlit has no built-in Mermaid support, so render it via an HTML component."""
    safe = html.escape(code, quote=False)
    components.html(
        f"""
        <pre class="mermaid">{safe}</pre>
        <script type="module">
          import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
          mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
        """,
        height=height,
        scrolling=True,
    )


def show_explanation(item):
    """Show a beginner/technical pair (dict) or a plain string."""
    if isinstance(item, dict):
        st.info(f"**🌱 Simple Explanation:** {item.get('beginner', 'No simple definition provided.')}")
        st.success(f"**⚙️ Technical Definition:** {item.get('technical', 'No technical definition provided.')}")
    else:
        st.info(f"**Explanation:** {item}")


SAMPLE_CODE = """def add(a, b):
    total = a + b
    return total

x = 5
y = 5
result = add(x, y)
print(result)"""


def _go(delta: int, last: int):
    st.session_state["step_idx"] = max(0, min(last, st.session_state.get("step_idx", 0) + delta))


def render_stepper():
    st.title("🐞 Step-Through Code Visualizer")
    st.caption(f"Run Python one line at a time, watch memory change, then ask Gemma (`{MODEL_NAME}`) to explain any step.")

    code = st.text_area("Python code (no imports, max 300 steps):", value=SAMPLE_CODE, height=220)
    if st.button("▶️ Run & trace", type="primary") or "trace" not in st.session_state:
        st.session_state["trace"] = {"code": code, **run_trace(code)}
        st.session_state["step_idx"] = 0

    trace = st.session_state["trace"]
    steps = trace["steps"]
    if trace["error"]:
        st.error(trace["error"])
    if not steps:
        return

    n = len(steps)
    last = n - 1
    nav1, nav2, nav3 = st.columns([1, 1, 6])
    nav1.button("◀ Prev", on_click=_go, args=(-1, last))
    nav2.button("Next ▶", on_click=_go, args=(1, last))
    if n > 1:
        nav3.slider("Step", 0, last, key="step_idx")
    idx = min(st.session_state.get("step_idx", 0), last)
    step = steps[idx]
    prev_frames = steps[idx - 1]["frames"] if idx > 0 else []

    lines = trace["code"].split("\n")
    left, right = st.columns([1, 1])

    with left:
        st.write(f"**Step {idx + 1} of {n}**" + ("  ✅ done running" if step["line"] is None else "  ➡ next line to execute"))
        st.code(
            "\n".join(f"{'➡' if i == step['line'] else ' '} {i:>2} | {text}" for i, text in enumerate(lines, 1)),
            language=None,
        )
        if step["line"] is not None:
            line_text = lines[step["line"] - 1].strip()
            ekey = f"explain_{hash(trace['code'])}_{idx}"
            if st.button("🤖 Explain this step with Gemma", key=f"btn_{ekey}"):
                with st.spinner("Gemma is explaining..."):
                    st.session_state[ekey] = get_engine().explain_execution_step(
                        trace["code"], step["line"], line_text, step["frames"]
                    )
            if ekey in st.session_state:
                st.markdown(st.session_state[ekey])

    with right:
        st.write("**Print output**")
        st.code(step["stdout"] or " ", language=None)
        st.write("**Frames** (✨ = new or changed)")
        for i, frame in enumerate(step["frames"]):
            before = prev_frames[i]["vars"] if i < len(prev_frames) and prev_frames[i]["name"] == frame["name"] else {}
            st.markdown(f"**{frame['name']}**")
            if frame["vars"]:
                names = [("✨ " if before.get(k) != v else "") + k for k, v in frame["vars"].items()]
                st.table({"variable": names, "value": list(frame["vars"].values())})
            else:
                st.caption("(empty)")


mode = st.sidebar.radio("Mode", ["🧠 Concept Explorer", "🐞 Step-Through Debugger"])
if mode.startswith("🐞"):
    render_stepper()
    st.stop()

st.title("🔮 Visual Sandbox for Code & Systems")
st.caption(f"Compare source code snippets side-by-side with live architectural topology drawings. Powered by open-weight Gemma (`{MODEL_NAME}`).")

with st.sidebar:
    st.header("🎯 Concept Explorer")
    selected_preset = st.selectbox(
        "Choose a topic or concept to inspect:", options=list(PRESETS.keys())
    )
    st.info("💡 Preset topics load instantly. Custom blueprints and extra deep dives use the Gemini API.")

data_key = f"data_{selected_preset}"

col1, col2 = st.columns([1, 1.4])

with col1:
    st.subheader("📝 Specifications & Code Syntax")

    if selected_preset == CUSTOM_PRESET:
        text_value = st.text_area(
            "Describe any tech setup, code pattern, or database process:",
            value="",
            height=150,
        )
    else:
        text_value = st.text_area(
            "Selected Blueprint Description:",
            value=PRESETS[selected_preset],
            height=120,
            disabled=True,
        )

    is_preset = selected_preset in PREBAKED_CACHE
    generate_blueprint = st.button(
        "🤖 Regenerate live with Gemma" if is_preset else "🚀 Render Visual Workspace",
        type="primary",
    )

    # Presets start from the prebaked cache (instant, no API call)
    if is_preset and data_key not in st.session_state:
        st.session_state[data_key] = PREBAKED_CACHE[selected_preset]

    # Button click -> Gemma generates it live (for presets and custom text)
    if generate_blueprint:
        target = PRESETS[selected_preset] if is_preset else text_value
        if not target.strip():
            st.warning("Type a description first.")
        else:
            with st.spinner("Gemma is generating the diagram and code..."):
                result = get_engine().generate_visual_map(target)
            if "API error" in result.get("glossary", {}):
                st.error(result.get("matching_code", "Gemma request failed."))
            else:
                st.session_state[data_key] = result
                st.session_state[f"concept_{selected_preset}"] = target

    app_data = st.session_state.get(data_key)

    if app_data:
        code = app_data.get("matching_code", "# No code required for this configuration.")
        st.write("### 💻 Corresponding Code View")
        st.code(code, language="python")

        # ---- Line-by-line inspector ----
        st.write("### 🔎 Line Inspector")
        code_lines = code.split("\n")
        numbered = [i + 1 for i, line in enumerate(code_lines) if line.strip()]

        explanations = {}
        for entry in app_data.get("line_explanations", []) or []:
            try:
                explanations[int(entry["line_number"])] = entry
            except (KeyError, TypeError, ValueError):
                continue

        if numbered:
            chosen_line = st.selectbox(
                "Pick a line of code to understand:",
                options=numbered,
                format_func=lambda n: f"{n}:  {code_lines[n - 1].strip()}",
                key=f"line_{selected_preset}_{hash(code)}",
            )
            if chosen_line in explanations:
                show_explanation(explanations[chosen_line])
            else:
                st.caption("No explanation available for this line.")

with col2:
    st.subheader("🎨 Live Structural Architecture")

    if app_data:
        mermaid_code = (
            app_data.get("mermaid_code", "")
            .replace("```mermaid", "")
            .replace("```", "")
            .strip()
        )
        glossary = app_data.get("glossary", {})

        render_mermaid(mermaid_code)

        st.write("### 🔍 Step Inspector")
        node_keys = list(glossary.keys())
        if node_keys:
            selected_node = st.radio(
                "Pick a step or component to focus on:",
                options=node_keys,
                horizontal=True,
                key=f"radio_{selected_preset}_{hash(tuple(node_keys))}",
            )
            st.markdown(f"#### 💡 Component Focus: **{selected_node}**")
            node_data = glossary[selected_node]
            show_explanation(node_data)

            # ---- Deep dive (prebaked if available, otherwise generated on demand) ----
            deep = node_data.get("deep_dive") if isinstance(node_data, dict) else None
            deep_key = f"deep_{selected_preset}_{selected_node}"
            deep = deep or st.session_state.get(deep_key)

            if deep:
                with st.expander("🔬 Deep dive: how it actually works", expanded=True):
                    st.markdown(deep)
            else:
                if st.button("🔬 Explain this step in depth", key=f"btn_{deep_key}"):
                    concept = st.session_state.get(f"concept_{selected_preset}") or PRESETS[selected_preset]
                    with st.spinner("Digging deeper..."):
                        st.session_state[deep_key] = get_engine().explain_step(
                            concept, app_data.get("matching_code", ""), selected_node
                        )
                    st.rerun()
    else:
        st.write("Enter a description and click **Render Visual Workspace**.")