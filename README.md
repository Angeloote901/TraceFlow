# 🔮 Visual Sandbox for Code & Systems

A learning tool that shows students and teachers **what a program is actually doing**, explained at two levels: a simple version with everyday analogies, and a precise technical version.

Built for Hack@URI. **Powered by Gemma 4** (open-weight), run through the Gemini API.

## Two modes

### 🧠 Concept Explorer
Pick a topic (math program, call stack, PostgreSQL, auth tokens, a tiny neural network) or type your own.
- Live **diagram** of the system or flow
- Matching **code**, with a **line inspector**: pick any line and get a simple and a technical explanation
- **Step inspector**: click any diagram step for both explanations, plus a **deep dive** with worked math (e.g. matrix multiply → ReLU → softmax in the neural network example)

### 🐞 Step-Through Debugger
A Python Tutor-style stepper. Paste Python, run it, and move one line at a time while watching variables and call-stack frames change. Click **Explain this step with Gemma** for an explanation grounded in the real memory state.

## How Gemma is used
- Generates the diagram, code, line-by-line explanations and glossary as structured JSON for any topic.
- Writes deep dives for individual steps, with thinking mode **on** so it works through the math.
- Explains each debugger step using the actual variable/stack state at that moment.
- Thinking mode is **off** for quick diagram generation. Calls fall back from `gemma-4-26b-a4b-it` to `gemma-4-31b-it` on errors.

The debugger's stepping is real code execution (`sys.settrace`); Gemma does the explaining.
Preset topics are pre-generated for instant, reliable demos, and **Regenerate live with Gemma** produces them live.

## Run it
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"     # Windows PowerShell: $env:GEMINI_API_KEY="your-key"
streamlit run app.py
```

## Files
| File | Purpose |
|---|---|
| `app.py` | Streamlit UI (both modes) |
| `ai_engine.py` | Gemma calls, JSON extraction, fallbacks |
| `presets.py` | Prompts and pre-generated preset topics |
| `tracer.py` | Line-by-line Python execution recorder |

## Limitations
- The debugger blocks imports and stops after 300 steps, but it is **not a true sandbox**. Run only code you trust, locally.
- Gemma runs through Google's hosted API rather than being self-hosted.
