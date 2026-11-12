import os

from flask import Flask, render_template_string, request
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
client = Groq(
    api_key="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"
)

MODEL = "openai/gpt-oss-120b"


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>AI Study Planner</title>

    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-color: #1e293b;
            --border-color: #cbd5e1;
        }

        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }

        .container {
            width: 100%;
            max-width: 700px;
            background: var(--card-bg);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

        h1 {
            text-align: center;
            color: var(--primary);
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 25px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
        }

        input, textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 1rem;
            box-sizing: border-box;
        }

        textarea {
            resize: vertical;
            height: 100px;
        }

        button {
            width: 100%;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        .result-box {
            margin-top: 30px;
            padding: 20px;
            background: #f1f5f9;
            border-left: 5px solid var(--primary);
            border-radius: 4px;
            white-space: pre-wrap;
            line-height: 1.6;
            overflow-wrap: anywhere;
        }

        .error {
            border-left-color: #dc2626;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>AI Study Planner</h1>

    <div class="subtitle">
        Class 12 Computer Science Project
    </div>

    <form method="POST">

        <div class="form-group">
            <label for="subjects">
                Subjects / Topics to Cover:
            </label>

            <input
                type="text"
                id="subjects"
                name="subjects"
                placeholder="e.g., Python SQL connectivity, Data Structures"
                required
                value="{{ subjects }}"
            >
        </div>

        <div class="form-group">
            <label for="days">
                Available Days Until Exam:
            </label>

            <input
                type="number"
                id="days"
                name="days"
                min="1"
                max="365"
                placeholder="e.g., 7"
                required
                value="{{ days }}"
            >
        </div>

        <div class="form-group">
            <label for="goals">
                Special Goals or Weaknesses:
            </label>

            <textarea
                id="goals"
                name="goals"
                placeholder="e.g., I need extra time for revision."
            >{{ goals }}</textarea>
        </div>

        <button type="submit">
            Generate Study Plan
        </button>

    </form>

    {% if plan %}
        <div class="result-box">
            <h3>Your Customized Schedule:</h3>
            <div>{{ plan }}</div>
        </div>
    {% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():

    study_plan = ""
    subjects_val = ""
    days_val = ""
    goals_val = ""

    if request.method == "POST":

        subjects_val = request.form.get("subjects", "").strip()
        days_val = request.form.get("days", "").strip()
        goals_val = request.form.get("goals", "").strip()

        if not subjects_val or not days_val:
            study_plan = "Please fill in all required fields."

        elif not os.environ.get("GROQ_API_KEY"):
            study_plan = "API configuration error. Please contact the administrator."

        else:

            prompt = f"""
You are an expert academic study planner.

Create a realistic, structured, day-by-day study schedule
for a Class 12 student.

STUDENT DETAILS:

Subjects and Topics:
{subjects_val}

Available Days:
{days_val}

Special Goals and Weaknesses:
{goals_val if goals_val else "No specific weaknesses mentioned."}

INSTRUCTIONS:

1. Divide the syllabus across the available days.
2. Prioritize difficult topics.
3. Include regular revision.
4. Include practice questions and mock tests.
5. Avoid unrealistic study schedules.
6. Include short breaks.
7. Make the schedule practical and achievable.
8. Use clear headings and bullet points.
9. End with a few useful study tips.

Generate the complete study plan.
"""

            try:

                response = client.chat.completions.create(
                    model=MODEL,

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an experienced academic "
                                "study planner who creates realistic "
                                "and personalized study schedules."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.7,
                    max_completion_tokens=3000
                )

                study_plan = (
                    response.choices[0].message.content
                    or "The AI returned an empty response."
                )

            except Exception:
                app.logger.exception("Groq API request failed")

                study_plan = (
                    "Unable to generate your study plan right now. "
                    "Please try again later."
                )

    return render_template_string(
        HTML_TEMPLATE,
        plan=study_plan,
        subjects=subjects_val,
        days=days_val,
        goals=goals_val
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
