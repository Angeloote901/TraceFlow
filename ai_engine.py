# ai_engine.py

import json
import time

from google import genai
from google.genai import types

from presets import SYSTEM_PROMPT_TEMPLATE, DEEP_DIVE_PROMPT

STEP_PROMPT = """
A student is stepping through a Python program in a debugger.

Program:
{code}

The NEXT line to execute is line {line_no}: {line_text}

Memory state BEFORE that line runs (JSON, list of stack frames, global first):
{state}

Explain this step in markdown with exactly two parts and at most 90 words total:
**🌱 Simple:** one or two sentences using an everyday analogy.
**⚙️ Technical:** two or three sentences describing precisely what happens and what changes in memory.
"""

# Gemma 4 is open-weight and is hosted on the Gemini API (same key, same SDK).
# Per the Gemma docs, the supported ids are "gemma-4-26b-a4b-it" and "gemma-4-31b-it".
MODEL_NAME = "gemma-4-26b-a4b-it"
FALLBACK_MODEL = "gemma-4-31b-it"  # also Gemma, used if the first one errors
TIMEOUT_MS = 60000  # Gemma can be slower than Flash


def _error_result(message: str) -> dict:
    """Shape an error so the UI can still render it."""
    return {
        "mermaid_code": 'graph TD\n    E["API error"]',
        "matching_code": f"# {message}",
        "line_explanations": [],
        "glossary": {"API error": {"beginner": message, "technical": message}},
    }


def _extract_json(text: str) -> dict:
    """Gemma doesn't support JSON mode, so pull the JSON object out of the raw text."""
    text = text.strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model output.")
    return json.loads(text[start : end + 1])


class ArchitectureAIEngine:
    def __init__(self):
        # Reads GEMINI_API_KEY / GOOGLE_API_KEY from the environment
        self.client = genai.Client()

    def _generate(self, prompt: str, thinking: str = "minimal") -> str:
        """Try Gemma with thinking config, then without it, then the bigger Gemma.
        A 500 INTERNAL from the API is usually server-side/transient or caused by one setting."""
        attempts = [
            (MODEL_NAME, thinking),
            (MODEL_NAME, None),
            (FALLBACK_MODEL, None),
        ]
        last_err = None
        for model, think in attempts:
            try:
                cfg = {"http_options": types.HttpOptions(timeout=TIMEOUT_MS)}
                if think:
                    cfg["thinking_config"] = types.ThinkingConfig(thinking_level=think)
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(**cfg),
                )
                if response.text:
                    return response.text
            except Exception as e:
                last_err = e
                time.sleep(1)
        raise last_err or RuntimeError("Empty response from Gemma.")

    def generate_visual_map(self, concept_description: str) -> dict:
        """Return a dict with mermaid_code, matching_code, line_explanations, glossary."""
        prompt = SYSTEM_PROMPT_TEMPLATE.format(user_concept=concept_description)

        last_err = None
        for _ in range(2):  # one retry if the JSON comes back malformed
            try:
                data = _extract_json(self._generate(prompt))
                if isinstance(data, dict):
                    return data
                last_err = ValueError("Model returned JSON that wasn't an object.")
            except Exception as e:
                last_err = e
        return _error_result(f"{type(last_err).__name__}: {last_err}")

    def explain_step(self, concept: str, code: str, step: str) -> str:
        """Return a markdown deep-dive for one diagram step."""
        prompt = DEEP_DIVE_PROMPT.format(concept=concept, code=code, step=step)
        try:
            return self._generate(prompt, thinking="high")  # let Gemma reason through the math
        except Exception as e:
            return f"Couldn't generate a deep dive: {type(e).__name__}: {e}"

    def explain_execution_step(self, code: str, line_no: int, line_text: str, frames: list) -> str:
        """Explain what the next line of a traced program does, given the current memory state."""
        prompt = STEP_PROMPT.format(
            code=code, line_no=line_no, line_text=line_text,
            state=json.dumps(frames, indent=1),
        )
        try:
            return self._generate(prompt)
        except Exception as e:
            return f"Couldn't explain this step: {type(e).__name__}: {e}"