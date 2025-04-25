#!/bin/bash

echo "Cleaning logs and rebuilding MCP cache..."

rm -rf logs/*
rm -rf __pycache__/
rm -rf .mcp_cache

echo "Done."
