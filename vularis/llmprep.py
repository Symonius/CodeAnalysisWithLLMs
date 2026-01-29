import requests
import json

def prepare_gpt_data(LLM, SYSTEM_PROMPT, user_prompt_final, TEMPERATURE):
    if LLM == "gpt-4o":
        endpoint = "https://[INSERTURL_gpt4]"
    else:
        endpoint = "https://[INSERTURL_gpt4omini]"

    body = {
        "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt_final},
    ],
        "temperature": TEMPERATURE
    }
    return endpoint, body
    
def prepare_gemini_data(LLM, SYSTEM_PROMPT, user_prompt_final, TEMPERATURE):
    if LLM == "gemini-2_5-flash":
        endpoint = "https://[INSERTURL_gemini2_5-flash]"
    else:
        endpoint = "https://[INSERTURL_gemini2_5-pro]"

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_prompt_final
                    }
                ]
            }
        ],
        "systemInstruction": {
            "role": "ThisStringWillBeIgnored",
            "parts": [
                {
                    "text": SYSTEM_PROMPT
                }
            ]
        },
        "generationConfig": {
            "temperature": TEMPERATURE,
            "responseMimeType": "application/json",
        }
    }

    return endpoint, body

def call_api(endpoint, headers, data):
    res = requests.post(endpoint, headers=headers, json=data)
    response_code = res.status_code
    response_text = res.json()["choices"][0]["message"]["content"] if "choices" in res.text else res.json()["candidates"][0]["content"]["parts"][0]["text"]
    return response_code, response_text

def process_response(response_code, response_text, file_path, FOLDER_PATH, file_content, debug, endpoint, headers, body):
    vulnerability_dict = {}
    if debug:
        vulnerability_dict["raw"] = {
            "endpoint": endpoint,
            "headers": headers,
            "body": body
        }
    
    print("Response: ", response_code)
    print("ResponseText: ", response_text)
    vulnerability_dict.update({
        "response_code_api_query": response_code,
        "filename": file_path.replace(FOLDER_PATH, "").lstrip("\\/"), # Handles both Windows and Linux paths
        "file_content": file_content,
        "vulnerabilities": [] 
    })

    for vul in json.loads(response_text): 
        vulnerability = {
            "code_line": vul.get("code_line"),
            "vulnerability_id": vul.get("vulnerability_id"),
            "description": vul.get("vulnerability_description")
        }
        vulnerability_dict["vulnerabilities"].append(vulnerability)

    return vulnerability_dict