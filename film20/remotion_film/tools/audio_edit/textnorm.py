"""Text normalisation shared by the aligner and film_build.py (no PocketSphinx import)."""
import re

SPOKEN = {  # number tokens as the narration speaks them (first variant is tried first)
    "3:05": ["three oh five"], "3:40": ["three forty"], "4:08": ["four oh eight"], "4:10": ["four ten"],
    "4:16": ["four sixteen"], "4:31": ["four thirty one"], "6:41": ["six forty one"], "11:31": ["eleven thirty one"],
    "12:52": ["twelve fifty two"], "2-14": ["two fourteen", "two one four"], "4471-b": ["forty four seventy one b", "four four seven one b"],
    "6b": ["six b"], "911": ["nine one one"], "2": ["two"],
}

def spoken(text: str, variant: int = 0) -> str:
    out = []
    for tok in text.split():
        core = tok.strip(".,;:!?\"'()").lower()
        out.append(SPOKEN[core][min(variant, len(SPOKEN[core]) - 1)] if core in SPOKEN else tok)
    return " ".join(out)

def norm(text: str) -> list[str]:
    import unicodedata
    text = "".join(ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch))
    t = text.lower().replace("’", "'").replace("—", " ").replace("-", " ")
    t = re.sub(r"[^a-z' ]", " ", t)
    return [w.strip("'") for w in t.split() if w.strip("'")]

