from __future__ import annotations

from schema import LearnerCandidate


def observe_turn(user_text: str, assistant_text: str) -> LearnerCandidate:
    # MVP determinista. Luego puede reemplazarse por llamada a modelo.
    joined = f"USER: {user_text}
ASSISTANT: {assistant_text}"
    return LearnerCandidate(
        observation="Hubo un turno de interacción que debe resumirse sin cambiar el objetivo fijo.",
        hypothesis="El usuario busca preservar experiencia operativa separada de la respuesta inmediata.",
        candidate_learning=joined[:1000],
        rejected_branch="Convertir cada interpretación en memoria permanente sin curaduría.",
        doubt="Si este turno debe guardarse completo o solo como regla abstracta.",
        confidence=0.65,
    )
