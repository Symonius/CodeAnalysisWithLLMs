import json
import os

def save_json_data(data, filepath, report_dir="\\report", indent=4):
    """
    Saves data to a JSON file.

    Args:
        data (dict or list): The Python object to save.
        filepath (str): The path to the JSON file, relative to report_dir
                        e.g., "my_report.json" or "subfolder/my_report.json"
        report_dir (str, optional): The root directory where the file
                                        should be saved. Defaults to "/report".
        indent (int, optional): Indentation level for pretty-printing. Defaults to 4.

    Returns:
        bool: True if successful, False otherwise.
    """

    full_path_to_file = os.path.join(os.getcwd() + report_dir, filepath)
    target_directory = os.path.dirname(full_path_to_file)

    print(f"Attempting to save to: {full_path_to_file}") # Added for debugging
    print(f"Target directory: {target_directory}")       # Added for debugging

    try:
        # Ensure the target directory (and any necessary parent directories) exist
        os.makedirs(target_directory, exist_ok=True)
        print(f"Directory '{target_directory}' ensured to exist.") # Added for debugging

        # Open the file using the full path and write the JSON data
        with open(full_path_to_file + ".json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        print(f"Data successfully written to {full_path_to_file}")
        return True
    except PermissionError as e: # Catch PermissionError specifically
        print(f"ERROR: Permission denied when trying to write to {full_path_to_file}. Details: {e}")
        print("Suggestion: Try changing 'report_dir' to a path you have write access to, like a subdirectory of your script.")
        return False
    except IOError as e:
        print(f"ERROR: An I/O error occurred while writing to {full_path_to_file}. Details: {e}")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while saving {full_path_to_file}. Details: {e}")
        return False