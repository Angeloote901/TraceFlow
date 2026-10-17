# presets.py
# COMPLETE UNIFIED CONFIGURATION DATA LAYER

AI_PRESET = "How AI Works (Input → Output with Matrices)"
CUSTOM_PRESET = "Custom Blueprints (Type your own!)"

PRESETS = {
    "Simple Math Program (Step-by-Step)": "A basic mathematical calculator workflow.",
    "Function Call Stack (Memory)": "Tracing execution memory stacks.",
    "PostgreSQL Database (Deep-Dive)": "Deep-dive database topology.",
    "Auth Service (How security tokens work)": "JWT token workflow.",
    AI_PRESET: "A tiny neural network taking an input vector and producing probabilities using matrix math.",
    CUSTOM_PRESET: "",
}

SYSTEM_PROMPT_TEMPLATE = """
You are an elite Computer Science educator and Principal Technical Architect. Convert this concept into a precise JSON structure containing a visual diagram, matching code, line-by-line explanations, and student definitions.

Concept to map:
{user_concept}

Respond with ONLY a JSON object with exactly these four keys: "mermaid_code", "matching_code", "line_explanations", "glossary". No markdown fences, no commentary.

CRITICAL FORMATTING & SYNTAX RULES:
1. 'mermaid_code': Use strict, executable Mermaid formatting.
   - ALWAYS enclose your node text descriptions explicitly inside double quotes and brackets like this: NodeID["Descriptive Text"]
   - Keep node text simple (letters, numbers, spaces, = and + only; no parentheses or quotes inside the text).
   - For code structures or stack memory frames, use 'subgraph' blocks heavily to represent bounded container walls.
2. 'matching_code': Create a clean, short Python code snippet (under 15 lines) showing what the raw code looks like for this concept.
3. 'line_explanations': A list with one object for every NON-EMPTY line of matching_code. Each object has three keys: 'line_number' (integer, 1-indexed, counting blank lines), 'beginner' (a simple everyday explanation of what that line does), and 'technical' (a precise explanation).
4. 'glossary': Create a dictionary mapping EVERY distinct node text label used in the diagram, spelled exactly the same, to a sub-dictionary containing three keys:
   - 'beginner': A heavily simplified explanation or everyday analogy.
   - 'technical': A precise, professional definition.
   - 'deep_dive': A step-by-step walkthrough in markdown of how this step works internally. If it involves math, show a tiny worked numeric example and write math using $...$ LaTeX. If it is a program, trace what the computer does.
"""

DEEP_DIVE_PROMPT = """
You are a Computer Science educator. A student is looking at this code and diagram.

Overall concept: {concept}

Code:
{code}

They selected this step: "{step}"

Explain in depth how this step works internally, in markdown. If it involves math, include a tiny worked numeric example and write math using $...$ LaTeX. If it is a program, trace what the computer does step by step. Keep it under 200 words and friendly but precise.
"""

PREBAKED_CACHE = {
    "Simple Math Program (Step-by-Step)": {
        "matching_code": "x = 5\ny = 2.5\ntotal = (x + y) * 2\nprint(total)  # Output: 15.0",
        "line_explanations": [
            {"line_number": 1, "beginner": "Put the number 5 in a box labeled x.", "technical": "Binds the name x to an int object with value 5 in the current namespace."},
            {"line_number": 2, "beginner": "Put the decimal number 2.5 in a box labeled y.", "technical": "Binds y to a float object (64-bit double) with value 2.5."},
            {"line_number": 3, "beginner": "Add the two boxes (7.5), then double it, and store the answer in a box called total.", "technical": "Evaluates (x + y) first due to parentheses, giving 7.5, multiplies by 2 to get 15.0, and binds the result to total."},
            {"line_number": 4, "beginner": "Show the answer on the screen.", "technical": "Calls print(), which writes the string form of total to stdout. The comment after # is ignored by Python."},
        ],
        "mermaid_code": 'graph TD\n    A["Start Script"] --> B["x = 5 (Integer Variable)"]\n    B --> C["y = 2.5 (Float/Decimal)"]\n    C --> D["Addition: x + y = 7.5"]\n    D --> E["Multiplication: 7.5 * 2 = 15.0"]\n    E --> F["Print Result to Console"]',
        "glossary": {
            "x = 5 (Integer Variable)": {
                "beginner": "A labeled box holding a whole number 5.",
                "technical": "An immutable primitive allocation storing an integer data type."
            },
            "y = 2.5 (Float/Decimal)": {
                "beginner": "A box holding a fractional number with decimal points.",
                "technical": "A double-precision floating-point scalar variable."
            },
            "Addition: x + y = 7.5": {
                "beginner": "Combining the values of both boxes together.",
                "technical": "An arithmetic operation executing an addition binary expression yielding a floating-point sum."
            }
        }
    },
    "Function Call Stack (Memory)": {
        "matching_code": "global_val = 100\n\ndef helper():\n    local_x = 5\n    return local_x\n\nhelper()",
        "line_explanations": [
            {"line_number": 1, "beginner": "A public sign that everyone in the program can read.", "technical": "Creates a module-level (global) variable global_val bound to 100."},
            {"line_number": 3, "beginner": "Write down a recipe called helper, but don't cook it yet.", "technical": "Defines a function object and binds it to the name helper. The body does not run until it is called."},
            {"line_number": 4, "beginner": "Inside the recipe, use a private notepad for the number 5.", "technical": "Creates a local variable local_x in the function's own stack frame; it disappears when the call ends."},
            {"line_number": 5, "beginner": "Hand the 5 back to whoever asked and close the workspace.", "technical": "Returns the value of local_x to the caller and pops helper's frame off the call stack."},
            {"line_number": 7, "beginner": "Actually cook the recipe now.", "technical": "Calls helper(): pushes a new stack frame, executes the body, then pops it. The return value is discarded here."},
        ],
        "mermaid_code": 'graph TD\n    subgraph Global_Scope["🌍 Global Variable Area"]\n        G["global_val = 100"]\n    end\n    subgraph Memory_Stack["🥞 Function Call Stack Memory Container"]\n        direction BT\n        M["Main Script Frame"] --> H["helper() Frame"]\n    end\n    H -->|Returns Value| M',
        "glossary": {
            "global_val = 100": {
                "beginner": "A sign board sitting out in the public square that any citizen can see and read.",
                "technical": "A variable bound to the module-level global namespace dictionary object scope."
            },
            "helper() Frame": {
                "beginner": "A private, temporary workspace that opens up when a helper runs, and gets completely thrown away when it is finished.",
                "technical": "An isolated execution context stack frame allocating temporary space for local environment scopes."
            }
        }
    },
    "PostgreSQL Database (Deep-Dive)": {
        "matching_code": "SELECT * FROM users WHERE id = 42;",
        "line_explanations": [
            {"line_number": 1, "beginner": "Ask the database: 'show me everything about the user whose ID is 42.'", "technical": "A SELECT query: * returns all columns, FROM names the table, and WHERE filters rows to those matching id = 42 (fast if id is indexed)."},
        ],
        "mermaid_code": 'graph LR\n    A["Client Query"] --> B["Connection Pooler"]\n    B --> C["SQL Parser"]\n    C --> D["Shared Buffer Cache"]\n    D --> E["Write-Ahead Log (WAL)"]',
        "glossary": {
            "Connection Pooler": {
                "beginner": "A waiting line coordinator outside a busy restaurant managing incoming guests.",
                "technical": "A proxy server maintaining a cache of reusable database connections to lower overhead."
            },
            "SQL Parser": {
                "beginner": "A language translator checking if your order slip is spelled correctly.",
                "technical": "A compilation compiler engine validating syntax and building a logical execution syntax tree."
            },
            "Shared Buffer Cache": {
                "beginner": "A quick-access shelf holding frequently ordered food boxes so you don't have to walk back to the deep kitchen freezer.",
                "technical": "A dedicated shared memory pool caching shared disk blocks to eliminate expensive physical storage disk operations."
            }
        }
    },
    "Auth Service (How security tokens work)": {
        "matching_code": "user_token = jwt.encode({'user_id': 123}, 'secret_key', algorithm='HS256')",
        "line_explanations": [
            {"line_number": 1, "beginner": "Make a stamped VIP wristband that says 'this is user 123'.", "technical": "Encodes the payload {'user_id': 123} as a JWT, signing it with HMAC-SHA256 using 'secret_key'. Anyone with the secret can verify it wasn't tampered with."},
        ],
        "mermaid_code": 'graph TD\n    A["Client Password"] --> B["Auth Handler"]\n    B --> C["Hashing Engine (Bcrypt)"]\n    C --> D["Database Check"]\n    D --> E["Token Generator (JWT)"]',
        "glossary": {
            "Hashing Engine (Bcrypt)": {
                "beginner": "A digital paper shredder that scrambles passwords into unique patterns so nobody can read them if stolen.",
                "technical": "A cryptographically secure key-derivation function adapting work factors to slow down brute force cracking attempts."
            },
            "Token Generator (JWT)": {
                "beginner": "A stamped VIP wristband given to you after security checks, letting you pass through doors without re-entering passwords.",
                "technical": "An authentication token standard formatting signed, URL-safe data claims using asymmetric or symmetric signatures."
            }
        }
    },
    AI_PRESET: {
        "matching_code": (
            "import numpy as np\n"
            "\n"
            "x = np.array([1.0, 2.0])\n"
            "W1 = np.array([[0.5, -1.0], [1.0, 0.5]])\n"
            "b1 = np.array([0.0, -0.5])\n"
            "W2 = np.array([[1.0, -1.0], [0.5, 1.0]])\n"
            "\n"
            "h = x @ W1 + b1          # [2.5, -0.5]\n"
            "h = np.maximum(0, h)     # [2.5, 0.0]\n"
            "logits = h @ W2          # [2.5, -2.5]\n"
            "probs = np.exp(logits) / np.exp(logits).sum()\n"
            "print(probs)             # [0.993 0.007]"
        ),
        "line_explanations": [
            {"line_number": 1, "beginner": "Borrow a toolbox that is great at handling grids of numbers.", "technical": "Imports NumPy, which provides n-dimensional arrays and fast vectorized linear algebra."},
            {"line_number": 3, "beginner": "This is the question we ask the AI, written as a list of two numbers.", "technical": "The input vector x, shape (2,). Real inputs would be pixels, word embeddings, etc."},
            {"line_number": 4, "beginner": "The AI's first set of 'dials'. Each dial says how much to care about each input.", "technical": "Weight matrix W1, shape (2, 2). Learned during training; here hand-picked for the demo."},
            {"line_number": 5, "beginner": "A small nudge added to each result, like a head start.", "technical": "Bias vector b1, shape (2,), added after the matrix multiply so neurons can shift their activation threshold."},
            {"line_number": 6, "beginner": "The second set of dials, turning the middle values into final scores.", "technical": "Weight matrix W2, shape (2, 2), mapping hidden activations to two output logits."},
            {"line_number": 8, "beginner": "Mix the inputs using the dials, then add the nudge.", "technical": "Layer 1 forward pass: h = xW1 + b1, a matrix-vector product plus bias, giving [2.5, -0.5]."},
            {"line_number": 9, "beginner": "Anything negative becomes zero. The AI only 'fires' on positive signals.", "technical": "ReLU activation, max(0, z) elementwise. It adds non-linearity; without it, stacked layers collapse into one linear map."},
            {"line_number": 10, "beginner": "Mix again with the second dials to get raw scores for each answer.", "technical": "Layer 2 forward pass: logits = hW2, the unnormalized scores for each class."},
            {"line_number": 11, "beginner": "Turn raw scores into percentages that add up to 100%.", "technical": "Softmax: exponentiate each logit and divide by the sum, producing a probability distribution."},
            {"line_number": 12, "beginner": "Show the AI's answer.", "technical": "Prints the probability vector: about 99.3% for class 0 and 0.7% for class 1."},
        ],
        "mermaid_code": 'graph LR\n    A["Input Vector x"] --> B["Layer 1 Weights W1 + Bias b1"]\n    B --> C["ReLU Activation"]\n    C --> D["Layer 2 Weights W2"]\n    D --> E["Softmax"]\n    E --> F["Output Probabilities"]',
        "glossary": {
            "Input Vector x": {
                "beginner": "The question you hand to the AI, turned into a list of numbers.",
                "technical": "A feature vector representing the input. Neural networks operate only on numeric tensors.",
                "deep_dive": r"""Models can't read pictures or words directly, only numbers. So everything is encoded first.

Here the input is just two numbers:

$$x = [1,\ 2]$$

For an image this might be thousands of pixel values; for text, a list of numbers (an *embedding*) per word. Same idea, bigger vector."""
            },
            "Layer 1 Weights W1 + Bias b1": {
                "beginner": "Dials that decide how much each input matters, plus a small nudge.",
                "technical": "An affine transformation: h = xW1 + b1, a vector-matrix product plus a bias.",
                "deep_dive": r"""Each output is a **weighted sum** of the inputs plus a bias:

$$h = xW_1 + b_1,\quad W_1=\begin{bmatrix}0.5 & -1\\ 1 & 0.5\end{bmatrix},\ b_1=[0,\,-0.5]$$

Column by column:

- $h_1 = 1(0.5) + 2(1) + 0 = 2.5$
- $h_2 = 1(-1) + 2(0.5) - 0.5 = -0.5$

So $h = [2.5,\ -0.5]$. Training is the process of nudging every number in $W_1$ and $b_1$ until the outputs get useful."""
            },
            "ReLU Activation": {
                "beginner": "A gate that lets positive signals through and blocks negative ones.",
                "technical": "Rectified Linear Unit: an elementwise non-linearity, max(0, z).",
                "deep_dive": r"""$$\text{ReLU}(z) = \max(0, z)$$

Applied to each number separately:

- $\max(0, 2.5) = 2.5$
- $\max(0, -0.5) = 0$

Result: $[2.5,\ 0]$.

**Why bother?** Without a non-linear step, two matrix multiplies in a row are mathematically the same as one bigger matrix multiply, so extra layers would add nothing. ReLU is what lets deep networks learn curvy, complex patterns."""
            },
            "Layer 2 Weights W2": {
                "beginner": "A second set of dials that turns the middle values into final scores.",
                "technical": "A second linear layer mapping hidden activations to output logits.",
                "deep_dive": r"""Same operation as before, new weights:

$$\text{logits} = hW_2,\quad W_2=\begin{bmatrix}1 & -1\\ 0.5 & 1\end{bmatrix}$$

- $z_1 = 2.5(1) + 0(0.5) = 2.5$
- $z_2 = 2.5(-1) + 0(1) = -2.5$

Logits: $[2.5,\ -2.5]$. They're raw scores, not probabilities yet. They can be any size, even negative."""
            },
            "Softmax": {
                "beginner": "Turns raw scores into percentages that add up to 100%.",
                "technical": "Normalizes logits into a probability distribution via exponentiation and division by the sum.",
                "deep_dive": r"""$$p_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

- $e^{2.5} \approx 12.18$
- $e^{-2.5} \approx 0.082$
- Sum $\approx 12.26$

So:

- $p_1 = 12.18 / 12.26 \approx 0.993$
- $p_2 = 0.082 / 12.26 \approx 0.007$

Exponentiating makes everything positive and exaggerates differences, and dividing by the sum makes them total 1."""
            },
            "Output Probabilities": {
                "beginner": "The AI's final answer: how confident it is in each choice.",
                "technical": "A categorical probability distribution over output classes.",
                "deep_dive": r"""The network says: **class 0 with ~99.3% confidence**, class 1 with ~0.7%.

During training, we compare this to the correct answer using a *loss* (e.g. cross-entropy), then use calculus (backpropagation) to figure out how to adjust $W_1, b_1, W_2$ so next time the answer is closer. Repeat millions of times, and that's learning."""
            },
        }
    },
}