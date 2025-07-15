#!/usr/bin/env python3
"""
Direct test van AI client om te zien waarom we dummy responses krijgen
"""

import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_client import AIClient, AIProvider

# Load environment variables
load_dotenv()

async def test_ai_client():
    """Test de AI client direct"""
    
    client = AIClient()
    
    print("🔍 AI Client Status:")
    print(f"OpenAI API Key: {'✅ Set' if client.openai_api_key else '❌ Not set'}")
    print(f"Claude API Key: {'✅ Set' if client.claude_api_key else '❌ Not set'}")
    print(f"Gemini API Key: {'✅ Set' if client.gemini_api_key else '❌ Not set'}")
    print(f"Default Provider: {client.default_provider}")
    print()
    
    # Test of we API keys hebben
    print("🔍 API Key Detection:")
    print(f"Has OpenAI key: {client._has_api_key(AIProvider.OPENAI)}")
    print(f"Has Claude key: {client._has_api_key(AIProvider.CLAUDE)}")
    print(f"Has Gemini key: {client._has_api_key(AIProvider.GEMINI)}")
    print()
    
    # Test met een simpele prompt
    test_prompt = "Schrijf een kort Nederlands liedje over Francis, een geweldige vriendin."
    
    print("🎵 Testing AI Generation...")
    print(f"Test prompt: {test_prompt}")
    print()
    
    # Test met alle providers
    providers = [AIProvider.GEMINI, AIProvider.OPENAI, AIProvider.CLAUDE]
    
    for provider in providers:
        if client._has_api_key(provider):
            print(f"📡 Testing {provider.value}...")
            try:
                result = await client.generate_songtext(
                    prompt=test_prompt,
                    provider=provider,
                    max_tokens=500,
                    temperature=0.7
                )
                
                print(f"✅ Success: {result.get('success')}")
                print(f"Provider: {result.get('provider')}")
                print(f"Is Dummy: {result.get('is_dummy', False)}")
                
                if result.get('success'):
                    songtext = result.get('songtext', '')
                    print(f"Response length: {len(songtext)} characters")
                    print(f"First 200 chars: {songtext[:200]}...")
                else:
                    print(f"Error: {result.get('error')}")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
                
            print("-" * 50)
        else:
            print(f"⏭️ Skipping {provider.value} (no API key)")
    
    print("\n🔍 Environment Check:")
    print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')[:15]}..." if os.getenv('GEMINI_API_KEY') else "Not set")
    print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')[:15]}..." if os.getenv('OPENAI_API_KEY') else "Not set")
    print(f"CLAUDE_API_KEY: {os.getenv('CLAUDE_API_KEY')[:15]}..." if os.getenv('CLAUDE_API_KEY') else "Not set")

if __name__ == "__main__":
    asyncio.run(test_ai_client()) 