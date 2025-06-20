from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = "sk-..."  # Replace with your real key

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

@app.route("/generate-okr-report", methods=["POST"])
def generate_okr_report():
    data = request.json
    interactions = data.get("interactions", [])
    student_name = data.get("student_name", "Student")

    formatted_data = "\n".join(
        [f"- {i['contact_name']} | Quality: {i['quality_score']}, Relevance: {i['relevance_score']}, Reciprocity: {i['reciprocity_status']}\nSummary: {i['summary']}" for i in interactions]
    )

    template = ChatPromptTemplate.from_template("""
Student: {student_name}
Interaction Details:
{formatted_data}

Instructions:
1. Identify high-value interactions: quality > 70, relevance > 70, reciprocity = balanced.
2. Summarize meaningful connections.
3. Format output in JSON:
- summary
- high_value_connections (list of { contact_name, reasons })
- low_value_connections (list of { contact_name, reasons })
""")

    prompt = template.format(student_name=student_name, formatted_data=formatted_data)
    result = llm.invoke(prompt)

    try:
        json_output = eval(result.content)
    except:
        return jsonify({ "error": "Invalid LLM JSON format" }), 400

    return jsonify(json_output)

if __name__ == '__main__':
    app.run(port=8004)
