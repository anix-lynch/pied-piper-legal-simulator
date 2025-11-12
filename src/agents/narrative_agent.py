"""NarrativeAgent: Generates trade-off summaries for each scenario"""
from typing import Dict, List
import anthropic
import config


class NarrativeAgent:
    """Generates natural language summaries of clause trade-offs"""
    
    def __init__(self):
        # Only initialize if API key is available
        if config.ANTHROPIC_API_KEY:
            self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        else:
            self.client = None
    
    def summarize_scenario(
        self, 
        episode: Dict, 
        clauses: List[Dict], 
        scenario_type: str
    ) -> str:
        """
        Generate a narrative summary for one scenario
        
        Args:
            episode: Episode data
            clauses: List of clauses for this scenario
            scenario_type: "vc_win", "founder_win", or "winwin"
            
        Returns:
            Natural language summary of trade-offs
        """
        # Build context for Claude
        episode_context = f"""
Episode: {episode['episode_id']} - {episode['title']}
Conflict: {episode['conflict_type']}
Scene: {episode['scene']}
Legal Stakes: {episode['legal_stakes']}
"""
        
        clause_context = "\n".join([
            f"- {c['short_text']}: {c['explanation']}"
            for c in clauses
        ])
        
        scenario_names = {
            "vc_win": "VC Win (VC-favorable terms)",
            "founder_win": "Founder Win (Founder-favorable terms)",
            "winwin": "Win-Win (Balanced terms)"
        }
        
        prompt = f"""You are a venture capital legal expert analyzing term sheet outcomes from the TV show "Silicon Valley."

{episode_context}

Scenario: {scenario_names.get(scenario_type, scenario_type)}

Clauses in this scenario:
{clause_context}

Write a concise 2-3 sentence summary explaining:
1. What this outcome means for Richard (the founder)
2. What this outcome means for the VCs
3. The key trade-off or risk in this scenario

Keep it conversational and reference the show's context. Use "you" for Richard's perspective."""

        # Use fallback if no API key configured
        if not self.client:
            return self._fallback_summary(clauses, scenario_type)
        
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=config.TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            # Fallback if API fails
            return self._fallback_summary(clauses, scenario_type)
    
    def _fallback_summary(self, clauses: List[Dict], scenario_type: str) -> str:
        """Generate simple summary without AI if API unavailable"""
        if scenario_type == "vc_win":
            return "VCs secure maximum control and downside protection. Founders face higher dilution risk and limited control. Trade-off: runway vs autonomy."
        elif scenario_type == "founder_win":
            return "Founder retains control and favorable economics. VCs accept higher risk for potential upside. Trade-off: VC comfort vs founder independence."
        else:
            return "Balanced structure requiring mutual consent on key decisions. Both sides protected but neither dominates. Trade-off: consensus overhead vs alignment."

