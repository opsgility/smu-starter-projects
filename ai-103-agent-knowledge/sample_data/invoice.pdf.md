# invoice.pdf (placeholder)

**This markdown file is a stand-in.** The actual file Exercise 3 analyzes
is `sample_data/invoice.pdf`. The lab environment seeds that PDF before
the learner starts. If it is missing, any vendor invoice PDF with legible
text will do.

## Expected content

A single-page vendor invoice addressed to Summitline Outfitters. The
Content Understanding analyzer is configured to extract:

| Field          | Example                              |
| -------------- | ------------------------------------ |
| `VendorName`   | Cascadia Textile Supply Co.          |
| `InvoiceDate`  | 2025-11-03                           |
| `InvoiceTotal` | 4,287.50                             |
| `LineItems`    | Bolt - 400D ripstop nylon, 1,450.00  |
|                | Zipper assemblies (100 ct), 612.00   |
|                | Reflective trim spool, 225.50        |

When the agent answers "Summarize the invoice in sample_data/invoice.pdf.",
the reply should include the vendor name, invoice total, date, and at
least one line item.
