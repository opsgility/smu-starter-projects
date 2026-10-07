// FleetBoard operator roster — role-based task permissions
// See docs/architecture.md for the role-to-task permission map.

const VALID_ROLES = ['admin', 'developer', 'designer', 'qa'];

const operators = [
  { id: 1, handle: 'alex.kim',    name: 'Alex Kim',           role: 'developer' },
  { id: 2, handle: 'michael.p',   name: 'Michael Peters',     role: 'admin'     },
  { id: 3, handle: 'r.ortega',    name: 'Rosa Ortega',        role: 'qa'        },
  { id: 4, handle: 'j.sato',      name: 'Jun Sato',           role: 'designer'  },
  { id: 5, handle: 'nina.hassan', name: 'Nina Hassan',        role: 'developer' },
];

function getAll() {
  return operators;
}

function getById(id) {
  return operators.find(o => o.id === id) || null;
}

function getByHandle(handle) {
  return operators.find(o => o.handle === handle) || null;
}

function hasRole(operatorId, role) {
  const operator = getById(operatorId);
  return operator ? operator.role === role : false;
}

module.exports = { VALID_ROLES, getAll, getById, getByHandle, hasRole };
