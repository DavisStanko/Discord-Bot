import os
import random

# Get a list of all the folders in a directory
def get_child_folders(path):
    return [entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]


def get_commands():
    # Get the media paths
    main_dir = os.path.dirname(os.path.realpath(__file__))
    content_path = os.path.join(main_dir, "content")

    # Get the command lists
    content_commands = sorted(["!" + command for command in get_child_folders(content_path)])

    # Format the command lists
    content_commands = "\n".join([f"`{command}`" for command in content_commands])
    
    return content_commands

def get_file(request):
    # Get the path to the folder
    main_dir = os.path.dirname(os.path.realpath(__file__))
    content_path = os.path.join(main_dir, "content")
    folder_path = os.path.join(content_path, request)
    # Get the list of files
    files = os.listdir(folder_path)
    # Get a random file
    reply = os.path.join(folder_path, files[random.randint(0, len(files) - 1)])
    return reply