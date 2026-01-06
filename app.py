from flask import Flask, render_template, request, jsonify
import os
from llm_service import LLMService

import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
llm_service = LLMService()

def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  filename TEXT,
                  provider TEXT,
                  model_name TEXT,
                  system_prompt TEXT,
                  test_data TEXT,
                  test_page TEXT,
                  test_script TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def get_history():
    conn = sqlite3.connect('history.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, timestamp, filename, provider, model_name FROM history ORDER BY id DESC")
    rows = c.fetchall()
    history = [dict(row) for row in rows]
    conn.close()
    return jsonify(history)

@app.route('/history/<int:id>')
def get_history_item(id):
    conn = sqlite3.connect('history.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE id=?", (id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Item not found'}), 404

@app.route('/refactor', methods=['POST'])
def refactor():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    model = request.form.get('model', 'mock')
    api_key = request.form.get('api_key')
    model_name = request.form.get('model_name')
    system_prompt = request.form.get('system_prompt')
    language = request.form.get('language', 'javascript')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        content = file.read().decode('utf-8')
        result = llm_service.generate_pom_files(content, model, api_key, model_name, system_prompt, language)
        
        # Save to history
        try:
            conn = sqlite3.connect('history.db')
            c = conn.cursor()
            c.execute("INSERT INTO history (timestamp, filename, provider, model_name, system_prompt, test_data, test_page, test_script) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file.filename, model, model_name, system_prompt, result['test_data'], result['test_page'], result['test_script']))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving history: {e}")

        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
