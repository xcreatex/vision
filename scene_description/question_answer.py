# import re
# import cv2
# import numpy as np
# from collections import Counter

# # -------------------------------------------------------------------
# # 🧠 Intent Patterns (Natural Q&A)
# # -------------------------------------------------------------------
# INTENTS = {
#     "presence": [
#         r"\bis there (?:a|an|any)?\s*(?P<obj>[a-z\s]+)",
#         r"\bdo you see (?:a|an|any)?\s*(?P<obj>[a-z\s]+)"
#     ],
#     "count": [
#         r"\bhow many\s+(?P<obj>[a-z\s]+)",
#         r"\bcount\s+(?P<obj>[a-z\s]+)"
#     ],
#     "where": [
#         r"\bwhere is\s+(?:the|a|an)?\s*(?P<obj>[a-z\s]+)",
#         r"\blocation of\s+(?:the|a|an)?\s*(?P<obj>[a-z\s]+)"
#     ],
#     "center": [
#         r"\bwhat (?:is|’s|'s) (?:in|at) the center",
#         r"\bwhat (?:is|’s|'s) in the middle"
#     ],
#     "list": [
#         r"\bwhat do you see\b",
#         r"\bwhat objects\b",
#         r"\bwhat can you see\b",
#         r"\bwhat is visible\b"
#     ],
#     "color": [
#         r"\bwhat color is\s+(?:the|a|an)?\s*(?P<obj>[a-z\s]+)",
#         r"\bwhat colour is\s+(?:the|a|an)?\s*(?P<obj>[a-z\s]+)",
#         r"\bwhat color\s+(?:of|does)?\s*(?:the|a|an)?\s*(?P<obj>[a-z\s]+)",
#         r"\bwhat colour\s+(?:of|does)?\s*(?:the|a|an)?\s*(?P<obj>[a-z\s]+)",
#         r"\bdescribe (?:the|a|an)?\s*(?P<obj>[a-z\s]+)\s*color"
#     ],
# }

# # -------------------------------------------------------------------
# # 🔍 Intent Parser
# # -------------------------------------------------------------------
# def parse_intent(question: str):
#     """Parse natural question to detect intent and object keyword."""
#     ql = question.lower().strip()
#     for intent, patterns in INTENTS.items():
#         for pat in patterns:
#             m = re.search(pat, ql, re.IGNORECASE)
#             if m:
#                 obj = m.groupdict().get("obj", "").strip()
#                 obj = obj.replace("  ", " ")
#                 return intent, {"obj": obj}
#     return None, {}

# # -------------------------------------------------------------------
# # 🎨 Color Analysis
# # -------------------------------------------------------------------
# def dominant_color_bgr(img, x1, y1, x2, y2):
#     """Find dominant hue color in an image region (rough mapping)."""
#     x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
#     crop = img[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]
#     if crop.size == 0:
#         return "unknown"

#     crop_small = cv2.resize(crop, (64, 64), interpolation=cv2.INTER_AREA)
#     hsv = cv2.cvtColor(crop_small, cv2.COLOR_BGR2HSV)
#     hues = hsv[:, :, 0].reshape(-1)

#     def hue_to_name(h):
#         if h < 10 or h >= 170: return "red"
#         if h < 25: return "orange"
#         if h < 35: return "yellow"
#         if h < 85: return "green"
#         if h < 125: return "blue"
#         if h < 150: return "purple"
#         return "pink"

#     names = [hue_to_name(int(h)) for h in hues]
#     common = Counter(names).most_common(1)
#     return common[0][0] if common else "unknown"

# # -------------------------------------------------------------------
# # 🧠 Question Answer Engine
# # -------------------------------------------------------------------
# def answer_question(question: str, scene_state: list, image_bgr=None):
#     """
#     Responds to a natural question about detected scene objects.
#     scene_state = list of dicts: {label, conf, region, bbox(x1,y1,x2,y2)}
#     """
#     intent, slots = parse_intent(question)
#     labels = [d["label"] for d in scene_state]

#     if intent is None:
#         return "Sorry, I couldn't understand your question."

#     # Utility for label matching (handles plurals)
#     def matches(obj_name, lbl):
#         obj_name = obj_name.lower().strip()
#         lbl = lbl.lower().strip()
#         return obj_name in lbl or lbl in obj_name or (
#             obj_name.endswith("s") and obj_name[:-1] in lbl
#         )

#     # ---- Handle listing intents ----
#     if intent == "list":
#         if not scene_state:
#             return "I don't see any known objects."
#         uniq = sorted(set(labels))
#         return "I can see: " + ", ".join(uniq) + "."

#     # ---- Handle center region ----
#     if intent == "center":
#         center_objs = [d["label"] for d in scene_state if d["region"] == "center"]
#         if center_objs:
#             return "In the center: " + ", ".join(sorted(set(center_objs))) + "."
#         return "Nothing notable in the center region."

#     # ---- Specific object queries ----
#     if intent in ("presence", "count", "where", "color"):
#         obj = slots.get("obj", "").strip()
#         if not obj:
#             return "Which object are you asking about?"

#         hits = [d for d in scene_state if matches(obj, d["label"])]

#         # Presence
#         if intent == "presence":
#             return f"Yes, I see {obj}." if hits else f"No, I don't see {obj}."

#         # Count
#         if intent == "count":
#             if hits:
#                 num = len(hits)
#                 plural = "s" if num > 1 else ""
#                 return f"I see {num} {obj}{plural}."
#             return f"I don't see any {obj}s."

#         # Location
#         if intent == "where":
#             if not hits:
#                 return f"I don't see {obj}."
#             best = max(hits, key=lambda d: d["conf"])
#             reg = best["region"]
#             if reg == "center":
#                 return f"The {obj} is in the center."
#             elif reg == "left":
#                 return f"The {obj} is on the left. Please move right to center it."
#             else:
#                 return f"The {obj} is on the right. Please move left to center it."

#         # Color
#         if intent == "color":
#             if not hits:
#                 return f"I don't see {obj}."
#             if image_bgr is None:
#                 return "I need the image to determine color."
#             best = max(hits, key=lambda d: d["conf"])
#             x1, y1, x2, y2 = best["bbox"]
#             col = dominant_color_bgr(image_bgr, x1, y1, x2, y2)
#             return f"The {obj} looks {col}."

#     # ---- Default fallback ----
#     return "I'm not sure how to answer that yet."

# scene_description/question_answer.py
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
        r"\bwhat color is\s+(?P<obj>\w+)",
        r"\bwhat color is it\b",
        r"\bcolor of\s+(?P<obj>\w+)",
        r"\bcolor of it\b"
    ],
}

# Store last mentioned object for follow-ups
LAST_OBJECT = None

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
    crop = img[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]
    if crop.size == 0:
        return "unknown"
    crop_small = cv2.resize(crop, (64, 64), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(crop_small, cv2.COLOR_BGR2HSV)
    hues = hsv[:, :, 0].reshape(-1)
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


def answer_question(question: str, scene_state: list, image_bgr=None):
    global LAST_OBJECT
    intent, slots = parse_intent(question)
    labels = [d["label"] for d in scene_state]

    if intent is None:
        return "Please rephrase the question about what you see."

    # Extract object
    obj = slots.get("obj", "").strip()
    if not obj and LAST_OBJECT:
        obj = LAST_OBJECT  # fallback to remembered object

    # Remember object for follow-ups
    if obj:
        LAST_OBJECT = obj

    # --- Helper function ---
    def matches(obj_name, lbl):
        return obj_name in lbl or (obj_name.endswith('s') and obj_name[:-1] in lbl)

    # --- Intent Handling ---
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
        if not obj:
            return "Which object are you referring to?"

        hits = [d for d in scene_state if matches(obj, d["label"])]

        if intent == "presence":
            return f"Yes, I see {obj}." if hits else f"No, I don't see {obj}."

        if intent == "count":
            if hits:
                num = len(hits)
                base = obj if obj.endswith("s") else obj + ("s" if num > 1 else "")
                return f"I see {num} {base}."
            return f"I don't see any {obj}s."

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

    # Fallback
    return "I'm not sure how to answer that yet."
