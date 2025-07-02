# CLI SWE AI Assistant

## Overview

The CLI SWE AI Assistant is an innovative command-line interface (CLI) application designed to empower software engineers with an AI-powered assistant. This assistant, powered by Google's Gemini model, interacts directly with your local filesystem and command line through a suite of specialized tools. It aims to streamline software development tasks by providing an intelligent agent capable of understanding, modifying, and executing code within your project environment.

The core idea is to provide a conversational interface where you can instruct the AI to perform various software engineering tasks, from code analysis and refactoring to bug fixing and feature implementation. The AI's "thinking process" is made transparent through streamed thought summaries, giving you insight into its decision-making and planning.

## Features

*   **AI-Powered Code Interaction:** Leverage the Gemini model to understand and manipulate your codebase.
*   **Local Filesystem Access:** The AI can read, write, and delete files and directories.
*   **Command Line Execution:** Execute shell commands for tasks like running tests, installing dependencies, or building projects.
*   **Transparent Thinking Process:** Observe the AI's internal reasoning and planning through streamed thought summaries.
*   **Modular Tooling:** Utilizes the Model Context Protocol (MCP) for a structured and extensible tool server.
*   **Interactive CLI:** A rich and user-friendly command-line interface built with `rich`.

## How It Works

The application operates with a client-server architecture:

1.  **GUI Client (`gui/main.py`):** This is the main application you interact with. It handles user input, displays AI responses, and manages the conversation history.
2.  **MCP Tool Server (`swe_tools/run_server.py`):** This is a separate Python process that runs in the background. It exposes a set of software engineering tools (e.g., `view_directory_structure`, `read_file_content`, `run_shell_command`) to the AI.
3.  **Gemini API Integration:** The GUI client communicates with the Google Gemini API, sending user prompts and conversation history. The Gemini model, configured with the available tools, generates responses that can include natural language answers or requests to call specific tools.
4.  **Tool Execution:** When the Gemini model decides to use a tool, the GUI client intercepts this request and forwards it to the local MCP Tool Server. The server executes the requested tool, performs the action on your local filesystem or command line, and returns the result.
5.  **Iterative Process:** The AI can engage in multi-turn conversations, using tool outputs to inform subsequent actions or refine its answers. The "thinking" mode allows the AI to generate internal thoughts and plans, which are streamed to the user for transparency.

## Requirements

*   Python 3.8+

### Python Libraries

The following Python libraries are required. They can be installed via `pip` using the `requirements.txt` file.

*   `google-genai`
*   `mcp`
*   `rich`
*   `python-dotenv`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd clia
    ```
    (Replace `<repository_url>` with the actual URL of your repository.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    venv\\Scripts\\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google Gemini API Key:**
    *   Obtain a Google Gemini API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   Create a file named `.env` in the root directory of the project (`C:\Users\past9\OneDrive\Desktop\project\clia\`).
    *   Add your API key to the `.env` file in the following format:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```
        Replace `"YOUR_API_KEY_HERE"` with your actual API key.

## Usage

To start the CLI SWE AI Assistant, run the following command from the project's root directory:

```bash
python -m gui.main
```

Once started, you can type your software engineering tasks or questions, and the AI will respond.

## Configuration

*   **`gui/config.py`:** This file contains various configuration settings for the GUI client, including:
    *   `MODEL_NAME`: The Gemini model to use (e.g., `gemini-2.5-flash`).
    *   `SYSTEM_PROMPT`: The AI's core instructions (loaded from `gui/system_prompt.py`).
    *   `MCP_SERVER_SCRIPT`: The entry point for the MCP tool server.
    *   `MAX_TOOL_TURNS`: The maximum number of tool calls the AI can make in a single turn.
    *   `THEME`: UI styling and icons.

*   **`.env`:** As mentioned in the installation, this file is used to store your `GOOGLE_API_KEY`.

## Troubleshooting

*   **`ModuleNotFoundError`:** Ensure all dependencies are installed (`pip install -r requirements.txt`) and your virtual environment is activated. Also, verify that relative imports are correctly handled within Python packages.
*   **API Key Issues:** Double-check that your `GOOGLE_API_KEY` is correctly set in the `.env` file and that there are no extra spaces or characters.
*   **Tool Execution Errors:** If the AI reports errors during tool execution, review the tool's arguments and the project's state. The AI's thought summaries can provide clues.

