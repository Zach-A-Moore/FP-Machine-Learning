import os
import time
import subprocess

def run_lua_script(script_path, params=""):
    """
    Execute a Lua script via Cheat Engine.
    Adjust the command based on your Cheat Engine setup.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_script_path = os.path.join(base_dir, script_path)
    
    # Example: Assume Cheat Engine can be called via command line
    # Replace with actual command or method (e.g., writing to a monitored file)
    command = f"cheatengine --load-script {full_script_path} {params}"
    print(f"Executing Lua script: {command}")
    
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Lua script {script_path}: {e}")
    
    # Small delay to ensure script execution completes
    time.sleep(0.5)