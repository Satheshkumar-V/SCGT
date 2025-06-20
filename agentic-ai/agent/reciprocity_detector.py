from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = "sk-..."  # Replace with your key

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

@app.route("/check-reciprocity", methods=["POST"])
def check_reciprocity():
    data = request.json
    summary = data.get("summary", "")
    quality_score = data.get("quality_score", 0)

    prompt_template = ChatPromptTemplate.from_template("""
Interaction Summary: {summary}
Quality Score: {quality_score}

Analyze:
- Does the interaction reflect a balanced relationship or is it one-sided?
- Identify if the user is always requesting without giving.
- Highlight any helpful exchanges.

Output as JSON:
- reciprocity_status ("balanced" or "one-sided")
- evidence (string with reasoning)
""")

    prompt = prompt_template.format(summary=summary, quality_score=quality_score)
    result = llm.invoke(prompt)

    try:
        json_output = eval(result.content)
    except Exception:
        return jsonify({ "error": "Failed to parse LLM output" }), 400

    return jsonify(json_output)

if __name__ == '__main__':
    app.run(port=8003)
