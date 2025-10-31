"""
Sample vulnerable Flask application
DO NOT USE IN PRODUCTION - For testing only!
"""

from flask import Flask, request, render_template_string
import sqlite3
import subprocess
import os

app = Flask(__name__)

# VULNERABILITY: Hardcoded credentials
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

@app.route('/')
def index():
    return "Vulnerable App for Security Testing"

@app.route('/search')
def search():
    # VULNERABILITY: SQL Injection
    query = request.args.get('q', '')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Unsafe - no parameterization
    cursor.execute(f"SELECT * FROM users WHERE name = '{query}'")
    results = cursor.fetchall()
    conn.close()
    return str(results)

@app.route('/execute')
def execute():
    # VULNERABILITY: Command Injection
    cmd = request.args.get('cmd', 'ls')
    # Unsafe subprocess call
    result = subprocess.check_output(cmd, shell=True)
    return result

@app.route('/template')
def template():
    # VULNERABILITY: Server-Side Template Injection
    name = request.args.get('name', 'Guest')
    template = f"<h1>Hello {name}</h1>"
    return render_template_string(template)

@app.route('/file')
def read_file():
    # VULNERABILITY: Path Traversal
    filename = request.args.get('file', 'default.txt')
    with open(filename, 'r') as f:
        content = f.read()
    return content

if __name__ == '__main__':
    # VULNERABILITY: Debug mode in production
    app.run(debug=True, host='0.0.0.0')
