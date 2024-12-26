import os
import sys

def set_pythonpath_to_project_root(root_path=None):
    """
    Sets the PYTHONPATH environment variable to the project's root directory.
    
    :param root_path: (str) Optional custom root path. If not provided, defaults
                      to the parent directory of the currently running script.
    """
    if root_path is None:
        # Default to the directory of the currently running script
        root_path = os.path.dirname(os.path.abspath(__file__))
    
    # Insert at the front of sys.path so that root modules/packages can be imported
    if root_path not in sys.path:
        sys.path.insert(0, root_path)

    # Set the PYTHONPATH environment variable
    os.environ["PYTHONPATH"] = root_path
    print(f"PYTHONPATH set to: {root_path}")

