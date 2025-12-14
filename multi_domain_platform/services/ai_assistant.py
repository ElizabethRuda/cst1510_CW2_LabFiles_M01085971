"""
AI Assistant service for AI-powered features
"""
import os
from typing import Optional, Dict, Any
from openai import OpenAI


class AIAssistant:
    """Manages AI assistant functionality"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI assistant"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None
    
    def is_available(self) -> bool:
        """Check if AI assistant is available"""
        return self.client is not None
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate AI response to a prompt"""
        if not self.is_available():
            return "AI Assistant is not available. Please configure OPENAI_API_KEY."
        
        try:
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a multi-domain intelligence platform."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def analyze_data(self, data_description: str) -> Dict[str, Any]:
        """Analyze data and provide insights"""
        if not self.is_available():
            return {"error": "AI Assistant is not available"}
        
        prompt = f"Analyze the following data and provide insights: {data_description}"
        response = self.generate_response(prompt)
        return {"analysis": response}

