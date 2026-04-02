const { chunkDocument } = require("./chunker");
const { extractFacts } = require("./fact-extractor");
const { FactStore } = require("./fact-store");
const Anthropic = require("@anthropic-ai/sdk");
const fs = require("fs");
const path = require("path");
const client = new Anthropic();

// TODO: Task 4 — Implement processLongDocument(documentText)
//
// 1. Chunk the document using chunkDocument()
// 2. Process each chunk: call extractFacts() and add to FactStore
// 3. Log progress and print the fact summary with any contradictions
// 4. Generate a final summary from preserved facts using client.messages.create()
//    - System prompt: CRITICAL — preserve ALL numbers, dates, names EXACTLY
//    - User message: the formatted facts list from factStore.getFactsForFinalSummary()
// 5. Return { summary, factStore: factStore.getSummary(), contradictions }

async function processLongDocument(documentText) {
  console.log(`Document length: ${documentText.length} characters`);

  // Step 1: Chunk the document
  const chunks = chunkDocument(documentText);
  console.log(`Split into ${chunks.length} chunks`);

  // Step 2: Extract facts from each chunk
  const factStore = new FactStore();
  for (const chunk of chunks) {
    console.log(`Processing chunk ${chunk.index + 1}/${chunks.length}...`);
    // TODO: extract facts and add to store
  }

  console.log(`\nFact extraction complete:`);
  console.log(JSON.stringify(factStore.getSummary(), null, 2));

  if (factStore.contradictions.length > 0) {
    console.log(`\nWARNING: ${factStore.contradictions.length} contradictions detected!`);
    // TODO: log contradiction details
  }

  // Step 3: Generate final summary from preserved facts
  const factsForSummary = factStore.getFactsForFinalSummary();

  // TODO: call client.messages.create() with strict fact-preservation system prompt

  return {
    summary: "", // TODO: replace with actual summary
    factStore: factStore.getSummary(),
    contradictions: factStore.contradictions
  };
}

// Run with the sample long contract
const contractPath = path.join(__dirname, "test-data", "long-contract.txt");
const documentText = fs.readFileSync(contractPath, "utf-8");

processLongDocument(documentText)
  .then(result => {
    console.log("\n=== Final Summary ===");
    console.log(result.summary);
    console.log("\n=== Fact Store Summary ===");
    console.log(JSON.stringify(result.factStore, null, 2));
  })
  .catch(console.error);
