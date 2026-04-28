"""Utility billing and service policy Q&A helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UtilityPolicySource:
    source_id: str
    title: str
    text: str
    citation: str


@dataclass(frozen=True)
class UtilityPolicyAnswer:
    answer: str
    citations: tuple[str, ...]
    csr_review_required: bool
    boundary: str


def answer_utility_question(
    question: str, sources: list[UtilityPolicySource]
) -> UtilityPolicyAnswer:
    citations = tuple(source.citation for source in sources if source.text)
    answer = (
        f"Draft utility customer-service answer for: {question}. "
        "Use the cited policy manual before giving this to a resident."
    )
    return UtilityPolicyAnswer(
        answer=answer,
        citations=citations,
        csr_review_required=True,
        boundary=(
            "CivicUtility is a copilot for policy and service-rule answers, not a utility "
            "billing system, payment processor, rate engine, or account system of record."
        ),
    )
