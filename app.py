from flask import Flask, request, jsonify
from flask_cors import CORS
from model.retriever import Retriever
from model.generator import Generator
import json
import traceback

app = Flask(__name__)
CORS(app)

retriever = Retriever()
generator = Generator()

# load sản phẩm
datas = []
with open('data/val-qar.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 2:
            break
        data = json.loads(line.strip())
        datas.append(data)
# tạo documents cho retriever
documents = []
for entry in datas:
    for snippet in entry.get("review_snippets", []):
        documents.append(snippet)
    for ans in entry.get("answers", []):
        documents.append(ans.get("answerText", ""))

retriever.add_documents(documents)

@app.route('/chat', methods=['POST'])
def chat():
    try:    
        user_message = request.json.get('message', '')
        print(f"user: {user_message}")

        relevant_docs = retriever.search(user_message)
        context = "\n".join(relevant_docs)
        print(f"[Relevant docs]: {relevant_docs}")

        answer = generator.generate_answer(user_message, context)
        print(f"[Generated answer]: {answer}")

        return jsonify({
            "reply": answer,
            "context": relevant_docs  
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)