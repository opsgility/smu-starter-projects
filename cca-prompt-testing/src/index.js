const Anthropic = require("@anthropic-ai/sdk");
const client = new Anthropic();
// DocStream Prompt Testing - Evaluation framework
const testCases = [
  { input: "INVOICE #123 - Amount: $500", expectedCategory: "invoice" },
  { input: "Dear Team, Please review the attached report", expectedCategory: "memo" },
  { input: "This agreement shall commence on...", expectedCategory: "contract" },
];
console.log("DocStream Prompt Testing Lab - Ready");
console.log("Test cases:", testCases.length);
