// TODO: Task 3/4 — Define test documents for the classifier
// Include clear-cut cases and intentionally ambiguous edge cases
// Each document should have: name (string), text (string), expectedCategory (optional)

const TEST_DOCUMENTS = [
  {
    name: "Standard Invoice",
    text: "INVOICE #2026-0501\nFrom: CloudScale Solutions\nTo: NovaPulse Technologies\nAmount: $47,500\nServices: Cloud migration consulting\nDue: Net 30",
    expectedCategory: "invoice"
  },
  {
    name: "Internal Memo",
    text: "MEMORANDUM\nTo: All Engineering Staff\nFrom: CTO\nRe: Q2 Architecture Review\nPlease prepare your service diagrams for the review on April 15th.",
    expectedCategory: "correspondence"
  },
  {
    name: "Services Agreement",
    text: "This Master Services Agreement is entered into between NovaPulse Technologies (Client) and DataFlow Inc (Provider) for data pipeline services...",
    expectedCategory: "contract"
  },
  // TODO: Task 4 — Add 2 ambiguous edge cases:
  //   1. A meeting transcript that discusses contract amendments
  //   2. A requirements document sent as an email with the header still present
];

module.exports = { TEST_DOCUMENTS };
