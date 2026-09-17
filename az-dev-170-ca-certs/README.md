# az-dev-170-ca-certs

Web app that:
1. Reads its client credential from Key Vault (certificate rather than string secret).
2. Handles Conditional Access step-up via a claims-challenge redirect on `POST /orders/refund`.
