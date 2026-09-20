const Anthropic = require("@anthropic-ai/sdk");
const { CircuitBreaker } = require("./circuit-breaker");
const { FallbackCache } = require("./fallback-cache");

// TODO: Step 4 — Build classifyWithBreaker(documentText)
// Use a shared CircuitBreaker (failureThreshold: 3, resetTimeoutMs: 10000)
// and a shared FallbackCache
//
// breaker.execute() primary fn: call Claude API to classify the document
//   - Use the classify_document tool (category, confidence, reasoning)
//   - On success: store result in cache and return it
//   - On tool_use response: extract classification from toolUse block
//
// breaker.execute() fallback fn:
//   - Try cache.get(cacheKey) first
//   - If no cache: return degraded default classification (_degraded: true)

const breaker = new CircuitBreaker({ failureThreshold: 3, resetTimeoutMs: 10000 });
const cache = new FallbackCache();

const classifyTools = [
  {
    name: "classify_document",
    description: "Classify a document into a category.",
    input_schema: {
      type: "object",
      properties: {
        category: { type: "string", enum: ["invoice", "contract", "report", "memo", "legal_filing", "correspondence"] },
        confidence: { type: "number" },
        reasoning: { type: "string" }
      },
      required: ["category", "confidence", "reasoning"]
    }
  }
];

async function classifyWithBreaker(documentText) {
  const cacheKey = cache.generateKey(documentText);

  // TODO: implement using breaker.execute(primaryFn, fallbackFn)
}

// Test documents
async function main() {
  const docs = [
    "INVOICE #001 - Amount: $5,000 - Due: Net 30",
    "MEMORANDUM - To: All Staff - Subject: Holiday Schedule",
    "This Agreement is entered into by Company A and Company B..."
  ];

  for (const doc of docs) {
    console.log(`\n--- Processing ---`);
    const result = await classifyWithBreaker(doc);
    console.log("Result:", JSON.stringify(result, null, 2));
    console.log("Breaker status:", breaker.getStatus());
  }
}

main().catch(console.error);
