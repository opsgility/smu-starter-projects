// TODO: Task 1 — Implement three-level validation for classification results
//
// validateStructure(result): check required fields exist and are valid types/values
//   - category must be in: ["invoice","contract","report","correspondence","technical_spec"]
//   - confidence must be 0-1 number
//   - reasoning must be present
//   - metadata must be present
//   Return: { valid: boolean, errors: string[], level: "structural" }
//
// validateSemantics(result): check reasoning vs confidence consistency and metadata consistency
//   - confidence > 0.9 but reasoning expresses uncertainty -> error
//   - confidence < 0.5 but reasoning says "clearly"/"obviously" -> error
//   - invoice without has_financial_data -> error
//   - contract without has_legal_terms -> error
//   Return: { valid: boolean, errors: string[], level: "semantic" }
//
// validateBusinessRules(result): check business-level constraints
//   - reasoning must be >= 20 characters
//   - primary_entities must not be empty
//   Return: { valid: boolean, errors: string[], level: "business" }

function validateStructure(result) {
  const errors = [];

  // TODO: implement structural validation

  return { valid: errors.length === 0, errors, level: "structural" };
}

function validateSemantics(result) {
  const errors = [];

  // TODO: implement semantic validation

  return { valid: errors.length === 0, errors, level: "semantic" };
}

function validateBusinessRules(result) {
  const errors = [];

  // TODO: implement business rule validation

  return { valid: errors.length === 0, errors, level: "business" };
}

module.exports = { validateStructure, validateSemantics, validateBusinessRules };
