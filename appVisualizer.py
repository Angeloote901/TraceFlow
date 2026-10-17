from google import genai
import json

client = genai.Client()

# Example code a student might submit
student_code = """
total = 0
for i in range(1, 4):
    total += i
"""

prompt = f"""
You are an expert computer science tutor. Analyze the following code and break down its execution into a clean list of sequential steps so we can visualize it for a student.

Code to analyze:
{student_code}

Return your response in a clear JSON layout containing a list of execution steps. Each step must track the current values of all variables and include a short, simple explanation of what is happening in that specific step.
"""

print("Analyzing code structure...")

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt,
    # Instruct the model to respond strictly with clean, predictable JSON
    response_format={
        "type": "text",
        "mime_type": "application/json"
    }
)

# Parse and look at the structured breakdown
visualization_data = json.loads(interaction.output_text)
print(json.dumps(visualization_data, indent=2))
