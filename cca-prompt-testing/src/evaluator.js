const Anthropic = require("@anthropic-ai/sdk");
const fs = require("fs");
const client = new Anthropic();

// TODO: Task 2 — Implement the PromptEvaluator class
//
// evaluatePrompt(promptConfig, testCases): run promptConfig against all testCases
//   - promptConfig: { name, system, examples }
//   - For each testCase: call client.messages.create(), parse JSON, record result
//   - Track: test_id, expected, predicted, confidence, correct, difficulty, latency_ms, tokens
//   - Return computeMetrics(name, results)
//
// computeMetrics(name, results): compute evaluation statistics
//   - accuracy: correct / total
//   - byDifficulty: accuracy per difficulty level (easy/medium/hard)
//   - precision: per-category true positives / predicted positive
//   - cost: (totalInputTokens * 0.003 + totalOutputTokens * 0.015) / 1000
//   - avgLatency: average response time
//   - confidenceCalibration: avg confidence when correct vs incorrect
//   - errors: list of incorrect predictions
//   - raw: all individual results

class PromptEvaluator {
  constructor() {
    this.results = [];
    // TODO: initialize additional state as needed
  }

  async evaluatePrompt(promptConfig, testCases) {
    const results = [];

    for (const tc of testCases) {
      const startTime = Date.now();

      // TODO: call client.messages.create() with promptConfig
      // Parse JSON response, compute latency, record result

      results.push({
        test_id: tc.id,
        expected: tc.expected_category,
        predicted: null,   // TODO: replace with actual prediction
        confidence: null,  // TODO: replace with actual confidence
        correct: false,    // TODO: replace with actual correctness
        difficulty: tc.difficulty,
        latency_ms: Date.now() - startTime,
        input_tokens: 0,   // TODO: replace with actual token count
        output_tokens: 0   // TODO: replace with actual token count
      });
    }

    return this.computeMetrics(promptConfig.name, results);
  }

  computeMetrics(name, results) {
    // TODO: implement metrics computation
    return {
      name,
      accuracy: 0,
      byDifficulty: {},
      precision: {},
      cost: "$0.0000",
      avgLatency: 0,
      confidenceCalibration: { whenCorrect: "0.00", whenIncorrect: "0.00" },
      errors: [],
      raw: results
    };
  }
}

// TODO: Task 4 — Implement detectRegressions(baseline, candidate)
// Compare two evaluation runs and flag any regressions:
//   - Overall accuracy drop
//   - Per-difficulty regressions
//   - New errors on tests that baseline got correct
function detectRegressions(baseline, candidate) {
  const regressions = [];

  // TODO: implement regression detection

  return { hasRegressions: regressions.length > 0, regressions };
}

// TODO: Task 3 — Run A/B comparison and save report
async function main() {
  const testData = JSON.parse(fs.readFileSync("src/test-data/classification-tests.json", "utf-8"));
  const { PROMPT_VARIANTS } = require("./prompt-variants");

  const evaluator = new PromptEvaluator();
  const reports = [];

  for (const variant of PROMPT_VARIANTS) {
    console.log(`\nEvaluating: ${variant.name}`);
    const report = await evaluator.evaluatePrompt(variant, testData.cases);
    reports.push(report);

    console.log(`  Accuracy: ${(report.accuracy * 100).toFixed(1)}%`);
    console.log(`  Cost: ${report.cost}`);
    console.log(`  Errors: ${report.errors.length}`);
  }

  // Detect regressions between first two variants
  if (reports.length >= 2) {
    const regression = detectRegressions(reports[0], reports[1]);
    if (regression.hasRegressions) {
      console.log("\n=== REGRESSIONS DETECTED ===");
      for (const r of regression.regressions) console.log(`  - ${r}`);
    }
  }

  // Save full report
  fs.mkdirSync("output", { recursive: true });
  fs.writeFileSync("output/eval-report.json", JSON.stringify(reports, null, 2));
  console.log("\nReport saved to output/eval-report.json");
}

main().catch(console.error);
