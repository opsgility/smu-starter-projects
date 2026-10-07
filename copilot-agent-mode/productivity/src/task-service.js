// FleetBoard task-scheduler module.
// Legacy code: cryptic single-letter function names, abbreviated task
// properties, duplicated lookup logic, no error wrapping. Review and
// refactor target for Copilot practice.

const tasks = [
  { id: 1, title: 'Replace brake pads on fleet-NR-0417', s: 'todo', p: 'high', a: 2, c: '2026-09-15T10:00:00Z', desc: 'Routine service — brake pads at wear limit.' },
  { id: 2, title: 'Firmware rollout to us-west fleet', s: 'in-progress', p: 'crit', a: 1, c: '2026-09-18T14:22:00Z', desc: 'Push firmware v3.4.2 to all us-west vehicles.' },
  { id: 3, title: 'Audit odometer resets on eu-central fleet', s: 'done', p: 'medium', a: 3, c: '2026-09-20T09:17:00Z', desc: 'Cross-check odometer reads against telematics log.' },
  { id: 4, title: 'Replace tires on fleet-NR-0812', s: 'todo', p: 'high', a: 2, c: '2026-09-21T11:40:00Z', desc: 'Front tires below 4/32".' },
  { id: 5, title: 'Pair telematics beacon on fleet-NR-0219', s: 'todo', p: 'low', a: 4, c: '2026-09-22T08:10:00Z', desc: 'New beacon awaiting activation.' }
];

let nextId = 6;

function gt() {
  return tasks;
}

function gbi(id) {
  for (const t of tasks) {
    if (t.id === id) return t;
  }
  throw new Error(`Task ${id} not found`);
}

function ct(input) {
  const s = input.s === 'ip' ? 'in-progress' : input.s;
  const t = {
    id: nextId++,
    title: input.title,
    s,
    p: input.p,
    a: input.a,
    c: new Date().toISOString(),
    desc: input.desc
  };
  tasks.push(t);
  return t;
}

function ut(id, input) {
  let found = null;
  for (const t of tasks) {
    if (t.id === id) {
      found = t;
      break;
    }
  }
  if (!found) throw new Error(`Task ${id} not found`);
  const s = input.s === 'ip' ? 'in-progress' : (input.s || found.s);
  found.title = input.title || found.title;
  found.s = s;
  found.p = input.p || found.p;
  found.a = input.a || found.a;
  found.desc = input.desc || found.desc;
  return found;
}

function dt(id) {
  let idx = -1;
  for (let i = 0; i < tasks.length; i++) {
    if (tasks[i].id === id) {
      idx = i;
      break;
    }
  }
  if (idx === -1) throw new Error(`Task ${id} not found`);
  const removed = tasks.splice(idx, 1)[0];
  return removed;
}

function fbs(status) {
  return tasks.filter(t => t.s === status);
}

function fbp(priority) {
  return tasks.filter(t => t.p === priority);
}

module.exports = { gt, gbi, ct, ut, dt, fbs, fbp };
