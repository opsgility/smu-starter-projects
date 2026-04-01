function validateEmail(email) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); }

function validateTaskTitle(title) {
  if (!title || typeof title !== 'string') return { valid: false, error: 'Title is required' };
  const trimmed = title.trim();
  if (trimmed.length < 3) return { valid: false, error: 'Title must be at least 3 characters' };
  if (trimmed.length > 200) return { valid: false, error: 'Title must be under 200 characters' };
  return { valid: true, value: trimmed };
}

function validatePriority(priority) { return ['low', 'medium', 'high', 'critical'].includes(priority); }

function validateDateRange(startDate, endDate) {
  const start = new Date(startDate); const end = new Date(endDate);
  if (isNaN(start.getTime())) return { valid: false, error: 'Invalid start date' };
  if (isNaN(end.getTime())) return { valid: false, error: 'Invalid end date' };
  if (end <= start) return { valid: false, error: 'End date must be after start date' };
  return { valid: true, start, end };
}

module.exports = { validateEmail, validateTaskTitle, validatePriority, validateDateRange };
