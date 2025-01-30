# AI Email Assistant (Powered by Ollama)

## Overview

The AI Email Assistant is a Gradio-based application that helps users generate and refine emails using the DeepSeek AI model, which is powered by Ollama. The application allows users to specify the recipient's name, email, the purpose of the email, and the desired tone. The AI then generates a draft email and refines it based on feedback until the email is finalized.

## Features

- Generate emails based on user input
- Refine emails based on feedback
- Supports different tones: casual, professional, and formal
- Interactive Gradio UI for easy use

## Tech Stack

- **Python**: The core programming language used for the application.
- **Gradio**: A Python library for creating interactive UIs.
- **Ollama**: Used to run the DeepSeek AI model locally.
- **Asyncio**: For handling asynchronous operations.
- **Pydantic**: For data validation and settings management.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/ai-email-assistant.git
    cd ai-email-assistant
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv .venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```sh
    python email_feedback_gradio_standard.py
    ```

2. **Open the Gradio UI**:
    - After running the application, a local URL will be provided in the terminal. Open this URL in your web browser to access the Gradio UI.

3. **Generate and refine emails**:
    - Enter the recipient's name, email, the purpose of the email, and select the desired tone.
    - Click the "Generate Email" button to generate a draft email.
    - The AI will provide feedback and refine the email until it is finalized.

## File Structure

- [email_feedback_gradio_standard.py](http://_vscodecontentref_/0): The main application file that sets up the Gradio UI and handles email generation and refinement.
- [load_models.py](http://_vscodecontentref_/1): Contains the logic to load and use the DeepSeek AI model via Ollama.
- [requirements.txt](http://_vscodecontentref_/2): Lists all the dependencies required for the project.
- [.gitignore](http://_vscodecontentref_/3): Specifies files and directories to be ignored by Git.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Gradio](https://gradio.app/)
- [Ollama](https://ollama.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
