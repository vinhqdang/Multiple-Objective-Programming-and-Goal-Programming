#!/bin/bash
# Extract each quarterly SEC zip into <quarter>/, split files >90MB into .001/.002/... chunks, then delete the zip.
set -e
cd "$(dirname "$0")/financial_statements_data_us"
LIMIT=94371840   # 90 MiB
for z in *.zip; do
  q="${z%.zip}"
  mkdir -p "$q"
  unzip -oq "$z" -d "$q"
  for f in "$q"/*; do
    sz=$(stat -c %s "$f")
    if [ "$sz" -gt "$LIMIT" ]; then
      split -b "$LIMIT" -d -a 3 --numeric-suffixes=1 "$f" "$f."
      rm "$f"
    fi
  done
  rm "$z"
  echo "done $q"
done
