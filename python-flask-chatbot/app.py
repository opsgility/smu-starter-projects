import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# TODO: Add your chat API endpoint here
# @app.route('/api/chat', methods=['POST'])
# def chat():
#     ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
