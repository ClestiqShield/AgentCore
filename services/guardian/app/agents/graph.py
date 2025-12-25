from langgraph.graph import StateGraph, START, END
from app.agents.state import GuardianState
from app.agents.nodes.content_filter import content_filter_node
from app.agents.nodes.pii_scanner import pii_scanner_node
from app.agents.nodes.toon_decoder import toon_decoder_node

# Advanced validation nodes (non-LLM)
from app.agents.nodes.citation_verifier import citation_verifier_node
from app.agents.nodes.disclaimer_injector import disclaimer_injector_node
from app.agents.nodes.refusal_detector import refusal_detector_node

# NEW: Parallel LLM validator (replaces 3 sequential LLM nodes)
from app.agents.nodes.parallel_llm_validator import parallel_llm_validator_node


def create_guardian_graph():
    """
    Create the Guardian validation workflow with parallel LLM execution.

    Flow:
        START → content_filter (pattern-based only)
             → (if blocked) → END
             → (if passed) → pii_scanner → toon_decoder
             → parallel_llm_validator (toxicity + hallucination + tone in parallel)
             → citation_verifier → refusal_detector
             → disclaimer_injector → END

    The parallel_llm_validator replaces:
    - content_filter (LLM toxicity check)
    - hallucination_detector
    - tone_checker

    Reducing LLM latency from 3-6s to 1-2s (67-83% improvement).
    """
    workflow = StateGraph(GuardianState)

    # Add pattern-based validation nodes
    workflow.add_node("content_filter", content_filter_node)
    workflow.add_node("pii_scanner", pii_scanner_node)
    workflow.add_node("toon_decoder", toon_decoder_node)

    # NEW: Add parallel LLM validator (replaces 3 sequential LLM nodes)
    workflow.add_node("parallel_llm_validator", parallel_llm_validator_node)

    # Add remaining non-LLM validation nodes
    workflow.add_node("citation_verifier", citation_verifier_node)
    workflow.add_node("refusal_detector", refusal_detector_node)
    workflow.add_node("disclaimer_injector", disclaimer_injector_node)

    # Entry point
    workflow.add_edge(START, "content_filter")

    # Conditional routing after content filter (pattern-based blocking)
    def route_after_filter(state: GuardianState):
        if state.get("content_blocked"):
            return END
        return "pii_scanner"

    workflow.add_conditional_edges("content_filter", route_after_filter)

    # Flow: PII → TOON → Parallel LLM Checks → Citation → Refusal → Disclaimer → END
    workflow.add_edge("pii_scanner", "toon_decoder")
    workflow.add_edge("toon_decoder", "parallel_llm_validator")
    workflow.add_edge("parallel_llm_validator", "citation_verifier")
    workflow.add_edge("citation_verifier", "refusal_detector")
    workflow.add_edge("refusal_detector", "disclaimer_injector")
    workflow.add_edge("disclaimer_injector", END)

    return workflow.compile()


guardian_graph = create_guardian_graph()
