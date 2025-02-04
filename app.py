from flask import Flask, jsonify, request
from flask_cors import CORS
import math
import requests

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

def get_fun_fact(number):
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math?json")
        if response.status_code == 200:
            return response.json().get("text", "No fun fact available.")
    except requests.RequestException:
        return "No fun fact available."
    return "No fun fact available."

def get_facts(number):
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    facts = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": math.isqrt(number) ** 2 == number,
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(number)),
        "fun_fact": get_fun_fact(number)
    }
    return facts

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_param = request.args.get('number')
    if number_param is None or not number_param.isdigit():
        return jsonify({"number": number_param, "error": True}), 400
    
    number = int(number_param)
    facts = get_facts(number)
    return jsonify(facts), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
