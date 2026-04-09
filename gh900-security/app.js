// Simple application demonstrating input validation and XSS prevention
// This is the starting point for the security lab exercises

function validateInput(input) {
    if (typeof input !== 'string') {
        throw new Error('Input must be a string');
    }
    // Sanitize to prevent XSS — replace dangerous characters with HTML entities
    return input.replace(/[<>&"']/g, (char) => {
        const entities = { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' };
        return entities[char];
    });
}

module.exports = { validateInput };
