# app/services/ai_service.py

import openai
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class AIService:
    """Service for AI-powered features using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    def is_available(self) -> bool:
        """Check if AI service is available."""
        return self.api_key is not None and self.api_key != ""
    
    def get_security_advice(self, incident_summary: str) -> str:
        """Get AI-generated security advice for an incident."""
        if not self.is_available():
            return "⚠️ OpenAI API key not configured."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert. Provide concise, actionable security advice."},
                    {"role": "user", "content": f"Provide security advice for this incident: {incident_summary}"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def analyze_data_trend(self, domain: str, data_summary: str) -> str:
        """Analyze data trends using AI."""
        if not self.is_available():
            return "⚠️ OpenAI API key not configured."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data science analyst. Provide insights about data trends."},
                    {"role": "user", "content": f"Analyze trends in {domain}: {data_summary}"}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def chat(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Chat with AI assistant."""
        if not self.is_available():
            return "⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        try:
            system_prompt = "You are an AI assistant for the Intelligence Platform. Help users with cybersecurity, IT operations, and data science questions."
            if context:
                context_str = f"\n\nCurrent context: {context}"
                system_prompt += context_str
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error: {str(e)}"


# Singleton instance
_ai_service_instance = None

def get_ai_service() -> AIService:
    """Get singleton AI service instance."""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance


