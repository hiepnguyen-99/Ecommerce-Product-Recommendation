from flask import Flask, request, jsonify
from flask_cors import CORS
from model.retriever import Retriever
from model.generator import Generator
import json
import traceback
from googletrans import Translator

app = Flask(__name__)
CORS(app)

retriever = Retriever()
generator = Generator()
translator = Translator()

# load data
with open('data/val.json', 'r', encoding='utf-8') as f:
    datas = json.load(f)
# tạo documents cho retriever
documents = []
for entry in datas:
    documents.append(entry.get("context", ''))

retriever.add_documents(documents)

@app.route('/chat', methods=['POST'])
def chat():
    try:    
        user_message_vi = request.json.get('message', '')
        user_message_en = translator.translate(user_message_vi, src='vi', dest='en').text
        print(f"user: {user_message_en}")

        relevant_docs = retriever.search(user_message_en)
        context = "\n".join(relevant_docs)
        print(f"[Relevant docs]: {relevant_docs}")

        answer_en = generator.generate_answer(user_message_en, context)
        answer_vi = translator.translate(answer_en, src='en', dest='vi').text
        print(f"[Generated answer]: {answer_vi}")

        return jsonify({
            "reply": answer_vi,
            "context": relevant_docs  
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)