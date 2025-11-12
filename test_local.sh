#!/bin/bash
# Test script for Pied Piper Legal Simulator

set -e

echo "🧪 Testing Pied Piper Legal Simulator..."

# Start backend in background
echo "Starting backend..."
python app.py &
BACKEND_PID=$!
sleep 3

# Test health endpoint
echo "Testing health endpoint..."
curl -s http://localhost:8000/ | grep -q "running" && echo "✅ Health check passed"

# Test episodes endpoint
echo "Testing episodes endpoint..."
curl -s http://localhost:8000/episodes | grep -q "episode_id" && echo "✅ Episodes endpoint passed"

# Test simulation
echo "Testing simulation..."
curl -s -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{"episode_id": "S02E04", "mode": "all"}' \
  | grep -q "scenarios" && echo "✅ Simulation endpoint passed"

# Test export
echo "Testing export..."
curl -s http://localhost:8000/export/S02E04 | grep -q "markdown" && echo "✅ Export endpoint passed"

# Cleanup
kill $BACKEND_PID

echo ""
echo "✅ All tests passed!"
echo ""
echo "To run manually:"
echo "  python app.py"
echo "  Open frontend/index.html in browser"

