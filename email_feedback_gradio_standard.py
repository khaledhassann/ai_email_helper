from __future__ import annotations
import asyncio
import gradio as gr
from load_models import generate_response  # Import the Ollama function

# Define email tones
TONE_OPTIONS = {
    "casual": "Write in a friendly, relaxed, and conversational tone.",
    "professional": "Write in a clear, direct, and professional tone.",
    "formal": "Write in a highly structured, respectful, and polished tone."
}

async def handle_email_flow(name, email, purpose, tone):
    """
    Handles the email generation and refinement loop.
    Uses Ollama (via `generate_response()`) to create and refine emails.
    """
    messages = []
    feedback = None

    while True:
        # Construct the prompt dynamically
        tone_instruction = TONE_OPTIONS.get(tone, "Write in a professional tone.")
        prompt = (
            f"{tone_instruction}\n"
            f"Write an email with the following details:\n"
            f"- Purpose: {purpose}\n"
            f"- Recipient Name: {name}\n"
            f"- Ensure the tone matches: {tone}.\n\n"
        )

        if feedback:
            prompt = f"Refine the previous email based on this feedback: {feedback}\n{prompt}"

        email_subject, email_body, feedback = "Generating email...", "", ""
        yield email_subject, email_body, feedback

        # Generate the email draft using Ollama
        email_body = generate_response(prompt)
        email_subject = f"Re: {purpose}"  # Auto-generate a basic subject line

        if not feedback:
            yield email_subject, email_body, "Draft generated, submitting for feedback..."
        else:
            yield email_subject, email_body, "Refinement complete, reviewing again..."

        # Ask for feedback on the generated email
        feedback_prompt = f"Review this email:\n\n{email_body}\n\nIs this well-written? If not, suggest improvements."
        feedback = generate_response(feedback_prompt)

        # If feedback indicates changes are needed, loop again
        if "needs improvement" in feedback.lower() or "refine" in feedback.lower():
            yield email_subject, email_body, f'Feedback: {feedback}'
            await asyncio.sleep(5)
        else:
            yield email_subject, email_body, "Email finalized successfully!"
            break

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## AI Email Assistant (Powered by Ollama)")

    with gr.Row():
        name_input = gr.Textbox(label="Recipient Name", placeholder="Enter recipient name")
        email_input = gr.Textbox(label="Recipient Email", placeholder="Enter recipient email")

    email_purpose = gr.Textbox(label="Email Purpose", placeholder="What is this email about?")
    email_tone = gr.Dropdown(choices=list(TONE_OPTIONS.keys()), label="Email Tone", value="professional")

    email_subject = gr.Textbox(label="Generated Email Subject", interactive=False)
    email_body = gr.Textbox(label="Generated Email Body", interactive=False, lines=5)
    feedback_display = gr.Textbox(label="Feedback", interactive=False, lines=3)

    generate_button = gr.Button(value="Generate Email")
    generate_button.click(
        handle_email_flow,
        inputs=[name_input, email_input, email_purpose, email_tone],
        outputs=[email_subject, email_body, feedback_display]
    )

if __name__ == '__main__':
    demo.launch()
