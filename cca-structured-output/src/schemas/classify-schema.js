// TODO: Task 1 — Define the CLASSIFY_TOOL schema for tool_use-based classification
//
// Tool name: "classify_document"
// Description: explain purpose and that it reports classification results
// input_schema properties:
//   - category: string, enum of 5 values (invoice/contract/report/correspondence/technical_spec)
//   - confidence: number, minimum 0, maximum 1
//   - reasoning: string, brief explanation
//   - metadata: object with required boolean flags and entity array:
//       has_financial_data: boolean
//       has_legal_terms: boolean
//       has_technical_content: boolean
//       primary_entities: array of strings
// All top-level properties required

const CLASSIFY_TOOL = {
  name: "classify_document",
  description: "Classify an enterprise document into a category and extract key metadata. Use this tool to report your classification result.",
  input_schema: {
    type: "object",
    properties: {
      // TODO: implement all properties as described above
    },
    required: ["category", "confidence", "reasoning", "metadata"]
  }
};

module.exports = { CLASSIFY_TOOL };
