import requests
import json
import datetime
import os
import argparse
import copy

# Self-developed modules
import scscraper
import secrets
import jsonhandler
import user_prompt
import system_prompt
import llmprep

# Debug-Mode
DEBUG = 1

# Set API key
API_KEY = secrets.API_KEY

def parse_arguments():
    parser = argparse.ArgumentParser(description="A program that uses an LLM and processes files from a specified folder path.")
    
    parser.add_argument('--llm', type=str, required=True, choices=["gpt-4o", "gpt-4o-mini", "gemini-2_5-flash", "gemini-2_5-pro"], help='The Large Language Model (LLM) to use.')
    parser.add_argument('--scfolder', type=str, required=True, help='The folder path for source code scraping.')
    parser.add_argument('--prompt', type=str, required=True, choices=["basic", "opt1", "opt2", "opt3"], help='Select the type of the system prompt to use.')
    
    return parser.parse_args()

def get_system_prompt(prompt):
    prompts = {
        "basic": system_prompt.SYSTEM_PROMPT_BASIC,
        "opt1": system_prompt.SYSTEM_PROMPT_OPT_I,
        "opt2": system_prompt.SYSTEM_PROMPT_OPT_II,
        "opt3": system_prompt.SYSTEM_PROMPT_OPT_III
    }
    return prompts.get(prompt, "")

def create_user_prompt(file_path, file_content):
    user_prompt_without_file = user_prompt.USER_PROMPT
    file_name = os.path.basename(file_path)
    numbered_lines = "\n".join(f"{i + 1}: {line}" for i, line in enumerate(file_content.splitlines()))
    return f"{user_prompt_without_file}File: {file_name}\n{numbered_lines}"

def redact_api_key(headers: dict) -> dict:
    """
    Finds and redacts the 'api-key' value in a dictionary of headers for safe logging.
    This function is case-insensitive for the 'api-key' header name.
    It returns a new, modified dictionary, leaving the original unchanged.

    Args:
        headers (dict): The original headers dictionary.

    Returns:
        dict: A new dictionary with the API key redacted.
    """
    # Create a deep copy to avoid modifying the original dictionary in place
    safe_headers = copy.deepcopy(headers)

    # Find the actual key name, ignoring case (e.g., 'api-key', 'Api-Key')
    api_key_name = None
    for key in safe_headers:
        if key.lower() == 'api-key':
            api_key_name = key
            break

    # If an API key was found, redact it
    if api_key_name:
        original_key = safe_headers[api_key_name]
        
        # Ensure the key is a string and long enough to be partially redacted
        if isinstance(original_key, str) and len(original_key) > 6:
            first_part = original_key[:3]
            last_part = original_key[-3:]
            safe_headers[api_key_name] = f"{first_part}...REDACTED...{last_part}"
        else:
            # If the key is too short or not a string, redact it completely
            safe_headers[api_key_name] = "***REDACTED***"
            
    return safe_headers


def main():
    args = parse_arguments()
    LLM = args.llm
    SCFOLDER_PATH = args.scfolder
    SYSTEM_PROMPT = get_system_prompt(args.prompt)
    TEMPERATURE = 0
    detected_vulnerabilities = []

    for loop, (file_path, file_content) in enumerate(scscraper.read_files_one_by_one(SCFOLDER_PATH), start=1):
        
        user_prompt_final = create_user_prompt(file_path, file_content)
        
        headers = {"Content-type": "application/json", "api-key": API_KEY}
        
        if LLM in ["gpt-4o", "gpt-4o-mini"]:
            endpoint, body = llmprep.prepare_gpt_data(LLM, SYSTEM_PROMPT, user_prompt_final, TEMPERATURE)
        elif LLM in ["gemini-2_5-flash", "gemini-2_5-pro"]:
            endpoint, body = llmprep.prepare_gemini_data(LLM, SYSTEM_PROMPT, user_prompt_final, TEMPERATURE)
        else:
            print("Error: Specified LLM not found")
            continue
        
        response_code, response_text = llmprep.call_api(endpoint, headers, body)
        
        vulnerability_dict = llmprep.process_response(response_code, response_text, file_path, SCFOLDER_PATH, file_content, DEBUG, endpoint, redact_api_key(headers), body)
            
        detected_vulnerabilities.append(vulnerability_dict)

    current_datetime = datetime.datetime.now()
    report_data = {
        "report_timestamp": current_datetime.strftime("%d.%m.%Y %H:%M:%S"),
        "scfolder": SCFOLDER_PATH,
        "prompttype": args.prompt,
        "analysis_details": {
            "sysprompt": SYSTEM_PROMPT,
            "userprompt": user_prompt.USER_PROMPT,
            "model": LLM,
            "config": {
                "temperature": TEMPERATURE,
            },
        },
        "vulnerabilities_found": detected_vulnerabilities
    }

    report_name = f"VD-report {LLM} {args.prompt} {current_datetime.strftime('%Y-%m-%d %H-%M-%S')}"
    if DEBUG:
        report_name += f" debug"
    jsonhandler.save_json_data(report_data, report_name)

if __name__ == "__main__":
    main()
