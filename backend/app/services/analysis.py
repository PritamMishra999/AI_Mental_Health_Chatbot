import re


def estimate_stress_score(message: str) -> int:
    indicators = [
        "anxious",
        "stressed",
        "overwhelmed",
        "worried",
        "panic",
        "tired",
        "unable",
        "pressure",
    ]
    score = 0
    text = message.lower()
    for indicator in indicators:
        if indicator in text:
            score += 2

    score += min(len(re.findall(r"!", text)), 3)
    score += len(re.findall(r"\b(can't|cannot|never|always|worst)\b", text))
    return min(max(score, 1), 10)


def detect_emotion(message: str) -> str:
    lower = message.lower()
    if any(word in lower for word in ["sad", "down", "hopeless", "depressed"]):
        return "Sadness"
    if any(word in lower for word in ["angry", "frustrated", "irritated"]):
        return "Frustration"
    if any(word in lower for word in ["anxious", "nervous", "panic", "worried"]):
        return "Anxiety"
    if any(word in lower for word in ["happy", "grateful", "relieved"]):
        return "Positive"
    return "Neutral"
