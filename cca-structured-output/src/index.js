import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();
// DocStream Structured Output - JSON schema design with tool_use
const classificationSchema = {
  name: "classify_document",
  description: "Classify a document and extract structured metadata",
  input_schema: {
    type: "object",
    properties: {
      // TODO: Design the schema
    },
    required: []
  }
};
console.log("DocStream Structured Output Lab - Ready");
