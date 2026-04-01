import base64
import io
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ocr import extract_text_from_image
from solver import build_solver_prompt, solve_question


class SolveRequest(BaseModel):
    question_text: Optional[str] = Field(default="", description="Typed question")
    image_base64: Optional[str] = Field(
        default=None, description="Optional base64-encoded image data"
    )
    class_level: int = Field(ge=1, le=12)
    explanation_mode: str = Field(default="english", pattern="^(english|hindi|bilingual)$")


class SolveResponse(BaseModel):
    extracted_text: str
    normalized_question: str
    solution: str


app = FastAPI(title="Student Math & Physics Solver API", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "solver-api"}


@app.post("/solve", response_model=SolveResponse)
def solve(req: SolveRequest) -> SolveResponse:
    extracted_text = ""

    if req.image_base64:
        try:
            image_bytes = base64.b64decode(req.image_base64)
            extracted_text = extract_text_from_image(io.BytesIO(image_bytes))
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail=f"OCR failed: {exc}") from exc

    merged_question = "\n".join(
        part.strip() for part in [req.question_text or "", extracted_text] if part and part.strip()
    ).strip()

    if not merged_question:
        raise HTTPException(
            status_code=400,
            detail="No valid question found. Please type a question or upload a clearer image.",
        )

    try:
        user_prompt = build_solver_prompt(
            question=merged_question,
            class_level=req.class_level,
            explanation_mode=req.explanation_mode,
        )
        solution = solve_question(user_prompt)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Solver failed: {exc}") from exc

    return SolveResponse(
        extracted_text=extracted_text,
        normalized_question=merged_question,
        solution=solution,
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
