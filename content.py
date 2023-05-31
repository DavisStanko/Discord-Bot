import os

# Get a list of all the folders in a directory
def get_child_folders(path):
    return [entry for entry in os.listdir(path) if os.path.isdir(os.path.join(path, entry))]

# Get the media paths
main_dir = os.path.dirname(os.path.realpath(__file__))
content_path = os.path.join(main_dir, "internet")

# Get the command lists
content_commands = sorted(["!" + command for command in get_child_folders(content_path)])

# Format the command lists
content_commands = "\n".join([f"`{command}`" for command in content_commands])