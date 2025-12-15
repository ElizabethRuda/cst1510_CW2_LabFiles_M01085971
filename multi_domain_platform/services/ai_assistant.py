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
            # Build system message with platform context
            system_message = (
                "You are a helpful AI assistant for a Multi-Domain "
                "Intelligence Platform. The platform manages three domains: "
                "1. Cybersecurity - security incident tracking and analysis, "
                "2. Data Science - dataset management and analytics, "
                "3. IT Operations - IT support ticket management. "
                "When users ask questions about the platform data, use the "
                "provided context information to give accurate answers based "
                "on the actual data in the platform. Always answer in "
                "English. If the context contains specific numbers or "
                "statistics, use them in your answer. If you don't have "
                "specific data in the context, acknowledge that and provide "
                "general guidance."
            )
            
            full_prompt = prompt
            if context:
                full_prompt = f"Platform Data Context:\n{context}\n\nUser Question: {prompt}\n\nPlease answer based on the platform data context provided above."
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
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


