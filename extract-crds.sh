#!/bin/bash
set -euo pipefail

KINDS=("Certificate" "Issuer" "ClusterIssuer" "CertificateRequest" "Order" "Challenge")
TMP="json-crds"
mkdir -p "$TMP"

echo "Downloading cert-manager CRDs..."
curl -L -o "$TMP/crds.yaml" https://github.com/cert-manager/cert-manager/releases/download/v1.18.2/cert-manager.crds.yaml

for kind in "${KINDS[@]}"; do
  lower_kind=$(echo "$kind" | tr '[:upper:]' '[:lower:]')
  out="$TMP/${lower_kind}_schema.json"
  echo "Extracting schema for: $kind -> $out"

  yq -o=json 'select(.spec.names.kind == "'"$kind"'") |
    .spec.versions[] |
    select(.name == "v1") |
    .schema.openAPIV3Schema' "$TMP/crds.yaml" > "$out"
done
