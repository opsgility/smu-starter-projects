import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();
// DocStream Prompt Engineering - Build production system prompts
const sampleDocuments = [
  "INVOICE #2847 - Due: April 15, 2026 - Amount: $4,500.00",
  "MEMORANDUM - To: All Staff - Re: Q2 Planning Session",
  "CONTRACT - This Service Level Agreement between NovaPulse and Acme Corp..."
];
console.log("DocStream Prompt Engineering Lab - Ready");
