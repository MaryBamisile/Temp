from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import os

app = Flask(__name__)
CORS(app)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_facts(number):
    properties = []
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    if is_armstrong(number):
        properties.append("armstrong")

    facts = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": math.isqrt(number) ** 2 == number,
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(number)),
        "fun_fact": f"{number} is an Armstrong number because {' + '.join(f'{d}^{len(str(number))}' for d in map(int, str(number)))} = {number}" if is_armstrong(number) else f"Did you know? The number {number} appears in many interesting ways in mathematics!"
    }
    return facts

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = int(request.args.get('number', 0))
        facts = get_facts(number)
        return jsonify(facts)
    except ValueError:
        return jsonify({"number": request.args.get('number', ""), "error": True}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render’s assigned port
    app.run(host='0.0.0.0', port=port)
