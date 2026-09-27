"""STRICT and LOOSE extraction schemas for the ablation."""


STRICT_SCHEMA = {
    "name": "submit_ticket_extraction",
    "description": ("Submit a structured warehouse record for the analyzed ticket. "
                   "All fields are required and constrained by the schema."),
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The customer identifier mentioned in the ticket (e.g. 'acme-corp')."
            },
            "category": {
                "type": "string",
                "enum": ["Billing", "Technical", "Feature Request", "Escalate", "Other"]
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative", "urgent"]
            },
            "requires_escalation": {
                "type": "boolean",
                "description": "True if the ticket mentions GDPR/SOC2/HIPAA/PCI, data loss, or security."
            },
            "recommended_action": {
                "type": "string",
                "description": "One imperative sentence, max 200 chars."
            },
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["customer_id", "product", "amount_usd", "date", "regulatory_keyword", "endpoint"]
                        },
                        "value": {"type": "string"}
                    },
                    "required": ["type", "value"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["customer_id", "category", "sentiment", "requires_escalation",
                    "recommended_action", "entities"],
        "additionalProperties": False
    }
}


# Deliberately loose schema for the ablation in Exercise 3.
LOOSE_SCHEMA = {
    "name": "submit_ticket_extraction",
    "description": "Submit a structured record for the analyzed ticket.",
    "input_schema": {"type": "object"}
}
