const { MessageBus } = require("./message-bus");
const { runExtractor } = require("./agents/extractor");
const { runClassifier } = require("./agents/classifier");
const { runSummarizer } = require("./agents/summarizer");
const { runRouter } = require("./agents/router");

// TODO: Step 7 — Implement processDocument(documentText)
// Pipeline stages: Extract -> Classify -> Summarize -> Route
// Use a shared MessageBus instance for all agents
// Log progress at each stage and total elapsed time
// Return: { extracted, classified, summarized, routed, pipelineMessages, elapsedMs }
async function processDocument(documentText) {
  const bus = new MessageBus();
  const startTime = Date.now();

  // TODO: implement the 4-stage pipeline

  const elapsed = Date.now() - startTime;
  console.log(`\n=== Pipeline complete in ${elapsed}ms ===`);

  return {
    // TODO: return all stage results and bus.messages
  };
}

// Test document — NovaPulse Services Agreement
const testDoc = `SERVICES AGREEMENT

This Services Agreement ("Agreement") is entered into as of March 15, 2024, by and between NovaPulse Technologies Inc., a Delaware corporation ("Client"), and CloudScale Solutions LLC ("Provider").

1. SERVICES: Provider shall deliver cloud infrastructure migration services for Client's DocStream platform, including:
   - Migration of 47 microservices to Kubernetes
   - Database replication setup (MySQL to Aurora)
   - Load testing and performance benchmarking

2. COMPENSATION: Client shall pay Provider $285,000 in three milestones:
   - $95,000 upon signing
   - $95,000 upon completion of migration
   - $95,000 upon successful load testing

3. TERM: This Agreement shall commence on April 1, 2024 and continue for six (6) months.

4. CONFIDENTIALITY: Both parties agree to maintain confidentiality of all proprietary information.`;

processDocument(testDoc)
  .then(result => {
    console.log("\n=== Final Result ===");
    console.log(JSON.stringify(result, null, 2));
  })
  .catch(console.error);
