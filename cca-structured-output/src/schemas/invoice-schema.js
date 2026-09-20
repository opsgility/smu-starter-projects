// TODO: Task 3 — Define the EXTRACT_INVOICE_TOOL schema for structured invoice extraction
//
// Tool name: "extract_invoice"
// Description: extract structured data from invoice documents including line items
// input_schema properties:
//   - invoice_number: string
//   - vendor: string
//   - recipient: string
//   - date_issued: string (ISO 8601 YYYY-MM-DD)
//   - due_date: string (ISO 8601)
//   - line_items: array of objects, each with description, quantity, unit_price, total
//   - subtotal: number
//   - tax: number (0 if not specified)
//   - total: number
//   - currency: string, enum ["USD","EUR","GBP","CAD","AUD"]
//   - payment_terms: string
// Required: invoice_number, vendor, total, currency, line_items

const EXTRACT_INVOICE_TOOL = {
  name: "extract_invoice",
  description: "Extract structured data from an invoice document including line items, totals, and payment terms.",
  input_schema: {
    type: "object",
    properties: {
      // TODO: implement all properties as described above
    },
    required: ["invoice_number", "vendor", "total", "currency", "line_items"]
  }
};

module.exports = { EXTRACT_INVOICE_TOOL };
