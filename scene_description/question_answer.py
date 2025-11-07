import re
import cv2
import numpy as np
from collections import Counter

# --- Simple intent parsing ---
INTENTS = {
    "presence": [
        r"\bis there (?:a|an|any)\s+(?P<obj>\w+)",
        r"\bdo you see (?:a|an|any)?\s*(?P<obj>\w+)"
    ],
    "count": [
        r"\bhow many\s+(?P<obj>\w+)",
        r"\bcount\s+(?P<obj>\w+)"
    ],
    "where": [
        r"\bwhere is\s+(?P<obj>\w+)",
        r"\blocation of\s+(?P<obj>\w+)"
    ],
    "center": [
        r"\bwhat (?:is|’s|'s) (?:in|at) the center",
        r"\bwhat (?:is|’s|'s) in the middle"
    ],
    "list": [
        r"\bwhat do you see\b",
        r"\bwhat objects\b",
    ],
    "color": [
        r"\bwhat (?:color|colour) (?:is|of)?\s+(?:the\s+)?(?P<obj>\w+)"
    ],
}

# --- Synonym mapping for flexibility ---
SYNONYMS = {
    "person": ["man", "woman", "people", "person"],
    "bottle": ["bottle", "water bottle", "drink", "flask"],
    "chair": ["chair", "seat"],
    "laptop": ["laptop", "computer", "pc"],
    "desk": ["desk", "table"],
    "board": ["board", "whiteboard", "blackboard"],
}

def parse_intent(q: str):
    ql = q.lower().strip()
    for intent, patterns in INTENTS.items():
        for pat in patterns:
            m = re.search(pat, ql)
            if m:
                return intent, m.groupdict()
    return None, {}

# --- Color util (dominant hue in bbox) ---
def dominant_color_bgr(img, x1, y1, x2, y2):
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    crop = img[max(0,y1):max(0,y2), max(0,x1):max(0,x2)]
    if crop.size == 0:
        return "unknown"
    crop_small = cv2.resize(crop, (64, 64), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(crop_small, cv2.COLOR_BGR2HSV)
    hues = hsv[:,:,0].reshape(-1)
    def hue_to_name(h):
        if h < 10 or h >= 170: return "red"
        if h < 25: return "orange"
        if h < 35: return "yellow"
        if h < 85: return "green"
        if h < 125: return "blue"
        if h < 150: return "purple"
        return "pink"
    names = [hue_to_name(int(h)) for h in hues]
    common = Counter(names).most_common(1)
    return common[0][0] if common else "unknown"

def expand_synonyms(word):
    for key, vals in SYNONYMS.items():
        if word in vals:
            return vals
    return [word]

def answer_question(question: str, scene_state: list, image_bgr=None):
    intent, slots = parse_intent(question)
    labels = [d["label"].lower() for d in scene_state]

    if intent is None:
        return "Please rephrase the question about what you see."

    def matches(obj_name, lbl):
        synonyms = expand_synonyms(obj_name)
        return any(s in lbl for s in synonyms)

    if intent == "list":
        if not scene_state:
            return "I don't see any known objects."
        uniq = sorted(set(labels))
        return "I can see: " + ", ".join(uniq) + "."

    if intent == "center":
        center_objs = [d["label"] for d in scene_state if d["region"] == "center"]
        if center_objs:
            return "In the center: " + ", ".join(sorted(set(center_objs))) + "."
        return "Nothing notable in the center region."

    if intent in ("presence", "count", "where", "color"):
        obj = slots.get("obj", "").strip()
        if not obj:
            return "Which object are you asking about?"

        hits = [d for d in scene_state if matches(obj, d["label"])]

        if intent == "presence":
            return f"Yes, I see {obj}." if hits else f"No, I don't see {obj}."

        if intent == "count":
            return f"I see {len(hits)} {obj}{'s' if len(hits)>1 else ''}." if hits else f"I don't see any {obj}s."

        if intent == "where":
            if not hits:
                return f"I don't see {obj}."
            best = max(hits, key=lambda d: d["conf"])
            reg = best["region"]
            if reg == "center":
                return f"The {obj} is in the center."
            elif reg == "left":
                return f"The {obj} is on the left. Please move right to center it."
            else:
                return f"The {obj} is on the right. Please move left to center it."

        if intent == "color":
            if not hits:
                return f"I don't see {obj}."
            if image_bgr is None:
                return "I need the image to determine color."
            best = max(hits, key=lambda d: d["conf"])
            x1, y1, x2, y2 = best["bbox"]
            col = dominant_color_bgr(image_bgr, x1, y1, x2, y2)
            return f"The {obj} looks {col}."
    return "I'm not sure how to answer that yet."
