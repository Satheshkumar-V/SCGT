from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = "sk-..."  # Replace with real key

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

@app.route("/map-relevance", methods=["POST"])
def map_relevance():
    data = request.json
    summary = data.get("summary", "")
    role = data.get("contact_role", "")
    goals = ", ".join(data.get("student_goals", []))

    prompt_template = ChatPromptTemplate.from_template("""
Interaction Summary: {summary}
Contact Role: {role}
Student Goals: {goals}

Instructions:
- Check if the contact's role aligns with any student goals.
- Check if the interaction content is related to the goals.
- Score the relevance from 0 to 100.

Output as JSON:
- relevance_score
- contact_alignment (boolean)
- content_relevance (boolean)
- goal_synergy_reasoning (string)
""")

    prompt = prompt_template.format(summary=summary, role=role, goals=goals)
    result = llm.invoke(prompt)

    try:
        json_output = eval(result.content)
    except Exception:
        return jsonify({ "error": "Failed to parse LLM output" }), 400

    return jsonify(json_output)

if __name__ == '__main__':
    app.run(port=8002)
