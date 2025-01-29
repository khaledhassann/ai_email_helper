from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.anthropic import AnthropicModel

OPENAI_MODEL = OpenAIModel('gpt-4o-mini')
OLLAMA_MODEL = OllamaModel('llama3.1:8b')
GROQ_MODEL = GroqModel('llama3-groq-8b-8192-tool-use-preview')
GEMINI_MODEL = GeminiModel('gemini-2.0-flash-exp')
ANTHROPIC_MODEL = AnthropicModel('claude-3-5-sonnet-20241022')