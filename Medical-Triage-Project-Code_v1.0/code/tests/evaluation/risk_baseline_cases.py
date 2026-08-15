RISK_BASELINE_CASES = [
    {
        "name": "chest_pain_with_shortness_of_breath",
        "state": {
            "symptoms": [
                "chest pain",
                "shortness of breath",
            ],
            "severity": "moderate",
            "age": 35,
            "duration": "1 day",
        },
        "expected_risk": "HIGH",
    },
    {
        "name": "loss_of_consciousness",
        "state": {
            "symptoms": [
                "loss of consciousness",
            ],
            "severity": "moderate",
            "age": 40,
            "duration": "1 day",
        },
        "expected_risk": "HIGH",
    },
    {
        "name": "severe_headache",
        "state": {
            "symptoms": [
                "headache",
            ],
            "severity": "severe",
            "age": 30,
            "duration": "2 days",
        },
        "expected_risk": "HIGH",
    },
    {
        "name": "mild_headache",
        "state": {
            "symptoms": [
                "headache",
            ],
            "severity": "mild",
            "age": 30,
            "duration": "1 day",
        },
        "expected_risk": "LOW",
    },
    {
        "name": "fever_and_headache",
        "state": {
            "symptoms": [
                "fever",
                "headache",
            ],
            "severity": "moderate",
            "age": 30,
            "duration": "2 days",
        },
        "expected_risk": "LOW",
    },
]