from agents.base import BaseAgent


class AnnotationAgent(BaseAgent):
    system_prompt = "You are a helpful assistant programmer that summarizes code, Summarize args and return type as python annotations. Output in JSON."
    prompt = "{code}"
    response_format = {
        "type": "json_object",
        "schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "function_name": {"type": "string"},
                    "annotation": {"type": "string"},
                    "what_does_it_do": {"type": "string"},
                },
                "required": ["function_name", "annotation", "what_does_it_do"],
            },
        },
    }
    temperature = 0.2
