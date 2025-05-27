from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load danh sách sản phẩm
with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

def get_recommendations(user_input):
    """Tạo câu trả lời đơn giản"""
    user_input = user_input.lower()
    
    # Tìm sản phẩm phù hợp
    matched_products = []
    for product in products:
        print(product)
        if any(keyword in user_input for keyword in product.get('keywords', [])):
            matched_products.append(product['name'])
    
    # Tạo câu trả lời
    if matched_products:
        return f"Bạn có thể tham khảo {', '.join(matched_products[:2])}"
    else:
        return "Xin lỗi, tôi không tìm thấy sản phẩm phù hợp"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response_text = get_recommendations(user_message)
    return jsonify({"reply": response_text})

if __name__ == '__main__':
    app.run(debug=True)