// ForgeBoard Utility Functions
// All functions are written on single compressed lines intentionally —
// use Copilot's /explain command to understand what each one does.

const formatDate = (d) => { const x = new Date(d); return `${x.getFullYear()}-${String(x.getMonth()+1).padStart(2,'0')}-${String(x.getDate()).padStart(2,'0')}`; };
const truncateText = (text, maxLength) => text.length <= maxLength ? text : text.substring(0, maxLength - 3) + '...';
const generateSlug = (text) => text.toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/^-+|-+$/g, '');
const formatRelativeTime = (date) => { const days = Math.floor((Date.now() - new Date(date)) / 86400000); if (days === 0) return 'today'; if (days === 1) return 'yesterday'; return `${days} days ago`; };
const isValidPriority = (p) => ['low', 'medium', 'high', 'critical'].includes(p);

module.exports = { formatDate, truncateText, generateSlug, formatRelativeTime, isValidPriority };
