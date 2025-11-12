# Pied Piper Legal Simulator

**Interactive VC negotiation simulator with AI agents analyzing 15+ term-sheet clauses across 3 outcomes**

## 🎯 What It Does

Teaches venture capital & founder negotiation through Silicon Valley scenarios. Each episode conflict generates 3 outcomes:
- **💰 VC Win**: VC-favorable terms (max control, downside protection)
- **💡 Founder Win**: Founder-favorable terms (control retention, favorable economics)  
- **🤝 Win-Win**: Balanced terms (mutual consent, neither dominates)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (React + TailwindCSS)                              │
│  ├─ Episode Selector                                         │
│  ├─ 3-Panel Outcome Display                                  │
│  └─ Markdown Export                                          │
└─────────────────────────────────────────────────────────────┘
                           ↓ FastAPI
┌─────────────────────────────────────────────────────────────┐
│  AI Agents                                                   │
│  ├─ ClauseMatchAgent: Filters clauses by bias               │
│  └─ NarrativeAgent: Claude-powered trade-off summaries      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Data Layer                                                  │
│  ├─ DuckDB: Episodes, clauses, simulations                   │
│  └─ Optional: Supabase for cloud persistence                │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Model

**Episodes** (5 Silicon Valley scenarios)
- Board Coup (S02E04)
- Funding Terms (S01E08)
- Founder Vesting (S03E01)
- IP Ownership (S04E03)
- Liquidation Event (S02E10)

**Clauses** (15+ real term-sheet provisions)
- Board composition, liquidation preferences, vesting schedules
- IP assignment, anti-dilution, drag-along rights
- Each tagged with `VC_bias`, `Founder_bias`, or `Neutral`

**Simulations** (persisted outputs)
- Stores all 3 scenarios per episode
- Includes clauses, narratives, alignment scores
- Exportable as markdown for portfolio/resume

## 🧠 AI Agent Logic

### ClauseMatchAgent
```python
def match_clauses(episode):
    conflict_type = episode.conflict_type  # e.g. "board_control"
    
    # Filter by conflict + bias
    vc_win = filter(clauses, bias="VC_bias", conflict=conflict_type)
    founder_win = filter(clauses, bias="Founder_bias", conflict=conflict_type)
    winwin = filter(clauses, bias="Neutral", conflict=conflict_type)
    
    return {vc_win, founder_win, winwin}
```

### NarrativeAgent
```python
def summarize_scenario(episode, clauses, scenario_type):
    prompt = f"""
    Episode: {episode.title}
    Scenario: {scenario_type}
    Clauses: {clauses}
    
    Explain:
    1. What this means for Richard (founder)
    2. What this means for VCs
    3. Key trade-off/risk
    """
    
    return claude.generate(prompt) or fallback_summary()
```

## 🔢 Alignment Scores

**VC Alignment**: Higher = more founder risk (VC-favorable)  
**Founder Alignment**: Higher = more VC risk (founder-favorable)  
**Balance Score**: 100 - abs(vc_risk - founder_risk)

Example:
```json
{
  "vc_win": { "vc": 90, "founder": 10, "balance": 20 },
  "founder_win": { "vc": 20, "founder": 85, "balance": 35 },
  "winwin": { "vc": 50, "founder": 50, "balance": 100 }
}
```

## 🚀 Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | React + TailwindCSS | Fast prototyping, modern UI |
| **Backend** | FastAPI + Python | Async, type-safe, fast |
| **AI** | Anthropic Claude 3.5 | Best legal reasoning |
| **Database** | DuckDB | Embedded, SQL, perfect for local |
| **Deploy** | Vercel | Free, instant, global CDN |

## 📈 Business Value

**For Founders:**
- Understand VC term sheets before negotiation
- Visualize trade-offs across 3 negotiation stances
- Export scenarios to share with lawyers/co-founders

**For VCs:**
- Demonstrate firm's founder-friendly approach
- Educational content for portfolio companies
- Thought leadership on fair deal structures

**For Legal Professionals:**
- Interactive training tool for associates
- Client education on term sheet dynamics
- Case studies from recognizable pop culture

## 🎓 Resume Hook

> "Built legal simulator with AI agents analyzing 15+ VC term-sheet clauses across 3 negotiation outcomes (VC-favorable, founder-favorable, balanced), demonstrating venture dynamics through Silicon Valley storytelling. FastAPI + Claude + DuckDB + React."

## 📦 Deliverables

- ✅ 5 episode scenarios (board, funding, vesting, IP, liquidation)
- ✅ 15 term-sheet clauses with bias tagging
- ✅ 2 AI agents (ClauseMatch + Narrative)
- ✅ FastAPI backend with 4 endpoints
- ✅ React frontend with 3-panel display
- ✅ DuckDB persistence layer
- ✅ Markdown export for portfolio

## 🔗 Deployment

**Local:**
```bash
python app.py  # Backend on :8000
cd frontend && python -m http.server 3000
```

**Vercel:**
```bash
vercel --prod
```

**Portfolio Addition:**
```js
// www.gozeroshot.dev/src/pages/index.astro
{
  title: "Pied Piper Legal Simulator",
  desc: "Interactive VC negotiation with AI agents",
  link: "https://pied-piper-legal.vercel.app",
  tags: ["Legal Tech", "AI Agents", "FastAPI", "Claude"]
}
```

## 🎯 Next Steps (Optional)

1. **More Episodes**: Add 10+ more Silicon Valley scenarios
2. **Supabase Sync**: Persist simulations to cloud
3. **User Auth**: Save personal simulations
4. **PDF Export**: Generate professional term-sheet PDFs
5. **Clause Library**: Expand to 50+ clauses from real deals
6. **Advisor Mode**: Claude generates custom negotiation advice
7. **Resume MCP Integration**: Add as "Legal Intelligence" skill

---

**Total Build Time**: ~2 hours  
**Lines of Code**: ~800 Python, ~200 React  
**Free Tier**: ✅ Anthropic, ✅ DuckDB, ✅ Vercel

