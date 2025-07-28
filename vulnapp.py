# create_project.py
# A self-contained Python script to create the necessary files and directories
# for a vulnerable Flask web application.
# This script does NOT install any system services and does NOT require sudo.
#
# USAGE: python3 create_project.py
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!         WARNING            !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# The generated application has a DELIBERATE command injection vulnerability
# for educational purposes (TryHackMe, CTF). DO NOT use it on a production server.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import os

# --- Configuration ---
PROJECT_NAME = "VulnerableWebApp"
FLASK_APP_FILENAME = "app.py"
HTML_FILENAME = "index.html"
FLASK_PORT = 8080

# --- Code Templates ---

# Template for the Flask Application (app.py)
# All code and comments are in English for the TryHackMe context.
FLASK_APP_CODE = f"""
import subprocess
from flask import Flask, request, render_template

# Initialize the Flask application
app = Flask(__name__)

# This route serves the main HTML page from the 'templates' folder
@app.route('/')
def index():
    # Renders and returns the content of index.html to the browser
    return render_template('{HTML_FILENAME}')

# This route processes the ping request and contains the VULNERABILITY
@app.route('/ping')
def ping():
    # Get the 'ip' parameter from the URL (e.g., ?ip=8.8.8.8)
    ip_address = request.args.get('ip', '')

    # WARNING: The 'shell=True' argument makes this code vulnerable to command injection.
    # It allows special characters like ';' or '&&' to be interpreted by the system's shell.
    try:
        command_to_run = f"ping -c 3 {{ip_address}}"
        result = subprocess.run(
            command_to_run,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        # Combine standard output and standard error for display
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Error: The command took too long to execute."

    # Return the output formatted inside a <pre> tag for readability
    return f"<pre>Executing command...\\n\\n{{output}}</pre>"

# This block runs the app when the script is executed directly
if __name__ == "__main__":
    # Runs the development server.
    # host='0.0.0.0' makes it accessible from other devices on the same network.
    print(f"Starting Flask server on http://0.0.0.0:{FLASK_PORT}")
    app.run(host='0.0.0.0', port={FLASK_PORT})
"""

# Template for the HTML User Interface (index.html)
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Command Tool</title>
    <style>
        body {{ font-family: monospace; background-color: #0d1117; color: #c9d1d9; margin: 40px; text-align: center; }}
        .container {{ max-width: 700px; margin: auto; background: #161b22; padding: 30px; border-radius: 8px; border: 1px solid #30363d; }}
        h1 {{ color: #e8554a; }}
        form {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        input[type="text"] {{ flex-grow: 1; padding: 10px; border: 1px solid #30363d; border-radius: 6px; background-color: #0d1117; color: #c9d1d9; font-family: monospace; }}
        button {{ padding: 10px 15px; background-color: #e8554a; color: #ffffff; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }}
        button:hover {{ background-color: #f36e65; }}
        p {{ color: #8b949e; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>System Command Executor</h1>
        <p>Enter a command or IP address. The system will execute it.</p>
        <form action="/ping" method="GET">
            <input type="text" name="ip" placeholder="8.8.8.8; ls -la">
            <button type="submit">Execute</button>
        </form>
    </div>
</body>
</html>
"""

def create_project_scaffold():
    """
    Main function to create the project directory and all necessary files.
    """
    print(f"--- Creating project scaffold: '{PROJECT_NAME}' ---")

    # Get the path for the new project directory in the current location
    project_path = os.path.join(os.getcwd(), PROJECT_NAME)
    templates_path = os.path.join(project_path, "templates")

    # Create the directories
    try:
        os.makedirs(templates_path, exist_ok=True)
        print(f"[+] Created directory: {project_path}")
        print(f"[+] Created directory: {templates_path}")
    except OSError as e:
        print(f"[!] ERROR: Could not create directories. {e}")
        return

    # Create the app.py file
    try:
        app_file_path = os.path.join(project_path, FLASK_APP_FILENAME)
        with open(app_file_path, "w") as f:
            f.write(FLASK_APP_CODE)
        print(f"[+] Created Flask app: {app_file_path}")
    except IOError as e:
        print(f"[!] ERROR: Could not write {FLASK_APP_FILENAME}. {e}")
        return

    # Create the index.html file
    try:
        html_file_path = os.path.join(templates_path, HTML_FILENAME)
        with open(html_file_path, "w") as f:
            f.write(HTML_CODE)
        print(f"[+] Created HTML template: {html_file_path}")
    except IOError as e:
        print(f"[!] ERROR: Could not write {HTML_FILENAME}. {e}")
        return

    print("\n--- Scaffold created successfully! ---")
    print("\nNext steps:")
    print(f"1. Navigate into the project directory:")
    print(f"   cd {PROJECT_NAME}")
    print(f"2. Install Flask (if you haven't already):")
    print(f"   pip3 install Flask")
    print(f"3. Run the application manually:")
    print(f"   python3 {FLASK_APP_FILENAME}")
    print(f"4. Open your browser and go to: http://127.0.0.1:{FLASK_PORT}")

if __name__ == "__main__":
    create_project_scaffold()
