import os
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are a mathematics and physics teacher. "
    "Solve step by step, explain simply, and mention rules used in each step."
)


def _difficulty_label(class_level: int) -> str:
    if 1 <= class_level <= 5:
        return "simple"
    if 6 <= class_level <= 10:
        return "medium"
    return "detailed"


def build_solver_prompt(question: str, class_level: int, explanation_mode: str) -> str:
    difficulty = _difficulty_label(class_level)
    language_map = {
        "english": "Use English only.",
        "hindi": "Use Hindi only.",
        "bilingual": "Use both Hindi and English in each step.",
    }

    language_instruction = language_map.get(explanation_mode, "Use English only.")

    return (
        f"Student class level: {class_level} ({difficulty}).\n"
        f"Explanation mode: {explanation_mode}. {language_instruction}\n\n"
        "Output format strictly:\n"
        "Step 1: ...\n"
        "Rule Used: ...\n\n"
        "Step 2: ...\n"
        "Rule Used: ...\n\n"
        "Continue steps as needed.\n"
        "Final Answer: ...\n\n"
        "Keep it student-friendly and concise.\n"
        f"Question:\n{question}"
    )


def solve_question(user_prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing in environment variables.")

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.output_text.strip()
