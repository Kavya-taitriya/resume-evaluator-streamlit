import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    return set(token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop)

def evaluate_resume(resume_text, jd_text):
    jd_keywords = extract_keywords(jd_text)
    resume_keywords = extract_keywords(resume_text)

    matched = jd_keywords & resume_keywords
    unmatched = jd_keywords - resume_keywords

    score = round((len(matched) / len(jd_keywords)) * 100, 2) if jd_keywords else 0

    return {
        "score": score,
        "matched": sorted(list(matched)),
        "unmatched": sorted(list(unmatched))
    }
