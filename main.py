from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from groq import Groq  # असली AI दिमाग के लिए

app = FastAPI(title="My Custom Advanced AI Engine")

# 🔴 अपनी Groq API Key यहाँ पेस्ट करें (जो आपने स्टेप 2 में बनाई थी)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

USER_DATABASE = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ImageRequest(BaseModel):
    user_id: str
    prompt: str

# 1. असली टेक्स्ट चैट (ChatGPT जैसा सोचने वाला दिमाग 🧠)
@app.post("/v1/chat")
async def chat_with_ai(request: ChatRequest):
    uid = request.user_id
    
    if uid not in USER_DATABASE:
        USER_DATABASE[uid] = {"history": [], "image_count": 0, "last_date": datetime.date.today()}
    
    # यूज़र का मैसेज याद रखें
    USER_DATABASE[uid]["history"].append({"role": "user", "content": request.message})
    
    try:
        # यहाँ हम दुनिया का सबसे तेज़ ओपन-सोर्स मॉडल (Llama-3.3-70b या DeepSeek) कॉल कर रहे हैं
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant like ChatGPT."},
                *USER_DATABASE[uid]["history"]
            ]
        )
        ai_response = completion.choices[0].message.content
    except Exception as e:
        ai_response = f"AI Error: API Key check karein ya internet check karein. Detail: {str(e)}"
    
    # AI का असली जवाब याद रखें
    USER_DATABASE[uid]["history"].append({"role": "assistant", "content": ai_response})
    
    return {"status": "success", "response": ai_response, "chat_history": USER_DATABASE[uid]["history"]}

# 2. असली इमेज जनरेशन (Flux Model के साथ 🎨)
@app.post("/v1/generate-image")
async def generate_ai_image(request: ImageRequest):
    uid = request.user_id
    today = date.today()
    
    if uid not in USER_DATABASE:
        USER_DATABASE[uid] = {"history": [], "image_count": 0, "last_date": today}
        
    if USER_DATABASE[uid]["last_date"] != today:
        USER_DATABASE[uid]["image_count"] = 0
        USER_DATABASE[uid]["last_date"] = today
        
    if USER_DATABASE[uid]["image_count"] >= 5:
        raise HTTPException(
            status_code=429, 
            detail="Daily free limit reached! Upgrade to Pro for unlimited images or pay ₹9 via UPI."
        )
        
    USER_DATABASE[uid]["image_count"] += 1
    
    # अब यह सीधे Hugging Face के Flux मॉडल का असली इमेज लिंक तैयार करेगा
    encoded_prompt = request.prompt.replace(" ", "%20")
    real_image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&model=flux"
    
    return {
        "status": "success", 
        "image_url": real_image_url, 
        "images_remaining": 5 - USER_DATABASE[uid]["image_count"]
    }
