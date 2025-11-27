
from typing import Dict
import os
from openai import OpenAI
import json

class OpenAIAdapter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY env var or pass it in.")
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, temperature: float = 0.0) -> Dict[str, object]:
        """
        Generates a response from OpenAI and attempts to parse it into the expected format.
        Expected format from LLM for this pipeline:
        {
            "classification": "positive" | "negative",
            "confidence": 0.0 to 1.0,
            "text": "explanation..."
        }
        """
        
        system_prompt = (
            "You are a helpful assistant. "
            "Analyze the sentiment of the user input provided in the prompt. "
            "You MUST return a valid JSON object with the following keys: "
            "'classification' (either 'positive' or 'negative'), "
            "'confidence' (a float between 0.0 and 1.0), "
            "and 'text' (a brief explanation)."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)
            
            return {
                "text": parsed.get("text", content),
                "classification": parsed.get("classification", "unknown"),
                "confidence": parsed.get("confidence", 0.0)
            }

        except Exception as e:
            # Fallback or error handling
            return {
                "text": f"Error calling OpenAI: {str(e)}",
                "classification": "error",
                "confidence": 0.0
            }
