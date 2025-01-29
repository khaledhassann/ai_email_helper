from __future__ import annotations
import asyncio
from dataclasses import dataclass,field
import gradio as gr
from pydantic import BaseModel, EmailStr
from pydantic_ai import Agent
from pydantic_ai.format_as_xml import format_as_xml
from pydantic_ai.messages import ModelMessage
from load_models import OPENAI_MODEL

@dataclass
class User:
    name: str
    email: EmailStr
    interests: list[str]

@dataclass
class Email:
    subject: str
    body: str

class EmailRequiresWrite(BaseModel):
    feedback: str

class EmailOK(BaseModel):
    pass

email_writer_agent = Agent(
    model=OPENAI_MODEL,
    result_type=Email,
    system_prompt=("Write a welcome email to our new members joining my AI Agent blog.","The first email must exclude interests")
)

feedback_agent = Agent[None, EmailRequiresWrite | EmailOK](
    OPENAI_MODEL,
    result_type = EmailRequiresWrite | EmailOK,
    system_prompt=("Review the email and provide feedback"
                   "The email must reference the user's specific interests"),
)

def create_user_xml(user: User):
    return f'''
    <user>
        <name>{user.name}</name>
        <email>{user.email}</email>
        <interests>{', '.join(user.interests)}</interests>
    </user>
'''

async def handle_email_flow(name, email, interests=''):
    user = User(name=name, email=email, interests=interests.split(', '))
    messages = []
    feedback = None

    while True:
        prompt = f"Write a welcome email:\n{create_user_xml(user)}" if not feedback else f"Refine the email based on feedback:\n{feedback}\n{create_user_xml(user)}"
        email_subject, email_body, feedback = "Generating email...", "", ""
        yield email_subject, email_body, feedback

        result = await email_writer_agent.run(prompt, message_history=messages)
        messages += result.all_messages()
        email = result.data
        email_subject, email_body = email.subject, email.body

        if not feedback:
            yield email_subject, email_body, "Draft generated, submitting for feedback..."
        else:
            yield email_subject, email_body, "Refinement complete, submitting reviewing..."
        
        feedback_prompt = format_as_xml({'user': user, 'email': email})
        feedback_result = await feedback_agent.run(feedback_prompt)

        if isinstance(feedback_result.data, EmailRequiresWrite):
            feedback = feedback_result.data.feedback
            yield email_subject, email_body, f'Feedback: {feedback}'
            await asyncio.sleep(7)
        elif isinstance(feedback_result.data, EmailOK):
            yield email_subject, email_body, "Email finalized successfully!"
            break

with gr.Blocks() as demo:
    gr.Markdown("## AI Email Feedback Agent")

    with gr.Row():
        name_input = gr.Textbox(label="Name", placeholder="Enter your name")
        email_input = gr.Textbox(label="Email", placeholder="Enter your email")
        interests_input = gr.Textbox(label="Interests", placeholder="Enter your interests (comma-separated)")
    
    email_subject = gr.Textbox(label="Email Subject", interactive=False)
    email_body = gr.Textbox(label="Email Body", interactive=False, lines=5)

    with gr.Row():
        feedback_display = gr.Textbox(label="Feedback", interactive=False, lines=3)

    generate_button = gr.Button(text="Generate Email")
    generate_button.click(
        handle_email_flow,
        inputs=[name_input, email_input, interests_input],
        outputs=[email_subject, email_body, feedback_display]
    )

if __name__ == '__main__':
    demo.launch()