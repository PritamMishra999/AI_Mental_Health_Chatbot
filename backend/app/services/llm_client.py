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
    """Generate intelligent, conversational responses based on message content"""
    message_lower = user_message.lower()
    
    # PERFORMANCE ANXIETY (Presentations, interviews, meetings)
    if any(word in message_lower for word in ["presentation", "public speaking", "speak in front", "seminar"]):
        if "tomorrow" in message_lower or "upcoming" in message_lower or "next" in message_lower:
            return {
                "response": "I can tell you're anxious about an upcoming presentation - that's really common! Here's what can help: First, break your presentation into smaller chunks and practice each one. This builds confidence. Second, do the 4-7-8 breathing technique: inhale for 4 counts, hold for 7, exhale for 8. It calms your nervous system. Third, remember that your audience WANTS you to succeed - they're not there to judge you harshly. And here's a pro tip: practice in front of a mirror or record yourself. This removes the fear of the unknown. What aspect worries you most - forgetting content, stumbling over words, or something else?",
                "emotion": "Anxiety - Performance",
                "recommendation": "Practice multiple times, use 4-7-8 breathing technique before presenting, focus on key points only, remind yourself the audience wants you to succeed",
            }
        else:
            return {
                "response": "Public speaking anxiety is one of the most common fears - you're definitely not alone. The good news? It gets easier with practice. Here's my advice: 1) Know your material inside out - this builds genuine confidence. 2) Practice with a friend or family member. 3) Visualize yourself succeeding - see the audience laughing at your jokes or nodding in agreement. 4) Focus on your message, not on being perfect. Your authentic passion for your topic is more important than flawless delivery. Do you have a specific presentation coming up, or is this a general fear?",
                "emotion": "Anxiety - Performance",
                "recommendation": "Master your content, practice with friendly audience, visualize success, focus on message over perfection",
            }
    
    elif any(word in message_lower for word in ["interview", "job interview", "hiring", "hiring manager"]):
        return {
            "response": "Job interview anxiety is totally normal - you're evaluating each other, remember that! Here's what I suggest: First, research the company thoroughly so you feel prepared. Second, prepare 3-4 specific examples of challenges you've overcome (use the STAR method: Situation, Task, Action, Result). Third, practice common questions out loud - hearing your own answers makes them feel more natural. Fourth, remember they see hundreds of nervous candidates - a bit of nervousness actually makes you seem human and relatable. Here's a tip: ask them questions too! It shows genuine interest and shifts some focus off you. When is your interview?",
            "emotion": "Anxiety - Performance",
            "recommendation": "Research company thoroughly, prepare STAR examples, practice speaking out loud, ask them questions during interview, remember nervousness is normal",
        }
    
    elif any(word in message_lower for word in ["meeting with boss", "meeting", "supervisor", "manager"]):
        return {
            "response": "Meetings with authority figures can feel intimidating. Here's the reality: your manager likely feels nervous too in some situations. Here's my approach: 1) Write down your main points beforehand - this keeps you focused. 2) Practice saying them out loud so they flow naturally. 3) Remember you have value - you were hired for a reason! 4) If you get nervous, pause, take a breath, and continue. Pauses feel longer to you than they actually are. 5) After the meeting, acknowledge what went well - this builds confidence for next time. What's the meeting about? Sometimes understanding the context helps ease anxiety.",
            "emotion": "Anxiety - Performance",
            "recommendation": "Prepare talking points written down, practice speaking out loud, remember your value, take pauses when needed",
        }
    
    # WORK STRESS & OVERWHELM
    elif any(word in message_lower for word in ["work", "job", "boss", "workload", "deadline", "project", "deadline", "overwhelmed at work"]):
        if "too much" in message_lower or "overloaded" in message_lower or "too many" in message_lower:
            return {
                "response": "It sounds like you're drowning in work - that's a sign you need to set boundaries. Here's what actually works: First, list EVERYTHING you need to do. Just writing it down reduces mental load. Second, categorize by urgency and importance. Third, pick the top 3 things for TODAY - that's it. The rest can wait or can be delegated. Fourth, talk to your manager - they don't want you burnt out. Sometimes they don't realize the workload! Fifth, take actual breaks - a 10-minute walk resets your brain. Last tip: check emails only 2-3 times a day, not constantly. What's driving most of the workload right now?",
                "emotion": "Stress - Work Overwhelm",
                "recommendation": "Write down all tasks, prioritize top 3 for today, talk to manager about workload, take breaks, limit email checking to 2-3 times daily",
            }
        else:
            return {
                "response": "Work stress is one of the biggest sources of anxiety for people - and it makes sense. You spend a lot of time there! Here's my advice: First, create a clear separation between work and personal time. When work ends, it ends. Second, identify what specific aspect stresses you - is it the workload, coworkers, your boss, or lack of control? Third, for things you can control, take action. For things you can't, practice accepting them. Fourth, build stress-relief into your day: 5 minutes of deep breathing, a lunch walk, or exercise after work. These aren't luxuries - they're essential for your mental health. What's the biggest work stressor for you?",
                "emotion": "Stress - Work Related",
                "recommendation": "Set work-life boundaries, identify specific stressors, take action on controllable items, build daily stress-relief habits",
            }
    
    # ANXIETY (General)
    elif any(word in message_lower for word in ["anxious", "anxiety", "worried", "nervous", "worry", "worrying", "can't stop thinking"]):
        return {
            "response": "Anxiety thrives on worry - and once it starts, it's hard to stop. But here's the thing: anxiety is just your mind trying to protect you. It's usually wrong about the danger level. Here's what helps: The 5-4-3-2-1 grounding technique - name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. This anchors you in the present. Also: Write down your worries. Seriously. Research shows this reduces mental load. Then ask: Is this worry something I can control? If yes, make a plan. If no, consciously let it go. Finally, physical activity burns off anxiety chemicals. A 20-minute walk, yoga, or dancing works wonders. What are you worried about specifically?",
            "emotion": "Anxiety",
            "recommendation": "Use 5-4-3-2-1 grounding technique, write down worries, identify what you can control, physical exercise, meditation",
        }
    
    # SADNESS & DEPRESSION
    elif any(word in message_lower for word in ["sad", "depressed", "depression", "down", "hopeless", "empty", "numb", "nothing makes me happy"]):
        if "sleep" in message_lower or "can't sleep" in message_lower or "too much sleep" in message_lower:
            return {
                "response": "When you're sad, sleep often gets disrupted - either too much or too little. This creates a cycle because poor sleep makes everything worse. Here's what to try: First, stick to consistent sleep times - even weekends. Your body loves routine. Second, avoid screens 30 minutes before bed. The blue light messes with your sleep hormones. Third, if you're sleeping too much, set an alarm and force yourself up (I know it's hard!). Then, do something that requires movement - make breakfast, take a walk. Fourth, go outside in natural light, especially morning light. This resets your circadian rhythm. Fifth, move your body - exercise is as effective as some antidepressants. Just a 20-minute walk helps. How's your sleep been?",
                "emotion": "Sadness - Sleep Disrupted",
                "recommendation": "Consistent sleep schedule, no screens before bed, morning sunlight exposure, physical exercise, force yourself to move during the day",
            }
        elif "nothing matters" in message_lower or "no point" in message_lower or "harm" in message_lower:
            return {
                "response": "I hear deep pain in what you're saying, and I want you to know that these feelings, while real, can change with proper support. What you're feeling right now isn't permanent, even though it feels that way. Please reach out to someone: Call a counselor today, text a crisis line (Crisis Text Line: text HOME to 741741), or tell a trusted friend. These feelings are treatable. In this moment, try: Move your body - even 5 minutes of movement. Splash cold water on your face. Call someone you trust immediately. You deserve support. Are you safe right now? Is there someone you can reach out to?",
                "emotion": "Depression - Severe",
                "recommendation": "PLEASE reach out to counselor/crisis line (Crisis Text: HOME to 741741), tell trusted friend, move your body, you are not alone",
            }
        else:
            return {
                "response": "Sadness is your mind and body saying something needs to change. Here's the action plan: First, get outside. Just 15 minutes of sunlight and fresh air boosts mood chemicals. Second, do something that used to make you happy - even if it doesn't feel appealing right now. Your emotions catch up with your actions. Third, connect with someone. Text a friend, call family, or join a group. Loneliness amplifies sadness. Fourth, be gentle with yourself - you're going through something difficult. Fifth, if you've felt this way for weeks, consider talking to a counselor. This isn't weakness - it's wisdom. What used to bring you joy?",
                "emotion": "Sadness",
                "recommendation": "Get sunlight for 15+ minutes, reconnect with hobbies, reach out to people, be self-compassionate, consider professional support if lasting weeks",
            }
    
    # ANGER & FRUSTRATION
    elif any(word in message_lower for word in ["angry", "furious", "frustrated", "irritated", "fed up", "rage", "mad at"]):
        return {
            "response": "Anger is actually useful information - it's telling you something matters to you. The key is channeling it constructively. Right now: First, remove yourself from the triggering situation if possible. A 10-minute walk does wonders. Second, do intense physical activity - punch a pillow, do pushups, run. This burns off the adrenaline. Third, write an angry letter to the person (don't send it!) - this gets it out of your system. Fourth, when you're calmer, identify what specifically made you angry. What boundary was crossed? What value was violated? Fifth, decide if/how you'll address it. Sometimes the anger teaches you something about what you need. What triggered this anger?",
            "emotion": "Anger / Frustration",
            "recommendation": "Remove yourself temporarily, intense physical activity, write angry letter (don't send), identify root cause, address boundary when calm",
        }
    
    # LONELINESS & ISOLATION
    elif any(word in message_lower for word in ["lonely", "isolated", "alone", "no one", "nobody cares", "feel like an outsider"]):
        return {
            "response": "Loneliness is one of the worst feelings - and it's more common than you think. Here's how to break the cycle: First, reach out to ONE person today. Text, call, or message. Just one. Rejection is unlikely, and connection is healing. Second, join something - a class, group activity, online community for your interests. Shared activities remove the pressure of 'making friends.' Third, volunteer - helping others gives purpose AND builds connections. Fourth, be online in communities you care about - comment, engage, be seen. Fifth, consider that you might need professional support. A therapist gives you guaranteed connection and someone who's always in your corner. The loneliness you feel right now is changeable. What interests do you have? Are there communities around them you could join?",
            "emotion": "Loneliness",
            "recommendation": "Reach out to one person today, join interest-based group/activity, volunteer, engage in online communities, consider therapy",
        }
    
    # SELF-DOUBT & LOW CONFIDENCE
    elif any(word in message_lower for word in ["can't do it", "not good enough", "failure", "stupid", "loser", "weak", "pathetic", "hate myself"]):
        return {
            "response": "These thoughts are lies your brain is telling you - usually because you're stressed or tired. Here's the truth: Everyone has self-doubt. Even confident people. Here's how to fight back: First, write down evidence AGAINST these thoughts. You HAVE accomplished things - challenges you overcame, skills you learned, people who care about you. Look at this list when doubt hits. Second, treat yourself like you'd treat a good friend. Would you call them stupid? No. So don't do it to yourself. Third, identify the source: Are you tired? Hungry? Comparing yourself to others? Address it. Fourth, take action on something small you CAN do - make your bed, text a friend, take a walk. Success builds confidence. Fifth, ask for help. Competent people ask for help all the time. What's one thing you've successfully done, no matter how small?",
            "emotion": "Low Confidence / Self-Doubt",
            "recommendation": "Write evidence against negative thoughts, treat yourself with kindness, take one small actionable step, reach out for help, reconnect with past successes",
        }
    
    # POSITIVE & GRATITUDE
    elif any(word in message_lower for word in ["happy", "great", "excited", "good", "better", "grateful", "thankful", "amazing", "wonderful"]):
        return {
            "response": "This is wonderful to hear! Celebrating positive moments is important - they remind us life has good things. Here's how to amplify this feeling: First, acknowledge and savor this moment. What's contributing to it? Second, tell someone about it - sharing joy multiplies it. Third, identify what made this possible. Repeat those actions. Fourth, write it down - capturing good moments helps you access them later during tough times. Fifth, don't wait to feel this way for it to be real. These moments matter. Future you will thank you for remembering this feeling. What specifically is going well right now?",
            "emotion": "Positive / Grateful",
            "recommendation": "Savor this moment, share your joy, identify what created this, write it down, repeat positive actions, appreciate the good",
        }
    
    # GENERAL FALLBACK - More conversational
    else:
        return {
            "response": "Thank you for sharing that with me. I'm here to listen and help however I can. I might not fully understand yet - could you tell me a bit more? For example: How are you feeling emotionally right now - stressed, sad, angry, lonely, or something else? What's happened that brought this on? And most importantly - what would actually help you feel better? Sometimes in talking things through, answers start appearing. I'm genuinely here for this conversation.",
            "emotion": "Neutral",
            "recommendation": "Express your feelings more, consider root cause, identify what would actually help, talk it through with someone",
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
