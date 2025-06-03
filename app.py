from flask import Flask, request, jsonify
from flask_cors import CORS
from model.retriever import Retriever
from model.generator import Generator
import json
import traceback
from transformers import pipeline

app = Flask(__name__)
CORS(app)

retriever = Retriever()
generator = Generator()

vi2en = pipeline("translation_vi_to_en", model="Helsinki-NLP/opus-mt-vi-en")
en2vi = pipeline("translation_en_to_vi", model="Helsinki-NLP/opus-mt-en-vi")

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
        user_message_en = vi2en(user_message_vi)[0]['translation_text']
        print(f"user: {user_message_en}")

        relevant_docs = retriever.search(user_message_en)
        context = "\n".join(relevant_docs)
        print(f"[Relevant docs]: {relevant_docs}")

        answer_en = generator.generate_answer(user_message_en, context)
        print(f"[Generated answer]: {answer_en}")
        # answer_vi = en2vi(answer_en)[0]['translation_text']
        # print(f"[Generated answer]: {answer_vi}")

        return jsonify({
            "reply": answer_en,
            "context": relevant_docs  
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)