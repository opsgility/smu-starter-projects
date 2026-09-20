// Simple app for CI demo
// The CI workflow will run test.js automatically on every push and pull request

function add(a, b) {
    return a + b;
}

function multiply(a, b) {
    return a * b;
}

// TODO (feature/add-subtract): add subtract(a, b) function with tests
// TODO (feature/buggy-divide): add divide(a, b) function — watch the CI catch the bug!

module.exports = { add, multiply };
