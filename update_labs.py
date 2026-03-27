#!/usr/bin/env python3
"""Script to extract and modify agent instructions for labs 1284, 1286, 1288, 1290."""
import json
import sys

BASE = r"C:\Users\mwash\.claude\projects\C--repos-smu-courses-mcp\a47d3001-4cca-42cc-af1e-210286ab57c9\tool-results"

def load_instructions(filename):
    with open(f"{BASE}/{filename}", 'r', encoding='utf-8') as f:
        data = json.load(f)
    return json.loads(data[0]['text'])['AgentInstructions']

def save_instructions(lab_id, instructions):
    with open(f"{BASE}/lab{lab_id}_updated.txt", 'w', encoding='utf-8') as f:
        f.write(instructions)
    print(f"Lab {lab_id}: saved {len(instructions)} chars")

# Lab 1284 - Replace 3 existing image URLs
instructions = load_instructions("toolu_01WGyPh7SLGbJMgncjpi48PB.json")
instructions = instructions.replace(
    "organizations/3/labs/1284/images/79f5a3b9-0f29-4dc0-807b-1917f5a6fe80_signalr-hub-architecture.png",
    "organizations/3/labs/1284/images/9ee695d7-6b15-497c-8cfc-d760f5f0000a_signalr-hub-architecture.png"
)
instructions = instructions.replace(
    "organizations/3/labs/1284/images/5d14c48a-0a7c-4b4d-bafd-11e4655a9e72_realtime-transport-comparison.png",
    "organizations/3/labs/1284/images/fc79bc4f-4ce1-45eb-ba34-e2495b04bc22_signalr-transport-comparison.png"
)
instructions = instructions.replace(
    "organizations/3/labs/1284/images/8d2db878-c76b-45ce-a8c5-08642a107b05_ihubcontext-integration-flow.png",
    "organizations/3/labs/1284/images/afcb3ddc-bda4-49f3-aac5-cb8ccfeae3d1_signalr-event-broadcasting-flow.png"
)
save_instructions(1284, instructions)

# Lab 1286 - Replace 3 existing image URLs
instructions = load_instructions("toolu_019ZwLYprzyouHPFB7m9M62T.json")
instructions = instructions.replace(
    "organizations/3/labs/1286/images/b4b66679-cc31-4c84-9d89-d16f76436ca2_backgroundservice-lifecycle.png",
    "organizations/3/labs/1286/images/025c9a0b-3a0c-48d3-9258-bafde21ce1a3_backgroundservice-lifecycle.png"
)
instructions = instructions.replace(
    "organizations/3/labs/1286/images/0f066144-6c42-471b-a20d-fa62de96e469_task-reminder-flow.png",
    "organizations/3/labs/1286/images/a20333bd-469c-43ce-b695-44cbb640277c_task-reminder-service-flow.png"
)
instructions = instructions.replace(
    "organizations/3/labs/1286/images/ce0573e1-f923-477e-8432-327fcf699ee6_email-service-architecture.png",
    "organizations/3/labs/1286/images/02a306b8-57d9-4084-a736-ed1aa6d6f928_email-service-architecture.png"
)
save_instructions(1286, instructions)

# Lab 1288 - Insert 3 new diagrams
instructions = load_instructions("toolu_01DFcor2iFWVuX4QqBQoHYRz.json")

# Diagram 1: Subscription Lifecycle - insert after the status lifecycle ASCII art
anchor1 = "| Canceled \u2192 Active | Customer reactivates before expiry | Cancel the cancellation, resume billing |"
insert1 = "\n\n**Display this diagram to the student:**\n![Subscription Lifecycle State Machine](https://labstoragesupport.blob.core.windows.net/exercise-content/organizations/3/labs/1288/images/0241cba4-ed41-488c-8a7d-e6544c779e79_subscription-lifecycle-state-machine.png)"
instructions = instructions.replace(anchor1, anchor1 + insert1)

# Diagram 2: Webhook Processing - insert after the webhook events table
anchor2 = "| `customer.subscription.deleted` | Subscription fully canceled in Stripe | Set Status = Expired, downgrade to Free |"
insert2 = "\n\n**Display this diagram to the student:**\n![Stripe Webhook Processing Flow](https://labstoragesupport.blob.core.windows.net/exercise-content/organizations/3/labs/1288/images/7477ef0f-3677-47b7-92b2-e16e6a360afb_stripe-webhook-processing.png)"
instructions = instructions.replace(anchor2, anchor2 + insert2)

# Diagram 3: Plan Feature Gating - insert after PlanLimits table in Topic 1
anchor3 = "| Advanced reporting | No | No | Yes |"
insert3 = "\n\n**Display this diagram to the student:**\n![Plan Feature Gating Comparison](https://labstoragesupport.blob.core.windows.net/exercise-content/organizations/3/labs/1288/images/16824c5d-9a4c-4d12-8b52-89ef5a2db99b_plan-feature-gating.png)"
instructions = instructions.replace(anchor3, anchor3 + insert3)

save_instructions(1288, instructions)

# Lab 1290 - Insert 3 new diagrams
instructions = load_instructions("toolu_013psAy3m9FWjz5qoSJ2zoDn.json")

# Diagram 1: File Upload Flow - insert after "Key design decisions in the controller:"
anchor1 = "Key design decisions in the controller:"
insert1 = "\n\n**Display this diagram to the student:**\n![File Upload Flow](https://labstoragesupport.blob.core.windows.net/exercise-content/organizations/3/labs/1290/images/4411961e-c935-4453-960b-8c0b24dc4b71_file-upload-flow.png)\n"
instructions = instructions.replace(anchor1, insert1 + "\n" + anchor1)

# Diagram 2: Storage Quota - insert after the plan quota table
anchor2 = "| **Enterprise** | $99/month | 50 GB |"
insert2 = "\n\n**Display this diagram to the student:**\n![Storage Quota Enforcement](https://labstoragesupport.blob.core.windows.net/exercise-content/organizations/3/labs/1290/images/ad32a4b9-f9be-4857-a1a0-4aa341a71c07_storage-quota-enforcement.png)"
instructions = instructions.replace(anchor2, anchor2 + insert2)

# Diagram 3: File Security Checklist - insert after the security threats table
anchor3 = "| **Denial of Service** | Upload thousands of files or huge files | Disk exhaustion, memory exhaustion | Size limits, quota enforcement, rate limiting |"
insert3 = "\n\n**Display this diagram to the student:**\n![File Security Checklist](https://labstoragesupport.blob.core.windows.net/exercise-content/organizations/3/labs/1290/images/46204456-4d9f-44ce-9253-902e740d5fd0_file-security-checklist.png)"
instructions = instructions.replace(anchor3, anchor3 + insert3)

save_instructions(1290, instructions)

print("\nAll done! Updated instructions saved to lab*_updated.txt files.")
