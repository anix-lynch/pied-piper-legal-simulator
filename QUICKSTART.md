# Pied Piper Legal Simulator - Quick Start

Interactive legal simulator teaching VC & founder negotiation through Silicon Valley scenarios.

## Setup (1 minute)

```bash
# 1. Install dependencies
cd /Users/anixlynch/dev/coursera-portfolio-projects/pied-piper-legal-simulator
source venv/bin/activate
pip install -r requirements.txt

# 2. Verify API key in ~/.config/secrets/global.env
# Should have: ANTHROPIC_API_KEY=sk-ant-...

# 3. Start backend
python app.py
```

## Usage

```bash
# Terminal 1: Start FastAPI backend
python app.py

# Terminal 2: Serve frontend
cd frontend
python -m http.server 3000

# Open: http://localhost:3000
```

## Features

- **3 Scenario Generator**: VC Win 💰 | Founder Win 💡 | Win-Win 🤝
- **5 Episodes**: Board control, funding terms, vesting, IP, liquidation
- **15+ Clauses**: Real term-sheet language with bias tagging
- **AI Narratives**: Claude-powered trade-off summaries
- **Export**: Markdown output for portfolio/resume

## API Endpoints

```bash
# List episodes
curl http://localhost:8000/episodes

# Run simulation
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{"episode_id": "S02E04", "mode": "all"}'

# Export markdown
curl http://localhost:8000/export/S02E04
```

## Architecture

```
Frontend (HTML/React) → FastAPI → Agents (ClauseMatch, Narrative) → DuckDB
```

**Agents:**
- `ClauseMatchAgent`: Filters clauses by bias (VC/Founder/Neutral)
- `NarrativeAgent`: Claude-powered trade-off summaries

**Data:**
- `data/episodes.json`: 5 Silicon Valley scenarios
- `data/clauses.json`: 15+ term-sheet clauses
- `data/legal_simulator.duckdb`: Persistent storage

## Deploy

**Vercel (Frontend + API):**
```bash
vercel --prod
```

**Add to Portfolio:**
```js
// www.gozeroshot.dev/src/pages/index.astro
{
  title: "Pied Piper Legal Simulator",
  desc: "Interactive VC negotiation scenarios",
  link: "https://pied-piper-legal.vercel.app",
  tags: ["Legal Tech", "AI Agents", "FastAPI"]
}
```

## Resume Hook

"Built legal simulator with AI agents analyzing 15+ VC term-sheet clauses across 3 negotiation outcomes (VC-favorable, founder-favorable, balanced), demonstrating venture dynamics through Silicon Valley storytelling."

