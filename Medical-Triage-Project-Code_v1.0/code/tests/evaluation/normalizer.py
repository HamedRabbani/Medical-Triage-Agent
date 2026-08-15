def normalize(text: str) -> str:
    text = text.strip().lower()

    replacements = {
        "،": ",",
        " و ": ",",
        "fever, cough": "fever,cough",
        "fever and cough": "fever,cough",
        "درد قفسه سینه، سخت نفس کشیدن": "درد قفسه سینه,سخت نفس کشیدن",
        "درد قفسه سینه و تنگی نفس": "درد قفسه سینه,تنگی نفس",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text