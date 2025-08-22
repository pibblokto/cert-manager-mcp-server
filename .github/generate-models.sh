#!/bin/bash
SCHEMA_DIR=$1
OUT_DIR="models/v1_18"
mkdir -p "$OUT_DIR"

for schema in "$SCHEMA_DIR"/*_schema.json; do
  base=$(basename "$schema" _schema.json)

  echo "Generating model: $base -> $OUT_DIR/${base}.py"

  datamodel-codegen \
    --input "$schema" \
    --input-file-type jsonschema \
    --output "$OUT_DIR/${base}.py" \
    --class-name "$base" \
    --field-constraints \
    --use-standard-collection \
    --output-model-type "pydantic_v2.BaseModel" \
    --target-python-version 3.12
done
