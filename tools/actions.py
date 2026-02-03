import os
import shutil
import pyautogui

def create_fastapi_project(project_name):
    """Initializes a standard FastAPI folder structure in the root."""
    # Create the root folder for the new project
    base_path = os.path.join(os.getcwd(), project_name)
    
    # Define your preferred folder structure
    folders = [
        os.path.join(base_path, "app"),
        os.path.join(base_path, "app/api"),
        os.path.join(base_path, "core"),
        os.path.join(base_path, "tools")
    ]
    
    try:
        os.makedirs(base_path, exist_ok=True)
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            
        # Create a boilerplate main.py
        main_py_path = os.path.join(base_path, "app/main.py")
        with open(main_py_path, "w") as f:
            f.write("from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {'status': 'FastAPI is running'}")
            
        return f"Successfully created FastAPI project '{project_name}' at {base_path}."
    except Exception as e:
        return f"Failed to create project: {str(e)}"

def organize_images():
    """Moves all screenshots from /images to /images/backup."""
    root_dir = os.getcwd()
    source_dir = os.path.join(root_dir, "images")
    backup_dir = os.path.join(source_dir, "backup")

    if not os.path.exists(source_dir):
        return "The images folder does not exist yet, sir."

    os.makedirs(backup_dir, exist_ok=True)

    try:
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        if not files:
            return "No screenshots found to move."

        for file in files:
            shutil.move(os.path.join(source_dir, file), os.path.join(backup_dir, file))
        
        return f"Moved {len(files)} screenshots to the backup folder."
    except Exception as e:
        return f"Error during organization: {str(e)}"

def media_command(action):
    """Sends hardware media signals to Windows."""
    # Mapping friendly names to PyAutoGUI hardware keys
    commands = {
        "play": "playpause",
        "pause": "playpause",
        "next": "nexttrack",
        "previous": "prevtrack",
        "volume up": "volumeup",
        "volume down": "volumedown",
        "mute": "volumemute"
    }
    
    key = commands.get(action.lower())
    if key:
        pyautogui.press(key)
        return f"Executing {action} command."
    return "Unknown media command."