#!/usr/bin/env bash
# Fire N requests against the APIM endpoint with a subscription key.
# Usage: KEY=... URL=... COUNT=1500 ./loadtest.sh
set -euo pipefail
: "${KEY:?}"; : "${URL:?}"
COUNT="${COUNT:-100}"
codes=$(for i in $(seq 1 "$COUNT"); do
  curl -s -o /dev/null -w "%{http_code}\n" -H "Ocp-Apim-Subscription-Key: $KEY" "$URL"
done | sort | uniq -c | sort -rn)
echo "Status distribution:"; echo "$codes"
