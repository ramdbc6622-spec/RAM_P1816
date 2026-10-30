#!/bin/sh
# Extract the solved-paper book column by column, one "@@PAGE n L|R" marker per column.
# Usage: tools/extract_source.sh SOURCE.pdf FIRST LAST > out.txt
pdf=$1; first=$2; last=$3
p=$first
while [ "$p" -le "$last" ]; do
  echo "@@PAGE $p L"; pdftotext -f "$p" -l "$p" -x 0 -y 30 -W 298 -H 780 "$pdf" -
  echo "@@PAGE $p R"; pdftotext -f "$p" -l "$p" -x 297 -y 30 -W 298 -H 780 "$pdf" -
  p=$((p + 1))
done
