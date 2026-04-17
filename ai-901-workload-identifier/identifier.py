"""
Map a plain-English business scenario to the right Azure AI workload + service.
"""
import json
import sys
from pathlib import Path

SCENARIOS = json.loads((Path(__file__).parent / "scenarios.json").read_text(encoding="utf-8"))


WORKLOAD_KEYWORDS: dict[str, list[str]] = {
    # TODO 1: expand this dictionary so each workload maps to a list of trigger keywords.
    # Example structure:
    # "Generative AI": ["chatbot", "generate", "write", "draft", "summarize"],
    # "Text Analysis": ["sentiment", "entity", "key phrase", "classify"],
    # "Speech":        ["transcribe", "voice", "spoken", "audio to text"],
    # "Computer Vision": ["image", "photo", "detect object", "classify image"],
    # "Information Extraction": ["invoice", "receipt", "form", "extract from pdf"],
}


SERVICE_FOR_WORKLOAD: dict[str, str] = {
    # TODO 2: map each workload to an Azure service available in Foundry.
    # "Generative AI":           "Microsoft Foundry (Azure OpenAI)",
    # "Text Analysis":           "Azure AI Language",
    # "Speech":                  "Azure AI Speech",
    # "Computer Vision":         "Azure AI Vision",
    # "Information Extraction":  "Azure Content Understanding (in Foundry Tools)",
}


def identify(scenario: str) -> tuple[str, str]:
    """Return (workload, recommended_service) for a scenario string."""
    # TODO 3: lowercase the scenario, find the first workload whose keyword list has a hit,
    #         return (workload, SERVICE_FOR_WORKLOAD[workload]).
    #         Fall back to ("Unknown", "Review manually") if nothing matches.
    raise NotImplementedError


def main() -> None:
    if len(sys.argv) > 1:
        scenario = " ".join(sys.argv[1:])
        workload, service = identify(scenario)
        print(f"Workload: {workload}\nService: {service}")
        return

    for sample in SCENARIOS:
        workload, service = identify(sample["scenario"])
        print(f"[{sample['expected']}] -> detected {workload} via {service}")


if __name__ == "__main__":
    main()
