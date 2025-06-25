#!/usr/bin/env python3
"""
Test Gemini API integratie
"""

import asyncio
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_gemini_integration():
    """Test de Gemini AI integratie"""
    
    logger.info("🤖 Testing Gemini AI Integration")
    logger.info("=" * 50)
    
    try:
        from app.services.ai_client import ai_client, generate_songtext_from_prompt
        
        # Check AI client status
        logger.info(f"✅ AI Client initialized")
        logger.info(f"🔑 Has Gemini key: {bool(ai_client.gemini_api_key)}")
        logger.info(f"🎯 Default provider: {ai_client.default_provider}")
        
        if not ai_client.gemini_api_key:
            logger.warning("⚠️ No Gemini API key found in environment")
            return
        
        # Test prompt
        test_prompt = """Schrijf een kort Nederlands liedje over vriendschap met de volgende elementen:

- Voor: Beste vriend Jan
- Van: Sarah  
- Thema: Vriendschap en dankbaarheid
- Beschrijving: Jan is altijd er voor me geweest, door dik en dun

Instructies:
- Schrijf in het Nederlands
- Maak het emotioneel en persoonlijk
- Gebruik een eenvoudige structuur: vers-refrein-vers-refrein
- Maximaal 8 regels per onderdeel"""

        logger.info(f"📝 Testing with prompt ({len(test_prompt)} chars)")
        logger.info("🔄 Generating songtext...")
        
        # Generate songtext
        result = await generate_songtext_from_prompt(
            test_prompt,
            provider="gemini",
            options={"temperature": 0.7, "max_tokens": 800}
        )
        
        if result["success"]:
            logger.info("🎉 SUCCESS! Gemini API is working!")
            logger.info(f"🤖 Provider: {result['provider']}")
            logger.info(f"📊 Songtext length: {len(result['songtext'])} characters")
            logger.info(f"⏰ Generated at: {result['generated_at']}")
            
            if result.get("is_dummy"):
                logger.warning("⚠️ This was a dummy response (API key might be invalid)")
            else:
                logger.info("✅ Real AI-generated content!")
            
            # Show songtext preview
            logger.info("\n" + "="*50)
            logger.info("🎵 GENERATED SONGTEXT:")
            logger.info("="*50)
            logger.info(result['songtext'])
            logger.info("="*50)
            
        else:
            logger.error(f"❌ Songtext generation failed: {result.get('error', 'Unknown error')}")
            logger.error(f"🤖 Provider: {result.get('provider', 'Unknown')}")
            
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 Make sure you've installed: pip install aiohttp==3.9.1")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")

async def test_api_health():
    """Test de API health endpoint"""
    
    logger.info("\n🌐 Testing API Health Endpoint")
    logger.info("=" * 50)
    
    try:
        import aiohttp
        import os
        
        base_url = "http://localhost:8000"
        api_key = os.getenv("API_KEY", "jouwsong2025")
        
        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{base_url}/api/ai/health", headers=headers, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info("✅ API Health check successful!")
                        logger.info(f"📊 Status: {data['status']}")
                        logger.info(f"🤖 Default provider: {data['default_provider']}")
                        logger.info(f"🔑 Has Gemini key: {data['has_gemini_key']}")
                        logger.info(f"🔑 Has OpenAI key: {data['has_openai_key']}")
                        logger.info(f"🔑 Has Claude key: {data['has_claude_key']}")
                    else:
                        logger.error(f"❌ API Health check failed: {response.status}")
            except asyncio.TimeoutError:
                logger.warning("⚠️ API server not running (timeout)")
                logger.info("💡 Start server with: uvicorn main:app --reload")
            except Exception as e:
                logger.warning(f"⚠️ Could not connect to API: {str(e)}")
                logger.info("💡 Make sure server is running on localhost:8000")
                
    except ImportError:
        logger.warning("⚠️ aiohttp not installed - skipping API test")
        logger.info("💡 Install with: pip install aiohttp==3.9.1")

async def main():
    """Main test function"""
    
    logger.info("🚀 Starting Gemini Integration Test")
    logger.info(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    # Test AI client
    await test_gemini_integration()
    
    # Test API (if server is running)
    await test_api_health()
    
    logger.info("\n✨ Gemini Integration Test Completed!")
    logger.info("\n💡 Next steps:")
    logger.info("1. If successful: Start server with 'uvicorn main:app --reload'")
    logger.info("2. Open frontend and test AI generation in Order Detail")
    logger.info("3. Try generating prompts and songteksten!")

if __name__ == "__main__":
    asyncio.run(main()) 