# deploy_vulnerable_app.py
# A script to automatically deploy a vulnerable Flask web application
# as a systemd service on Debian-based systems.
#
# USAGE: sudo python3 deploy_vulnerable_app.py
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!         WARNING            !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# This script deploys a web application with a DELIBERATE and SEVERE
# command injection vulnerability. It is intended for educational purposes
# (like TryHackMe, CTF) ONLY.
#
# DO NOT run this on a production server or any machine with sensitive data.
# You are responsible for any consequences.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import os
import sys
import getpass
import subprocess

# --- Configuration ---
# You can change these values if you want.
SERVICE_NAME = "vulnerablewebapp"
FLASK_APP_FILENAME = "app.py"
HTML_FILENAME = "index.html"
FLASK_PORT = 8080

# --- Code Templates ---

# Template for the Flask Application (app.py)
FLASK_APP_CODE = f"""
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)

# This route serves the main HTML page
@app.route('/')
def index():
    return render_template('{HTML_FILENAME}')

# This route processes the ping request and is VULNERABLE
@app.route('/ping')
def ping():
    ip_address = request.args.get('ip', '') # Get 'ip' parameter from user

    # WARNING: The 'shell=True' argument makes this code vulnerable to command injection.
    # It directly passes the user's input to the system's shell.
    try:
        command = f"ping -c 3 {{ip_address}}"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Error: Command timed out."

    return f"<pre>Executing command...\\n\\n{{output}}</pre>"

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port={FLASK_PORT})
"""

# Template for the HTML User Interface (index.html)
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Ping Tool</title>
    <style>
        body {{ font-family: sans-serif; background-color: #1a1a1a; color: #e0e0e0; margin: 40px; text-align: center; }}
        .container {{ max-width: 700px; margin: auto; background: #2a2a2a; padding: 30px; border-radius: 8px; border: 1px solid #444; }}
        h1 {{ color: #ff4d4d; }}
        form {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        input[type="text"] {{ flex-grow: 1; padding: 10px; border: 1px solid #555; border-radius: 4px; background-color: #333; color: #e0e0e0; }}
        button {{ padding: 10px 15px; background-color: #ff4d4d; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background-color: #e60000; }}
        p {{ color: #aaa; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>System Command Executor</h1>
        <p>Enter an IP address to ping. The system will execute the command.</p>
        <form action="/ping" method="GET">
            <input type="text" name="ip" placeholder="e.g., 8.8.8.8">
            <button type="submit">Execute</button>
        </form>
    </div>
</body>
</html>
"""

# Template for the systemd service file
SYSTEMD_SERVICE_TEMPLATE = """
[Unit]
Description=A Vulnerable Flask Web Application for Educational Purposes
After=network.target

[Service]
User={username}
Group={group}
WorkingDirectory={workdir}
ExecStart={python_path} {app_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""

def run_command(command, as_root=False):
    """Helper function to run a shell command."""
    if as_root:
        command.insert(0, "sudo")
    print(f"[*] Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] ERROR: Command failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[!] ERROR: Command not found: {command[0]}. Is it installed?")
        sys.exit(1)

def main():
    """Main function to perform all setup steps."""
    print("--- Vulnerable Flask App Deployment Script ---")

    # --- Step 1: Check for root privileges ---
    if os.geteuid() != 0:
        print("[!] ERROR: This script needs to be run with root privileges.")
        print("[!] Please run it with: sudo python3 deploy_vulnerable_app.py")
        sys.exit(1)

    # --- Step 2: Define paths and user ---
    project_dir = os.path.dirname(os.path.realpath(__file__))
    app_path = os.path.join(project_dir, FLASK_APP_FILENAME)
    templates_dir = os.path.join(project_dir, "templates")
    html_path = os.path.join(templates_dir, HTML_FILENAME)
    # Get the user who invoked sudo, not 'root'
    username = os.environ.get("SUDO_USER", getpass.getuser())
    user_group = username # On most systems, group name is the same as username

    print(f"[*] Project Directory: {project_dir}")
    print(f"[*] Running as user: {username}")

    # --- Step 3: Create application files ---
    print("\n[+] Step 3: Creating application files...")
    os.makedirs(templates_dir, exist_ok=True)

    with open(app_path, "w") as f:
        f.write(FLASK_APP_CODE)
    print(f"    - Created {app_path}")

    with open(html_path, "w") as f:
        f.write(HTML_CODE)
    print(f"    - Created {html_path}")

    # --- Step 4: Find Python interpreter path ---
    print("\n[+] Step 4: Locating Python interpreter...")
    try:
        result = subprocess.run(["which", "python3"], capture_output=True, text=True, check=True)
        python_path = result.stdout.strip()
        print(f"    - Found python3 at: {python_path}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] ERROR: Could not find 'python3'. Please make sure it's installed and in your PATH.")
        sys.exit(1)

    # --- Step 5: Generate and install systemd service ---
    print("\n[+] Step 5: Creating and installing systemd service...")
    service_content = SYSTEMD_SERVICE_TEMPLATE.format(
        username=username,
        group=user_group,
        workdir=project_dir,
        python_path=python_path,
        app_path=app_path
    )
    
    service_filepath = f"/etc/systemd/system/{SERVICE_NAME}.service"
    print(f"    - Writing service file to {service_filepath}")
    with open(service_filepath, "w") as f:
        f.write(service_content)

    # --- Step 6: Reload, enable, and start the service ---
    print("\n[+] Step 6: Starting the service with systemctl...")
    run_command(["systemctl", "daemon-reload"])
    run_command(["systemctl", "enable", SERVICE_NAME])
    run_command(["systemctl", "start", SERVICE_NAME])

    print("\n--- DEPLOYMENT COMPLETE ---")
    print(f"[*] The vulnerable web application is now running as a service.")
    print(f"[*] To check its status, run: sudo systemctl status {SERVICE_NAME}")
    print(f"[*] You can access the app at: http://<YOUR_MACHINE_IP>:{FLASK_PORT}")
    print("\n[!] REMINDER: This application is INSECURE. Use it for educational purposes only.")

if __name__ == "__main__":
    main()
