#!/bin/bash
# Script to copy AEO framework files to your workspace

# Change this to your actual workspace path
WORKSPACE_PATH="/Users/maxb/Desktop/Vibe Projects/aeo-optimizer-business"

# Create directories
mkdir -p "$WORKSPACE_PATH/business-plans/aeo-framework"

# Copy all files
cp -r /workspace/business-plans/aeo-framework/* "$WORKSPACE_PATH/business-plans/aeo-framework/"

echo "Files copied to: $WORKSPACE_PATH/business-plans/aeo-framework/"
echo "Total files: $(ls -1 "$WORKSPACE_PATH/business-plans/aeo-framework/" | wc -l)"
