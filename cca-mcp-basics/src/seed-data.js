// TODO: Task 5 — Implement seedDocuments(store) to pre-populate the document store
// Call this function from server.js before starting the transport
// to ensure the store has sample data for testing
//
// Each document needs: title, content, category, author
// Include at least 3 documents covering different categories:
//   - An invoice
//   - A contract/NDA
//   - A report
//
// The store parameter is the documentStore Map from server.js
// Use store.set(id, { ...doc, id, created_at, status: "active" }) or a helper function

function seedDocuments(documentStore, getNextId) {
  const docs = [
    {
      title: "Q1 Cloud Hosting Invoice",
      content: "Invoice #2026-001 from CloudServe Inc.\nAmount Due: $12,500\nServices: Cloud infrastructure hosting, January-March 2026\nPayment Terms: Net 30",
      category: "invoice",
      author: "CloudServe Inc."
    },
    {
      title: "NDA - TechVentures Partnership",
      content: "Non-Disclosure Agreement between NovaPulse Technologies Inc. and TechVentures Ltd.\nEffective Date: January 1, 2026\nBoth parties agree to maintain confidentiality of all shared proprietary information for a period of 3 years.",
      category: "contract",
      author: "Legal Dept"
    },
    {
      title: "Sprint Velocity Report - March 2026",
      content: "Engineering velocity for March 2026.\nSprint completion rate: 92%\nBlocked items: 2\nKey achievement: DocStream v2.1 deployed to production.\nNext sprint focus: performance optimization.",
      category: "report",
      author: "Engineering"
    }
    // TODO: add more seed documents if desired
  ];

  for (const doc of docs) {
    const id = getNextId();
    documentStore.set(id, {
      ...doc,
      id,
      created_at: new Date().toISOString(),
      status: "active"
    });
  }

  console.error(`[Seed] Loaded ${docs.length} documents into store`);
}

module.exports = { seedDocuments };
