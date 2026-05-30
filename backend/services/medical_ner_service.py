import re


MEDICAL_TERMS = {
    "symptoms": [
        "fever",
        "cough",
        "fatigue",
        "pain",
        "headache",
        "nausea",
        "vomiting",
        "dizziness",
        "shortness of breath",
        "chest pain",
        "rash",
        "swelling",
        "bleeding",
        "weight loss",
        "blurred vision",
        "frequent urination",
        "increased thirst",
    ],

    "diseases": [
        "diabetes",
        "cancer",
        "asthma",
        "hypertension",
        "heart disease",
        "stroke",
        "infection",
        "covid",
        "flu",
        "malaria",
        "tuberculosis",
        "arthritis",
        "depression",
        "anxiety",
        "kidney disease",
        "liver disease",
    ],

    "treatments": [
        "insulin",
        "antibiotics",
        "chemotherapy",
        "radiation",
        "surgery",
        "therapy",
        "medication",
        "vaccine",
        "vaccination",
        "exercise",
        "diet",
        "rest",
        "hydration",
    ],

    "body_parts": [
        "heart",
        "lung",
        "liver",
        "kidney",
        "brain",
        "stomach",
        "skin",
        "eye",
        "ear",
        "throat",
        "blood",
        "bone",
        "muscle",
        "chest",
        "abdomen",
    ],
}


def find_terms(text, terms):
    found = []

    lower_text = text.lower()

    for term in terms:
        pattern = r"\b" + re.escape(term.lower()) + r"\b"

        if re.search(pattern, lower_text):
            found.append(term)

    return found


def extract_medical_entities(text):
    return {
        category: find_terms(text, terms)
        for category, terms in MEDICAL_TERMS.items()
    }