// FleetBoard utility helpers — single-line stubs the student will extend with Copilot ghost text.

// Return the robot in the fleet with the matching id, or null if not found
const getRobotById = (fleet, id) => fleet.find(r => r.id === id) || null;

// Count the robots whose status is 'active'
const countActiveRobots = (fleet) => fleet.filter(r => r.status === 'active').length;

// Format a robot as "<id> [<status>] battery=<n>%"
const formatRobotStatus = (robot) => `${robot.id} [${robot.status}] battery=${robot.batteryLevel}%`;

// Group robots by status into a { status: [robots] } map
const groupByStatus = (fleet) => fleet.reduce((acc, r) => { (acc[r.status] = acc[r.status] || []).push(r); return acc; }, {});

module.exports = { getRobotById, countActiveRobots, formatRobotStatus, groupByStatus };
