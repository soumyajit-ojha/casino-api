import os

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "env",
    ".idea",
    ".vscode",
    "node_modules",
    "config",
    "var",
}


def print_directory_tree(root_path, prefix=""):
    try:
        items = sorted(os.listdir(root_path))
    except PermissionError:
        return

    for index, item in enumerate(items):
        if item in IGNORE_DIRS:
            continue

        full_path = os.path.join(root_path, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        print(prefix + connector + item)

        if os.path.isdir(full_path):
            extension = "    " if index == len(items) - 1 else "│   "
            print_directory_tree(full_path, prefix + extension)


if __name__ == "__main__":
    project_root = os.getcwd()  # current directory
    print(os.path.basename(project_root) + "/")
    print_directory_tree(project_root)
