import PySimpleGUI as sg
import requests
import json

# Define the API URL and headers
URL = 'http://localhost:11434/api/generate'
HEADERS = {'Content-Type': 'application/json'}

# List of predefined models (all lowercase to avoid 404 errors)
MODEL_LIST = [
    "deepseek-r1:8b",
    "llama-2-7b",
    "mistral-7b",
    "llama-2-13b-quantized",
    "mistral-v0.2-fine-tune",
    "distilled-llama-2-7b",
    "qwen-1.5b",
    "deepseek-r1:1.5b",
    "llama-2-chat-7b",
    "mistral-fine-tune-rag",
    "distilled-mistral-7b"
]

# List of context lengths
CTX_LIST = ["1024", "2048", "4096", "8192", "16384"]

# Function to stream responses from the API
def get_response(user_message, model_name, ctx_length, window):
    data = {
        "model": model_name.lower(),  # Ensure model name is lowercase
        "prompt": user_message,
        "stream": False,  # Enable streaming
        "options": {
            "num_ctx": int(ctx_length)  # User-selected context length
        }
    }
    try:
        response = requests.post(URL, headers=HEADERS, json=data, stream=True)
        if response.status_code == 200:
            streamed_text = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            streamed_text += chunk["response"]
                            window["CHAT_HISTORY"].update(streamed_text + "\n\n", append=True)
                    except json.JSONDecodeError:
                        continue
        else:
            window["CHAT_HISTORY"].update(f"Error: {response.status_code} - {response.text}\n\n", append=True)
    except requests.exceptions.RequestException as e:
        window["CHAT_HISTORY"].update(f"Request failed: {e}\n\n", append=True)

# Define the PySimpleGUI layout
sg.theme("DarkBlue3")
layout = [
    [sg.Text("Chat with Ollama LLM", font=("Arial", 14), justification="center", size=(50, 1))],
    
    # Model Selection (Dropdown + Manual Input)
    [sg.Text("Model:", font=("Arial", 14)), 
     sg.Combo(MODEL_LIST, default_value="deepseek-r1:8b", key="MODEL", size=(30, 1), enable_events=True, readonly=True),
     sg.Button("Load Model"),  # Button to load selected model
     sg.InputText("deepseek-r1:8b", key="MODEL_INPUT", size=(20, 1))],
    
    # Context Length Selection
    [sg.Text("Context Length:", font=("Arial", 12)), 
     sg.Combo(CTX_LIST, default_value="8192", key="CTX", size=(14, 1), readonly=True)],

    # Multi-line input box
    [sg.Multiline(key="USER_INPUT", size=(60, 4), font=("Arial", 18), enter_submits=False)],
    
    [sg.Button("Send", bind_return_key=True)],

    # Chat History Output
    [sg.Multiline(size=(60, 20), key="CHAT_HISTORY", font=("Arial", 18), disabled=True, autoscroll=True)]
]

# Create the window
window = sg.Window("Ollama Chat", layout, size=(1000, 800), resizable=True)

# Event loop
chat_history = ""
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    
    elif event == "Load Model":
        selected_model = values["MODEL"].strip().lower()  # Force lowercase for compatibility
        window["MODEL_INPUT"].update(selected_model)
    
    elif event == "Send":
        user_message = values["USER_INPUT"].strip()
        model_name = values["MODEL_INPUT"].strip().lower()  # Force lowercase
        ctx_length = values["CTX"].strip()
        
        if user_message:
            chat_history += f"You: {user_message}\nOllama ({model_name}) - ctx {ctx_length}:\n"
            window["CHAT_HISTORY"].update(chat_history, append=True)
            window["USER_INPUT"].update("")
            get_response(user_message, model_name, ctx_length, window)

window.close()
