"""FastAPI backend for Pied Piper Legal Simulator"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json

import config
from src.agents import ClauseMatchAgent, NarrativeAgent
from src.database import DBManager

app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = DBManager()
clause_agent = ClauseMatchAgent()
narrative_agent = NarrativeAgent()


class SimulateRequest(BaseModel):
    episode_id: str
    mode: str = "all"  # "all", "vc_win", "founder_win", "winwin"


class SimulateResponse(BaseModel):
    episode: dict
    scenarios: dict
    alignment_scores: dict


@app.on_event("startup")
async def startup_event():
    """Load data on startup"""
    try:
        db.load_episodes("data/episodes.json")
        db.load_clauses("data/clauses.json")
        print("✅ Data loaded successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not load data - {e}")
        import traceback
        traceback.print_exc()


@app.get("/")
async def root():
    """Health check"""
    return {
        "app": config.APP_NAME,
        "version": config.APP_VERSION,
        "status": "running"
    }


@app.get("/episodes")
async def list_episodes():
    """List all available episodes"""
    episodes = db.get_all_episodes()
    return {"episodes": episodes}


@app.post("/simulate", response_model=SimulateResponse)
async def simulate(request: SimulateRequest):
    """
    Generate 3-scenario analysis for an episode
    
    Returns VC Win, Founder Win, and Win-Win versions with:
    - Relevant clauses
    - Trade-off narratives
    - Alignment scores
    """
    try:
        # Fetch episode
        episode = db.get_episode(request.episode_id)
        if not episode:
            raise HTTPException(status_code=404, detail="Episode not found")
        
        # Match clauses for all 3 scenarios
        clause_sets = clause_agent.match_clauses(episode)
        
        # Generate narratives for each scenario
        scenarios = {}
        alignment_scores = {}
        
        for scenario_type, clauses in clause_sets.items():
            if not clauses:
                scenarios[scenario_type] = {
                    "clauses": [],
                    "narrative": "No clauses available for this scenario.",
                    "clause_details": []
                }
                alignment_scores[scenario_type] = {
                    "vc": 50,
                    "founder": 50,
                    "balance": 50
                }
                continue
            
            # Generate narrative
            narrative = narrative_agent.summarize_scenario(
                episode, clauses, scenario_type
            )
            
            # Calculate alignment scores
            vc_score = clause_agent.get_alignment_score(clauses, "vc")
            founder_score = clause_agent.get_alignment_score(clauses, "founder")
            balance_score = clause_agent.get_alignment_score(clauses, "neutral")
            
            scenarios[scenario_type] = {
                "clauses": clauses,  # Return full clause objects, not just short_text
                "narrative": narrative,
                "clause_details": clauses
            }
            
            alignment_scores[scenario_type] = {
                "vc": vc_score,
                "founder": founder_score,
                "balance": balance_score
            }
            
            # Save to database for portfolio
            db.save_simulation(
                request.episode_id,
                scenario_type,
                clauses,
                narrative,
                alignment_scores[scenario_type]
            )
        
        return SimulateResponse(
            episode=episode,
            scenarios=scenarios,
            alignment_scores=alignment_scores
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/export/{episode_id}")
async def export_simulation(episode_id: str):
    """
    Export simulation as markdown for portfolio/resume use
    """
    episode = db.get_episode(episode_id)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    # Generate fresh simulation
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
            
            # Add alignment scores
            vc_score = clause_agent.get_alignment_score(clauses, "vc")
            founder_score = clause_agent.get_alignment_score(clauses, "founder")
            balance_score = clause_agent.get_alignment_score(clauses, "neutral")
            
            markdown += f"**Alignment:** VC: {vc_score}% | Founder: {founder_score}% | Balance: {balance_score}%\n\n"
        else:
            markdown += "*No clauses available*\n\n"
        
        markdown += "---\n\n"
    
    return {"markdown": markdown}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

