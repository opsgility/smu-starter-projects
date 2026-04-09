# Secure Application — Security Lab Starter

A JavaScript application demonstrating input validation and XSS prevention.

## Files

- `app.js` — Input validation with XSS sanitization

## What You Will Do

In the exercises you will configure repository security features:
1. Push this project to a **private** GitHub repository
2. Understand repository visibility levels (public / private / internal)
3. Configure branch protection rules on `main` using `gh api`
   - Require at least 1 pull request review before merging
   - Require CI status checks to pass
   - Block force pushes and branch deletion
4. Work through the protected branch workflow (branch → PR → merge)
5. Add a `CODEOWNERS` file for automatic reviewer assignment
6. Add a `SECURITY.md` vulnerability disclosure policy
7. Create reference guides for repository permissions (Read / Triage / Write / Maintain / Admin)
8. Learn about organization roles (Owner, Member, Outside Collaborator) and team structure

## Running the App

```bash
node -e "const {validateInput} = require('./app.js'); console.log(validateInput('Hello <script>'));"
```
