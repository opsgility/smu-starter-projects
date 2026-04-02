const Anthropic = require("@anthropic-ai/sdk");
const client = new Anthropic();

// TODO: Task 1 — Define the four-step prompt chain
// Each step has a name and system prompt that uses XML tags for structured output
//
// extract: Pull entities, dates, financial amounts using <extraction> XML structure
// classify: Use extracted data to classify using <classification> XML structure
// summarize: Generate summary and action items using <summary> XML structure
// route: Decide destination and urgency using <routing> XML structure

const CHAIN_STEPS = {
  extract: {
    name: "Extract",
    system: `Extract key information from the document. Structure your response using XML tags:

<extraction>
  <document_type>the apparent type of document</document_type>
  <key_entities>
    <entity role="...">name</entity>
  </key_entities>
  <dates>
    <date type="...">YYYY-MM-DD</date>
  </dates>
  <financial>
    <amount currency="...">number</amount>
  </financial>
  <key_phrases>important phrases or terms from the document</key_phrases>
</extraction>

Include only information explicitly present. Use "unknown" for undetermined fields.`
  },

  classify: {
    name: "Classify",
    system: `You receive extracted document metadata in XML. Based on the extraction, classify the document.

<classification>
  <category>invoice|contract|report|correspondence|technical_spec</category>
  <confidence>0.0-1.0</confidence>
  <evidence>specific extraction fields that support this classification</evidence>
  <alternative_category>second most likely category, if any</alternative_category>
</classification>`
  },

  summarize: {
    name: "Summarize",
    system: `You receive document extraction and classification in XML. Generate a concise summary.

<summary>
  <headline>one-line description (max 100 chars)</headline>
  <body>2-3 sentence summary covering who, what, when, and why</body>
  <action_items>
    <item priority="high|medium|low">specific action needed</item>
  </action_items>
</summary>`
  },

  route: {
    name: "Route",
    system: `You receive document extraction, classification, and summary in XML. Determine routing.

<routing>
  <destination>finance|legal|engineering|management|archive</destination>
  <urgency>immediate|standard|low</urgency>
  <reason>why this destination and urgency level</reason>
  <notify>
    <person role="...">who should be notified</person>
  </notify>
</routing>`
  }
};

// TODO: Task 2 — Implement validateStepOutput(stepName, output)
// Check that expected XML tags are present in the output
// Throw an error listing missing tags if any are absent
function validateStepOutput(stepName, output) {
  const expectedTags = {
    extract: ["extraction", "document_type", "key_entities"],
    classify: ["classification", "category", "confidence"],
    summarize: ["summary", "headline", "body"],
    route: ["routing", "destination", "urgency"]
  };

  // TODO: implement tag presence check
}

// TODO: Task 2 — Implement executeChain(documentText)
// For each step in CHAIN_STEPS:
//   1. Build user message — first step uses raw document, subsequent steps use accumulated XML
//   2. Call client.messages.create() with step.system
//   3. Validate output with validateStepOutput() — retry that step if invalid
//   4. Accumulate results: wrap each step output in <stepname_result>...</stepname_result>
// Return all step results as an object

async function executeChain(documentText) {
  const results = {};
  let context = documentText;

  for (const [stepName, step] of Object.entries(CHAIN_STEPS)) {
    console.log(`  Step: ${step.name}...`);

    // TODO: implement
  }

  return results;
}

// Test document
const testDoc = `SERVICES AGREEMENT

This Services Agreement is entered into as of March 15, 2024, by and between NovaPulse Technologies Inc. (Client) and CloudScale Solutions LLC (Provider).

1. SERVICES: Cloud infrastructure migration for DocStream platform.
   - Migration of 47 microservices to Kubernetes

2. COMPENSATION: $285,000 in three milestones ($95,000 each).

3. TERM: April 1, 2024 through September 30, 2024.

4. CONFIDENTIALITY: Both parties maintain confidentiality of proprietary information.`;

async function main() {
  console.log("Running 4-step prompt chain...\n");
  const results = await executeChain(testDoc);
  console.log("\n=== Chain Results ===");
  for (const [step, output] of Object.entries(results)) {
    console.log(`\n--- ${step} ---`);
    console.log(output);
  }
}

main().catch(console.error);
