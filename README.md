# DeepSeekPyChat

DeepSeekPyChat is a PySimpleGUI-based chat client that interacts with the Ollama LLM API.

## Prerequisites

1. **Python 3.6+**  
   Make sure you have Python installed on your system.

2. **Ollama**  
   You need to have [Ollama](https://ollama.com) installed.  
   Follow the installation instructions on the [Ollama website](https://ollama.com).

3. **DeepSeek Model**  
   After installing Ollama, pull the DeepSeek model by running the following command in your terminal:

```bash
ollama pull deepseek1.5b
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/DeepSeekPyChat.git
cd DeepSeekPyChat
```

2. (Optional) Create and activate a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate   # On Windows use: myenv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```



## Usage

Run the chat client by executing the following command:

```bash
python DeepSeekChat.py
#you might need to use python3 depending on your installation
```


## Contributing

Feel free to fork the repository and submit pull requests.


