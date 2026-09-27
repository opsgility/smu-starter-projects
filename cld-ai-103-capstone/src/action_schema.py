"""COMPLETE: JSON schema for the final action record (L8 pattern)."""

ACTION_SCHEMA = {
    "name": "submit_action_record",
    "description": "Submit the structured action record for what the agent decided to do.",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {"type": "string"},
            "decided_action": {
                "type": "string",
                "enum": ["refund_approved", "escalate_suspended", "escalate_reactivation",
                         "escalate_pattern", "escalate_urgent", "escalate_compliance",
                         "escalate_injection_detected", "escalate_retention",
                         "escalate_or_refuse", "no_leak", "technical_investigation",
                         "no_action"]
            },
            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
            "reasoning": {"type": "string", "description": "One paragraph explaining the decision."},
            "tools_used": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["customer_id", "decided_action", "priority", "reasoning", "tools_used"],
        "additionalProperties": False
    }
}
