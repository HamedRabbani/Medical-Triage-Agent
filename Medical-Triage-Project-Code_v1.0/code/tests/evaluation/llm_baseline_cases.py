CASES = [
    {
        "input": "من سردرد دارم",
        "expected_symptoms": ["headache"],
    },
    {
        "input": "من تب و سردرد دارم",
        "expected_symptoms": ["fever", "headache"],
    },
    {
        "input": "I have fever and a cough",
        "expected_symptoms": ["fever", "cough"],
    },
    {
        "input": "قفسه سینه‌ام درد می‌کند",
        "expected_symptoms": ["chest pain"],
    },
    {
        "input": "حالم خوب نیست",
        "expected_symptoms": [],
    },
]