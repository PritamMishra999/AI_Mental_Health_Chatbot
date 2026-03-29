import json
from typing import Dict
import os

from ..config import settings


def parse_chat_response(content: str) -> Dict[str, str]:
    try:
        payload = json.loads(content)
        return {
            "response": payload.get("response", content),
            "emotion": payload.get("emotion", "Neutral"),
            "recommendation": payload.get("recommendation", "Try a few calming breaths and reach out to someone you trust."),
        }
    except json.JSONDecodeError:
        return {
            "response": content,
            "emotion": "Neutral",
            "recommendation": "Try a few calming breaths and reach out to someone you trust.",
        }


def get_intelligent_response(user_message: str) -> Dict[str, str]:
    """Generate intelligent responses based on message content with suggestions"""
    message_lower = user_message.lower()
    
    # Anxiety/Stress topics
    if any(word in message_lower for word in ["anxious", "anxiety", "worried", "nervous", "stressed", "pressure", "overwhelmed"]):
        if "presentation" in message_lower or "meeting" in message_lower or "interview" in message_lower:
            return {
                "response": "That sounds like you're dealing with performance anxiety. It's completely normal to feel nervous before important presentations or meetings. Here's what might help: First, practice your presentation multiple times to build confidence. Deep breathing exercises (try 4-7-8 breathing) before the event can calm your nerves. Remember, most people are focused on their own concerns, not judging you. You've got this!",
                "emotion": "Anxiety",
                "recommendation": "Practice deep breathing (4-7-8 technique), prepare thoroughly, talk to a trusted friend about it",
            }
        elif "work" in message_lower or "job" in message_lower or "boss" in message_lower:
            return {
                "response": "Work stress can be really overwhelming. It might help to: 1) Break big tasks into smaller steps, 2) Set realistic daily goals, 3) Take short breaks to recharge, 4) Talk with your manager about workload if needed. Remember, your worth isn't defined by your productivity. What's one thing you could tackle first?",
                "emotion": "Stress",
                "recommendation": "Take regular breaks, prioritize tasks, discuss concerns with your manager, exercise daily",
            }
        else:
            return {
                "response": "I hear that you're feeling anxious. Anxiety is your mind trying to protect you, but sometimes it works overtime. Some grounding techniques that help: 5-4-3-2-1 method (notice 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste). Also, physical activity, even a 10-minute walk, can significantly reduce anxiety. What's the main trigger right now?",
                "emotion": "Anxiety",
                "recommendation": "Try grounding techniques, physical exercise, meditation, journaling",
            }
    
    # Sadness/Depression
    elif any(word in message_lower for word in ["sad", "depressed", "empty", "hopeless", "down", "blue", "lonely", "alone"]):
        if "family" in message_lower or "friend" in message_lower or "relationship" in message_lower:
            return {
                "response": "Relationship challenges can feel really isolating. Remember that feeling disconnected is temporary and fixable. Have you considered: 1) Having an honest conversation with the person, 2) Spending time with other supportive people, 3) Engaging in activities you enjoy? Sometimes taking a break and coming back helps. Reaching out (like you're doing now) is actually a positive step.",
                "emotion": "Sadness",
                "recommendation": "Communicate openly, spend time with supportive people, engage in hobbies you love, consider talking to someone",
            }
        else:
            return {
                "response": "I'm sorry you're feeling sad. That takes courage to share. What might help: 1) Get outside for sunlight and fresh air, 2) Do something physical (walk, dance, sport), 3) Reach out to someone you trust, 4) Do something you usually enjoy, even if it feels small. Sadness is often temporary. What's one small thing that usually makes you feel better?",
                "emotion": "Sadness",
                "recommendation": "Get sunlight, move your body, reach out to loved ones, engage in favorite activities",
            }
    
    # Anger/Frustration
    elif any(word in message_lower for word in ["angry", "irritated", "furious", "frustrated", "annoyed", "mad"]):
        return {
            "response": "Anger is a signal that something matters to you. Before acting on it, try: 1) Take 5-10 deep breaths, 2) Remove yourself from the situation temporarily, 3) Exercise or physical activity, 4) Write down why you're angry without filtering. Once you're calmer, you can address the issue more effectively. What triggered this feeling?",
            "emotion": "Anger",
            "recommendation": "Take deep breaths, exercise, step away, journal about it, then address the root cause",
        }
    
    # Loneliness
    elif any(word in message_lower for word in ["lonely", "isolated", "nobody", "no one", "nobody understands"]):
        return {
            "response": "Loneliness is painful, but remember you're not truly alone. Many people feel this way. You could: 1) Reach out to one person today (even a text), 2) Join a group activity (hobby, gym, class), 3) Volunteer (helps others + builds connection), 4) Try online communities with shared interests. Small connections matter. What's one person you could reach out to?",
            "emotion": "Loneliness",
            "recommendation": "Reach out to someone, join a group or activity, volunteer, engage in online communities",
        }
    
    # Confidence/Self-doubt
    elif any(word in message_lower for word in ["can't", "not good enough", "failure", "unable", "inadequate", "stupid", "dummy", "loser"]):
        return {
            "response": "These negative thoughts are lying to you. Everyone doubts themselves sometimes - it's human. Try: 1) Write down evidence against these thoughts, 2) Ask friends what they think of you, 3) Remember past successes, 4) Practice self-compassion like you'd give a friend. You're capable of more than you think. What's one thing you've accomplished that you're proud of?",
            "emotion": "Low Confidence",
            "recommendation": "Practice self-compassion, recall past successes, challenge negative thoughts with evidence, reach out for support",
        }
    
    # Gratitude/Positive
    elif any(word in message_lower for word in ["happy", "great", "excited", "good", "better", "grateful", "wonderful", "amazing"]):
        return {
            "response": "That's wonderful to hear! Positive emotions are important to celebrate. Keep riding this wave by: 1) Sharing your happiness with others, 2) Journaling about what made you feel this way, 3) Doing more of what's working. You're doing great! What's contributing most to feeling this way?",
            "emotion": "Positive",
            "recommendation": "Share your positivity with others, journal about it, continue what's working",
        }
    
    # General catchall with better advice
    else:
        return {
            "response": "I appreciate you sharing that with me. It sounds like there's something on your mind. To help you better, tell me more - are you feeling stressed, sad, anxious, or something else? What would make you feel better right now? Remember, talking about it (like you're doing) is already a helpful step forward.",
            "emotion": "Neutral",
            "recommendation": "Take a moment to reflect, talk to someone you trust, practice self-care, consider professional support if needed",
        }


def create_chat_response(user_message: str) -> Dict[str, str]:
    """Create chat response using OpenAI API or intelligent fallback"""
    if not user_message or not user_message.strip():
        return {
            "response": "Hello! I'm here to listen and support you. What's on your mind today?",
            "emotion": "Neutral",
            "recommendation": "Share what you're feeling or thinking about.",
        }
    
    try:
        # Try OpenAI first
        import os
        os.environ.pop('http_proxy', None)
        os.environ.pop('https_proxy', None)
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)
        
        from openai import OpenAI
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        prompt = (
            "You are a compassionate mental health coach. Respond with empathy, understanding, and practical suggestions. "
            "Return a JSON object with: emotion (detected emotion), response (supportive message with actionable advice), "
            "recommendation (specific wellness actions). Keep responses warm and conversational.\n\n"
            f"User: {user_message}\n\n"
            "Your response as JSON:"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a compassionate mental health coach who provides emotional support and practical wellness advice."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.75,
            max_tokens=320,
        )

        text = response.choices[0].message.content.strip()
        return parse_chat_response(text)
    except Exception as e:
        # Use intelligent fallback if OpenAI fails
        print(f"Using intelligent fallback (OpenAI error: {str(e)[:50]})")
        return get_intelligent_response(user_message)
