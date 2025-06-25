# 🚀 Render Deployment Guide - AI Integration

## 📋 **Pre-deployment Checklist**

### ✅ **1. Environment Variables Setup**
In je Render dashboard, ga naar je service settings en voeg toe:

```env
# AI API Keys (voeg alleen toe wat je hebt)
GEMINI_API_KEY=AIzaSyA5D7Rv1xRpnbLx-s-ZOrbl5jxGC75ZHWk
OPENAI_API_KEY=sk-...  # Optioneel
CLAUDE_API_KEY=sk-...  # Optioneel

# Bestaande environment variables
DATABASE_URL=postgresql://...
API_KEY=jouwsong2025
PLUGPAY_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
PLUGPAY_SECRET=plugpay_webhook_secret_2025
LOG_LEVEL=INFO
```

### ✅ **2. Dependencies Check**
Zorg dat `requirements.txt` deze packages bevat:
- `python-dotenv==1.1.1` ✅ (al toegevoegd)
- `requests>=2.31.0` ✅ (al beschikbaar)
- `fastapi`, `uvicorn`, etc. ✅ (al beschikbaar)

### ✅ **3. Health Check Update**
De AI health check is beschikbaar op: `/api/ai/health`

## 🔧 **Deployment Steps**

### **Stap 1: Push naar GitHub**
```bash
git add .
git commit -m "Add AI integration with Gemini support"
git push origin main
```

### **Stap 2: Render Environment Variables**
1. Ga naar je Render dashboard
2. Selecteer je `song-scribe-api-flow` service
3. Ga naar **Environment** tab
4. Voeg toe:
   - `GEMINI_API_KEY`: `AIzaSyA5D7Rv1xRpnbLx-s-ZOrbl5jxGC75ZHWk`
   - Andere AI keys indien beschikbaar

### **Stap 3: Deploy**
Render zal automatisch deployen na je GitHub push.

### **Stap 4: Test AI Endpoints**
Na deployment, test:
```bash
# Health check
curl https://jouwsong-api.onrender.com/api/ai/health

# Songtext generation (met je API key)
curl -X POST https://jouwsong-api.onrender.com/api/ai/generate-songtext \
  -H "Content-Type: application/json" \
  -H "X-API-Key: jouwsong2025" \
  -d '{
    "prompt": "Schrijf een kort Nederlands liedje over vriendschap",
    "provider": "gemini",
    "temperature": 0.7
  }'
```

## 🌐 **Vercel (Frontend) Configuratie**

### **Environment Variables voor Vercel:**
```env
# Deze zijn waarschijnlijk al ingesteld
VITE_API_URL=https://jouwsong-api.onrender.com
VITE_API_KEY=jouwsong2025
```

### **Deployment Check:**
1. Zorg dat je frontend build succesvol is:
   ```bash
   npm run build
   ```

2. Test lokaal met productie API:
   ```bash
   # In .env.local (tijdelijk voor test)
   VITE_API_URL=https://jouwsong-api.onrender.com
   npm run dev
   ```

## 🚨 **Troubleshooting**

### **AI Endpoints niet beschikbaar?**
- Check Render logs: `https://dashboard.render.com/`
- Verify environment variables zijn correct ingesteld
- Test health endpoint: `/api/ai/health`

### **"No API key" errors?**
- Controleer dat `GEMINI_API_KEY` correct is ingesteld in Render
- Check dat de key geldig is en quota heeft

### **Frontend kan AI niet bereiken?**
- Verify `VITE_API_URL` wijst naar je Render URL
- Check CORS settings in `main.py`
- Test AI endpoints direct met curl/Postman

## ✨ **Success Indicators**

Je AI integratie werkt als:
- ✅ `/api/ai/health` returns `{"status": "healthy"}`
- ✅ Frontend toont AI Generation card
- ✅ Songtext generation werkt in Order Detail pages
- ✅ Geen "aiohttp" errors in logs (gebruikt requests fallback)

## 🎯 **Next Steps After Deployment**

1. **Test in productie**: Ga naar een Order Detail page en test AI generatie
2. **Monitor usage**: Check je Gemini API quota/billing
3. **Add more providers**: Voeg OpenAI/Claude keys toe indien gewenst
4. **Performance monitoring**: Monitor response times en error rates

---

**🎉 Je AI-powered Song Scribe is nu live in productie!** 