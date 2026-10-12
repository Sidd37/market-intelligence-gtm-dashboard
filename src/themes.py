"""Keyword theme detection on three text groups. Mirrored exactly by the Excel formulas.
Normalisation: lower-case, replace punctuation with spaces (no collapsing), pad with spaces.
Match "word" = whole word; "prefix" = word starts with the keyword."""

PUNCT = "-.,:;!?'\"’—/()&+"

GROUPS = {
    "positioning": {
        "title": "Positioning themes (homepage headline + subheadline)",
        "columns": ["positioning_h1", "positioning_sub"],
        "keywords": [
            ("AI-led", "ai", "word"), ("AI-led", "agent", "prefix"),
            ("Engineering craft", "engineering", "word"), ("Engineering craft", "engineers", "word"),
            ("Speed & agility", "agile", "word"), ("Speed & agility", "speed", "word"), ("Speed & agility", "faster", "word"),
            ("Scale & security", "scal", "prefix"), ("Scale & security", "secure", "prefix"),
            ("Business growth", "growth", "word"), ("Business growth", "business", "word"),
            ("Vertical focus", "healthcare", "word"), ("Vertical focus", "commerce", "word"), ("Vertical focus", "fintech", "word"),
            ("Product / digital", "product", "prefix"), ("Product / digital", "digital", "word"),
            ("Credibility claim", "#1", "prefix"), ("Credibility claim", "fortune 500", "prefix"), ("Credibility claim", "top 1", "prefix"),
        ],
    },
    "cta": {
        "title": "Lead-capture CTAs (primary calls to action on the homepage)",
        "columns": ["primary_ctas"],
        "keywords": [
            ("Book a call / consult", "call", "word"), ("Book a call / consult", "consult", "prefix"),
            ("Book a call / consult", "discovery", "word"), ("Book a call / consult", "intro", "word"),
            ("Get a quote / estimate", "quote", "word"), ("Get a quote / estimate", "estimate", "prefix"),
            ("Hire talent", "hire", "word"),
            ("Generic contact", "contact", "word"), ("Generic contact", "get in touch", "prefix"),
            ("NDA-first trust", "nda", "word"),
            ("Show proof", "portfolio", "word"), ("Show proof", "case stud", "prefix"),
            ("Show proof", "client work", "prefix"), ("Show proof", "review", "word"),
            ("Event / webinar", "register", "word"),
        ],
    },
    "engagement": {
        "title": "Engagement models named on the homepage",
        "columns": ["engagement_models"],
        "keywords": [
            ("Fixed price", "fixed", "word"),
            ("Hourly / T&M", "hourly", "word"),
            ("Dedicated team", "dedicated", "word"),
            ("Staff augmentation", "staff augmentation", "prefix"), ("Staff augmentation", "team extension", "prefix"),
            ("Outcome-based", "outcome", "prefix"),
            ("Outsourcing / offshore", "outsourcing", "word"), ("Outsourcing / offshore", "offshore", "word"),
            ("Outsourcing / offshore", "nearshore", "word"),
            ("Managed services", "managed", "word"),
        ],
    },
}


def theme_names(group):
    return list(dict.fromkeys(t for t, _, _ in GROUPS[group]["keywords"]))


def normalize(text):
    s = "" if text is None else str(text).lower()
    if s == "nan":
        s = ""
    for ch in PUNCT:
        s = s.replace(ch, " ")
    return " " + s + " "


def needle(keyword, match):
    return " " + keyword + (" " if match == "word" else "")


def theme_hits(group, text):
    s = normalize(text)
    out = {t: 0 for t in theme_names(group)}
    for t, kw, m in GROUPS[group]["keywords"]:
        if kw and needle(kw, m) in s:
            out[t] += 1
    return out
