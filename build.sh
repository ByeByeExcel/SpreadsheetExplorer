#!/bin/bash

# Exit if any command fails
set -e

# Define input script and output paths
ENTRY_POINT="src/main.py"
DIST_DIR="out/dist"
BUILD_DIR="out/build"
ASSETS_DIR="assets"
NAME="SpreadsheetXplorer"

# Platform-specific data separator
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  SEP=";"
else
  SEP=":"
fi

# Clean old output
rm -rf "$DIST_DIR" "$BUILD_DIR"

# Run PyInstaller
pyinstaller "$ENTRY_POINT" \
  --windowed \
  --distpath "$DIST_DIR" \
  --workpath "$BUILD_DIR" \
  --add-data "${ASSETS_DIR}${SEP}assets" \
  --name "$NAME"

# Remove the .spec file
rm -f "$NAME".spec

echo "✅ Build complete. Executable is in $DIST_DIR"