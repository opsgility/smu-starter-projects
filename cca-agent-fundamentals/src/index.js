const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic();

// DocStream Document Classifier Agent
// TODO: Implement the agentic loop with tool_use
const tools = [
  {
    name: "classify_document",
    description: "Classify a document into a category based on its content",
    input_schema: {
      type: "object",
      properties: {
        category: { type: "string", enum: ["invoice", "contract", "report", "memo", "other"] },
        confidence: { type: "number", minimum: 0, maximum: 1 },
        reasoning: { type: "string" }
      },
      required: ["category", "confidence", "reasoning"]
    }
  }
];

const sampleDocuments = [
  "INVOICE #2847 - Due: April 15, 2026 - Amount: $4,500.00 - Services rendered for Q1 consulting",
  "This agreement is entered into between NovaPulse Inc and Acme Corp for the provision of AI services...",
  "Q1 2026 Performance Report: Revenue increased 23% YoY. Customer acquisition cost decreased by 12%.",
];

console.log("DocStream Agent - Ready to classify documents");
console.log("Documents to process:", sampleDocuments.length);
