from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from agent/.env
load_dotenv()

USE_OPENAI = True  # Set to False to use Gemini instead

app = Flask(__name__)

if USE_OPENAI:
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate

    # Get OpenAI key from .env
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        raise Exception("Missing OPENAI_API_KEY in .env file")

    os.environ["OPENAI_API_KEY"] = openai_api_key  # Used internally by langchain
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

else:
    import google.generativeai as genai

    # Get Gemini key from .env
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        raise Exception("Missing GEMINI_API_KEY in .env file")

    genai.configure(api_key=gemini_api_key)
    gemini_model = genai.GenerativeModel('gemini-pro')

@app.route("/evaluate-quality", methods=["POST"])
def evaluate_quality():
    data = request.json
    summary = data.get("summary", "")

    full_prompt = f"""You are a relationship analysis agent.

Interaction Summary: {summary}

Score each of the following from 0 to 10:
1. Helpfulness – Does this offer advice or value?
2. Supportiveness – Is the tone encouraging or positive?
3. Continuity – Does this suggest a long-term interaction?

Then return:
- Total score (scaled to 100)
- A breakdown of the 3 scores
- A one-line explanation
"""

    try:
        if USE_OPENAI:
            prompt = ChatPromptTemplate.from_template("{input}")
            chain = prompt | llm
            response = chain.invoke({"input": full_prompt})
            explanation = response.content.strip()
        else:
            response = gemini_model.generate_content(full_prompt)
            explanation = response.text.strip()

        result = {
            "quality_score": 85,
            "breakdown": {
                "helpfulness": 8,
                "supportiveness": 9,
                "continuity": 8
            },
            "explanation": explanation
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in Agent 2: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8001)
