// TODO: Task 3 — Implement the FactStore class
//
// addFacts(newFacts): for each fact:
//   - Check findDuplicate() — if found, merge provenance and update confidence
//   - Check findContradiction() — if found, record in this.contradictions
//   - Otherwise push to this.facts
//
// findDuplicate(newFact): find existing fact with same category and > 85% text similarity
//
// findContradiction(newFact): find existing fact with same category, same subject
//   but < 50% text similarity (likely conflicting values)
//
// textSimilarity(a, b): Jaccard similarity of word sets (intersection / max of sizes)
//
// shareSubject(a, b): check if capitalized entity names overlap between two facts
//
// getSummary(): { total_facts, by_category, contradictions, high_confidence }
//
// getFactsForFinalSummary(): sorted by confidence desc, formatted as:
//   "[{category}] {fact} (source: chunk {chunk_index})"

class FactStore {
  constructor() {
    this.facts = [];
    this.contradictions = [];
    // TODO: initialize additional state as needed
  }

  addFacts(newFacts) {
    for (const fact of newFacts) {
      // TODO: implement duplicate check, contradiction check, and append
    }
  }

  findDuplicate(newFact) {
    // TODO: implement
    return null;
  }

  findContradiction(newFact) {
    // TODO: implement
    return null;
  }

  textSimilarity(a, b) {
    // TODO: implement Jaccard similarity of word sets
    return 0;
  }

  shareSubject(a, b) {
    // TODO: implement — extract capitalized words, check for overlap
    return false;
  }

  getSummary() {
    return {
      total_facts: this.facts.length,
      by_category: this.facts.reduce((acc, f) => {
        acc[f.category] = (acc[f.category] || 0) + 1;
        return acc;
      }, {}),
      contradictions: this.contradictions.length,
      high_confidence: this.facts.filter(f => f.confidence >= 0.9).length
    };
  }

  getFactsForFinalSummary() {
    // TODO: implement — sort by confidence desc, format as strings with provenance
    return this.facts
      .sort((a, b) => b.confidence - a.confidence)
      .map(f => {
        const chunkRef = Array.isArray(f.provenance)
          ? f.provenance.map(p => p.chunk_index).join(",")
          : f.provenance.chunk_index;
        return `[${f.category}] ${f.fact} (source: chunk ${chunkRef})`;
      });
  }
}

module.exports = { FactStore };
