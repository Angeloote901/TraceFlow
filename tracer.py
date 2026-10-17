# tracer.py
# Python-Tutor-style step recorder: runs code and snapshots memory before every line.
# NOTE: restricted builtins make this safer, but it is NOT a real sandbox.
# Only run code you trust (fine for a local hackathon demo).

import builtins
import contextlib
import io
import sys
import types

FILENAME = "<user_code>"
MAX_STEPS = 300

_ALLOWED = [
    "abs", "all", "any", "bool", "chr", "dict", "divmod", "enumerate", "filter",
    "float", "hash", "int", "isinstance", "len", "list", "map", "max", "min",
    "next", "object", "ord", "pow", "print", "range", "repr", "reversed",
    "round", "set", "sorted", "str", "sum", "super", "tuple", "type", "zip",
    "Exception", "ValueError", "TypeError", "ZeroDivisionError", "IndexError",
    "KeyError", "StopIteration", "__build_class__",
]
SAFE_BUILTINS = {name: getattr(builtins, name) for name in _ALLOWED}


def _fmt(value) -> str:
    if isinstance(value, types.FunctionType):
        return f"function {value.__name__}"
    try:
        text = repr(value)
    except Exception:
        text = "<unprintable>"
    return text if len(text) <= 60 else text[:57] + "..."


def _frames(frame) -> list:
    """Snapshot the user-code call stack, bottom (global) first."""
    stack = []
    f = frame
    while f is not None:
        if f.f_code.co_filename == FILENAME:
            is_global = f.f_code.co_name == "<module>"
            stack.append({
                "name": "Global frame" if is_global else f"{f.f_code.co_name}()",
                "vars": {k: _fmt(v) for k, v in f.f_locals.items() if not k.startswith("__")},
            })
        f = f.f_back
    return list(reversed(stack))


def run_trace(code: str) -> dict:
    """Return {"steps": [...], "error": str | None}.

    Each step: {"line": next line to execute (None = finished), "frames": [...], "stdout": str}
    """
    try:
        compiled = compile(code, FILENAME, "exec")
    except SyntaxError as e:
        return {"steps": [], "error": f"SyntaxError: {e.msg} (line {e.lineno})"}

    steps, out, error = [], io.StringIO(), None
    env = {"__builtins__": SAFE_BUILTINS, "__name__": "__main__"}

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != FILENAME:
            return None
        if event == "line":
            if len(steps) >= MAX_STEPS:
                raise RuntimeError(f"Stopped after {MAX_STEPS} steps (possible infinite loop).")
            steps.append({"line": frame.f_lineno, "frames": _frames(frame), "stdout": out.getvalue()})
        elif event == "return" and frame.f_code.co_name == "<module>":
            steps.append({"line": None, "frames": _frames(frame), "stdout": out.getvalue()})
        return tracer

    sys.settrace(tracer)
    try:
        with contextlib.redirect_stdout(out):
            exec(compiled, env)
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
    finally:
        sys.settrace(None)

    if steps and steps[-1]["line"] is not None:  # crashed or was cut off: add a final frame
        steps.append({"line": None, "frames": steps[-1]["frames"], "stdout": out.getvalue()})
    return {"steps": steps, "error": error}