import os
from flask import Flask, render_template_string, request
from google import genai

# Initialize Flask app (Functional style, no classes)
app = Flask(__name__)

# Initialize the Gemini client using the modern google-genai SDK
# It automatically picks up the GEMINI_API_KEY environment variable


client = genai.Client(api_key="AQ.Ab8RN6ImOSH5pEmp_QCo80UIG-0RUYLonDpLeIz_CNPNFK5l6g")

# Inline HTML and CSS template for the user interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Study Planner - Class 12 Project</title>
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        h1 {
            text-align: center;
            color: var(--primary);
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            color: #64748b;
            font-size: 0.95rem;
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
        input[type="text"], textarea {
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
            transition: background 0.2s;
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
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Study Planner</h1>
        <div class="subtitle">Class 12 Computer Science Project</div>
        
        <form method="POST">
            <div class="form-group">
                <label for="subjects">Subjects / Topics to Cover:</label>
                <input type="text" id="subjects" name="subjects" placeholder="e.g., Python SQL connectivity, Data Structures, Physics Ch 1" required value="{{ subjects if subjects else '' }}">
            </div>
            
            <div class="form-group">
                <label for="days">Available Days Until Exam:</label>
                <input type="text" id="days" name="days" placeholder="e.g., 7 days" required value="{{ days if days else '' }}">
            </div>
            
            <div class="form-group">
                <label for="goals">Special Goals or Weaknesses:</label>
                <textarea id="goals" name="goals" placeholder="e.g., I need extra time for revision and practical coding examples.">{{ goals if goals else '' }}</textarea>
            </div>
            
            <button type="submit">Generate Study Plan</button>
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
        # Extract form inputs safely
        subjects_val = request.form.get("subjects")
        days_val = request.form.get("days")
        goals_val = request.form.get("goals")

        # Construct a prompt for the Gemini model
        prompt = (
            f"Create a structured, day-by-day study plan based on the following details:\n"
            f"- Subjects/Topics: {subjects_val}\n"
            f"- Timeline: {days_val}\n"
            f"- Specific Goals/Weaknesses: {goals_val}\n"
            f"Keep it encouraging, clear, well-formatted, and practical for a Class 12 student."
        )

        try:
            # Call the Gemini API using the standard gemini-2.5-flash model
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            study_plan = response.text
        except Exception as e:
            study_plan = f"An error occurred while generating the plan: {str(e)}"

    return render_template_string(
        HTML_TEMPLATE, 
        plan=study_plan, 
        subjects=subjects_val, 
        days=days_val, 
        goals=goals_val
    )

if __name__ == "__main__":
    # Run the Flask app locally on port 5000
    app.run(debug=True, port=5000)
