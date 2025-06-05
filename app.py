import json
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from model.retriever import Retriever
from model.generator import Generator
from transformers import pipeline
from datasets import load_dataset
from langdetect import detect

app = Flask(__name__)
CORS(app)

retriever = Retriever()
generator = Generator()

vi2en = pipeline("translation_vi_to_en", model="Helsinki-NLP/opus-mt-vi-en")
en2vi = pipeline("translation_en_to_vi", model="Helsinki-NLP/opus-mt-en-vi")

# load data
datas = load_dataset('hiepnguyenn-99/amazon-qa', data_files='reduced_data.json', split='all')
# tạo documents cho retriever
documents = [
    f"{entry['question']}? answer: {entry['answer']}"
    for entry in datas
]

retriever.add_documents(documents)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        raw_message = request.json.get('message', '')

        try:
            lang = detect(raw_message)
        except:
            lang = 'en'

        if lang == 'vi':
            user_message_en = vi2en(raw_message)[0]['translation_text']
        else:
            user_message_en = raw_message
        print(f"user: {user_message_en}")

        relevant_docs = retriever.search(user_message_en)
        context = "\n".join(relevant_docs)
        print(f"[Relevant docs]: {relevant_docs}")

        answer_en = generator.generate_answer(user_message_en, context)
        print(f"[Generated answer]: {answer_en}")
        # answer_vi = en2vi(answer_en)[0]['translation_text']
        # print(f"[Generated answer]: {answer_en}")

        return jsonify({
            "reply": answer_en
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)