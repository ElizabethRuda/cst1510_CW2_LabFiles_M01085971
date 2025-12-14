"""
AI Service for OpenAI API Integration
Week 10 Requirement: AI Assistant Feature
"""

import os
import openai
from typing import Optional, Dict, Any


class AIService:
    """Service class for interacting with OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Service with API key.
        
        Args:
            api_key: OpenAI API key. If None, tries to get from environment.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        else:
            self.api_key = None
    
    def is_available(self) -> bool:
        """Check if API key is configured."""
        return self.api_key is not None
    
    def get_security_advice(self, incident_type: str, severity: str, context: str = "") -> str:
        """
        Get AI-generated security advice for a cyber incident.
        
        Args:
            incident_type: Type of incident (e.g., "Phishing", "Malware")
            severity: Severity level (e.g., "Critical", "High")
            context: Additional context about the incident
            
        Returns:
            AI-generated security advice
        """
        if not self.is_available():
            return "⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        try:
            prompt = f"""As a cybersecurity expert, provide brief, actionable advice for handling a {severity} severity {incident_type} incident.
            
Context: {context if context else "No additional context provided."}

Provide 3-5 specific, actionable recommendations. Keep response under 200 words."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert providing concise, actionable security advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"❌ Error getting AI advice: {str(e)}"
    
    def analyze_data_trend(self, domain: str, data_summary: str) -> str:
        """
        Get AI analysis of data trends.
        
        Args:
            domain: Domain name (e.g., "Cybersecurity", "IT Operations")
            data_summary: Summary of data to analyze
            
        Returns:
            AI-generated analysis
        """
        if not self.is_available():
            return "⚠️ OpenAI API key not configured."
        
        try:
            prompt = f"""As a data analyst, analyze the following {domain} data and provide insights:
            
{data_summary}

Provide 3-5 key insights and recommendations. Keep response under 200 words."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data analyst providing insights and recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"❌ Error in AI analysis: {str(e)}"
    
    def chat(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        General chat function for AI Assistant.
        
        Args:
            user_message: User's question or message
            context: Optional context dictionary with domain information
            
        Returns:
            AI response
        """
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
    """Get or create AI service instance."""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance

