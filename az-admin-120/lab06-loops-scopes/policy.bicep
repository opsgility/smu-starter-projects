// SMU-BICEP-FUND Lab 06 — starter policy.bicep (SUBSCRIPTION SCOPE)
//
// This file is empty by design. You author it in Exercise 4:
//
//   1. Set targetScope = 'subscription'.
//   2. Declare a Microsoft.Authorization/policyAssignments@2023-04-01 resource
//      that assigns the built-in "Not allowed resource types" policy definition
//      (id: 6c112d4e-5bc7-47ae-a041-ea2d9dccd749).
//   3. Configure its `listOfResourceTypesNotAllowed` parameter to a single-
//      element array containing the string 'Microsoft.Network/publicIPAddresses'.
//   4. Give the assignment a stable, human-readable displayName.
//
// You deploy it in Exercise 5 with:
//   az deployment sub create --location <region> -f policy.bicep
//
// See README.md and the exercise pane for full guidance.
