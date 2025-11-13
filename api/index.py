"""Vercel serverless API for Pied Piper Legal Simulator"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
from pathlib import Path

# FastAPI app
app = FastAPI(title="Pied Piper Legal Simulator API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data from JSON files (no DuckDB on serverless)
DATA_DIR = Path(__file__).parent.parent / "data"

def load_json(filename):
    """Load JSON data file"""
    try:
        with open(DATA_DIR / filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

EPISODES = load_json("episodes.json")
CLAUSES = load_json("clauses.json")


class SimulateRequest(BaseModel):
    episode_id: str
    mode: str = "all"


class ClauseMatchAgent:
    """Matches episode conflicts to relevant clauses"""
    
    def __init__(self, clauses):
        self.clauses = clauses
    
    def match_clauses(self, episode):
        """Return 3 clause sets: VC win, Founder win, Win-Win"""
        conflict_type = episode.get("conflict_type")
        
        # Filter by conflict type
        relevant = [c for c in self.clauses if c["conflict_type"] == conflict_type]
        
        # Separate by bias
        return {
            "vc_win": [c for c in relevant if c["bias"] == "VC_bias"],
            "founder_win": [c for c in relevant if c["bias"] == "Founder_bias"],
            "winwin": [c for c in relevant if c["bias"] == "Neutral"]
        }
    
    def get_alignment_score(self, clauses, perspective):
        """Calculate alignment score (0-100)"""
        if not clauses:
            return 50
        
        if perspective == "vc":
            avg_risk = sum(c["risk_score_founder"] for c in clauses) / len(clauses)
            return int(avg_risk)
        elif perspective == "founder":
            avg_risk = sum(c["risk_score_vc"] for c in clauses) / len(clauses)
            return int(avg_risk)
        else:
            avg_f = sum(c["risk_score_founder"] for c in clauses) / len(clauses)
            avg_v = sum(c["risk_score_vc"] for c in clauses) / len(clauses)
            return int(100 - abs(avg_f - avg_v))


class NarrativeAgent:
    """Generates trade-off summaries"""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except:
                pass
    
    def summarize_scenario(self, episode, clauses, scenario_type):
        """Generate narrative summary"""
        # Use fallback for now (Claude optional)
        episode_title = episode.get("title", "")
        conflict_type = episode.get("conflict_type", "")
        return self._fallback_summary(clauses, scenario_type, episode_title, conflict_type)
    
    def _fallback_summary(self, clauses, scenario_type, episode_title="", conflict_type=""):
        """Episode-specific summary with conflict-type awareness"""
        
        # Create conflict-specific narratives
        conflict_narratives = {
            "board_control": {
                "vc_win": f"In '{episode_title}', VCs lock down board majority. Founders become employees of their own company. Like when Raviga tried to replace Richard - this is how they do it legally through board composition clauses.",
                "founder_win": f"In '{episode_title}', founders secure board control with protective provisions. Dual-class shares keep voting power with Richard. This is the 'middle fingers up' moment - founders can't be voted out.",
                "winwin": f"In '{episode_title}', board seats split evenly with independent tie-breaker. Both sides need to agree on major decisions. It's the fantasy scenario where everyone plays nice."
            },
            "funding_terms": {
                "vc_win": f"In '{episode_title}', VCs demand 2x liquidation preference and full ratchet anti-dilution. Founders get crushed on down-rounds. This is Peter Gregory territory - aggressive terms for runway.",
                "founder_win": f"In '{episode_title}', founders negotiate 1x participating preferred with broad-based weighted average anti-dilution. They maintain equity and upside. Richard actually wins the valuation game.",
                "winwin": f"In '{episode_title}', standard market terms with 1x non-participating liquidation preference. Both sides share upside fairly. The mythical 'fair deal' that Silicon Valley pretends exists."
            },
            "founder_vesting": {
                "vc_win": f"In '{episode_title}', VCs impose 4-year vesting with 1-year cliff and no acceleration. Founders lose equity if they leave. Erlich's nightmare - they can take your shares away.",
                "founder_win": f"In '{episode_title}', founders get reverse vesting with single-trigger acceleration on acquisition. They're protected if VCs push them out. Erlich keeps his 10% no matter what.",
                "winwin": f"In '{episode_title}', standard vesting with double-trigger acceleration. Both sides protected but neither can exploit the other. The compromise nobody actually likes."
            },
            "ip_ownership": {
                "vc_win": f"In '{episode_title}', all IP assigned to company with VCs controlling licensing. Founders can't use their own tech if they leave. Hooli's wet dream - they own everything.",
                "founder_win": f"In '{episode_title}', founders retain personal IP rights with exclusive licensing to company. They keep leverage if things go south. Richard proves he built it independently.",
                "winwin": f"In '{episode_title}', joint IP ownership with fair licensing terms. Both sides can use the tech under specific conditions. Patent attorneys make millions sorting this out."
            },
            "liquidation_event": {
                "vc_win": f"In '{episode_title}', VCs get 2-3x liquidation preference with participation rights. They make money even if founders get nothing. That Hooli acquisition offer? VCs take it all.",
                "founder_win": f"In '{episode_title}', founders negotiate 1x non-participating preference and anti-cramdown provisions. Common stock actually matters. Richard can say no to bad acquisitions.",
                "winwin": f"In '{episode_title}', 1.5x participating with cap at 2x investment. Both sides share downside and upside reasonably. The spreadsheet that makes everyone equally unhappy."
            },
            "seed_funding": {
                "vc_win": f"In '{episode_title}', early investors take 25%+ equity for minimal cash. High valuation cap on SAFE notes crushes founders later. That $250K costs you the company.",
                "founder_win": f"In '{episode_title}', founders raise on favorable SAFE terms with low discount and high cap. They keep ownership and control. Building product first actually works.",
                "winwin": f"In '{episode_title}', standard Y Combinator SAFE with 20% discount and reasonable cap. Industry-standard seed terms that don't screw anyone. Boring but functional."
            }
        }
        
        # Get narratives for this conflict type or use generic
        narratives = conflict_narratives.get(conflict_type, {
            "vc_win": f"In '{episode_title}', VCs secure maximum control. Founders face higher dilution and limited board power. Investors hold all the cards.",
            "founder_win": f"In '{episode_title}', founders retain control with protective provisions. VCs accept higher risk for upside. This is that middle-fingers-up energy.",
            "winwin": f"In '{episode_title}', balanced terms require mutual consent. Both sides protected but neither dominates. The unicorn deal that rarely happens."
        })
        
        return narratives.get(scenario_type, f"Standard {scenario_type} terms for this scenario.")


# Initialize agents
clause_agent = ClauseMatchAgent(CLAUSES)
narrative_agent = NarrativeAgent()


@app.get("/")
async def root():
    """Health check"""
    return {
        "app": "Pied Piper Legal Simulator API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/episodes", "/simulate", "/export/{episode_id}"]
    }


@app.get("/episodes")
async def list_episodes():
    """List all available episodes"""
    return {"episodes": EPISODES}


@app.post("/simulate")
async def simulate(request: SimulateRequest):
    """Generate 3-scenario analysis"""
    try:
        # Find episode
        episode = next((e for e in EPISODES if e["episode_id"] == request.episode_id), None)
        if not episode:
            raise HTTPException(status_code=404, detail="Episode not found")
        
        # Match clauses
        clause_sets = clause_agent.match_clauses(episode)
        
        # Generate scenarios
        scenarios = {}
        alignment_scores = {}
        
        for scenario_type, clauses in clause_sets.items():
            if not clauses:
                scenarios[scenario_type] = {
                    "clauses": [],
                    "narrative": "No clauses available.",
                    "clause_details": []
                }
                alignment_scores[scenario_type] = {"vc": 50, "founder": 50, "balance": 50}
                continue
            
            narrative = narrative_agent.summarize_scenario(episode, clauses, scenario_type)
            
            scenarios[scenario_type] = {
                "clauses": clauses,  # Return full clause objects, not just short_text
                "narrative": narrative,
                "clause_details": clauses
            }
            
            alignment_scores[scenario_type] = {
                "vc": clause_agent.get_alignment_score(clauses, "vc"),
                "founder": clause_agent.get_alignment_score(clauses, "founder"),
                "balance": clause_agent.get_alignment_score(clauses, "neutral")
            }
        
        return {
            "episode": episode,
            "scenarios": scenarios,
            "alignment_scores": alignment_scores
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/export/{episode_id}")
async def export_simulation(episode_id: str):
    """Export simulation as markdown"""
    episode = next((e for e in EPISODES if e["episode_id"] == episode_id), None)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    clause_sets = clause_agent.match_clauses(episode)
    
    markdown = f"""# Pied Piper Legal Simulator

## Episode: {episode['title']} ({episode['episode_id']})

**Conflict:** {episode['conflict_type']}  
**Scene:** {episode['scene']}  
**Legal Stakes:** {episode['legal_stakes']}

---

"""
    
    scenario_names = {
        "vc_win": "💰 VC WIN",
        "founder_win": "💡 FOUNDER WIN",
        "winwin": "🤝 WIN-WIN"
    }
    
    for scenario_type, clauses in clause_sets.items():
        markdown += f"### {scenario_names.get(scenario_type)}\n\n"
        
        if clauses:
            for clause in clauses:
                markdown += f"- **{clause['clause_type']}:** {clause['short_text']}\n"
                markdown += f"  - {clause['explanation']}\n"
                markdown += f"  - Risk (Founder): {clause['risk_score_founder']}% | Risk (VC): {clause['risk_score_vc']}%\n\n"
            
            vc_score = clause_agent.get_alignment_score(clauses, "vc")
            founder_score = clause_agent.get_alignment_score(clauses, "founder")
            balance_score = clause_agent.get_alignment_score(clauses, "neutral")
            
            markdown += f"**Alignment:** VC: {vc_score}% | Founder: {founder_score}% | Balance: {balance_score}%\n\n"
        
        markdown += "---\n\n"
    
    return {"markdown": markdown}


# Export app for Vercel
# Vercel will automatically detect and serve the FastAPI app

