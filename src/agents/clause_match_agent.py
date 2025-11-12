"""ClauseMatchAgent: Matches conflicts to clauses with bias filtering"""
import json
from typing import Dict, List
from pathlib import Path


class ClauseMatchAgent:
    """Matches episode conflicts to relevant clauses by bias type"""
    
    def __init__(self, clauses_path: str = "data/clauses.json"):
        self.clauses_path = Path(clauses_path)
        self.clauses = self._load_clauses()
    
    def _load_clauses(self) -> List[Dict]:
        """Load clause library from JSON"""
        with open(self.clauses_path, 'r') as f:
            return json.load(f)
    
    def match_clauses(self, episode: Dict) -> Dict[str, List[Dict]]:
        """
        Return 3 clause sets for an episode: VC win, Founder win, Win-Win
        
        Args:
            episode: Episode data with conflict_type
            
        Returns:
            Dict with keys: vc_win, founder_win, winwin
        """
        conflict_type = episode.get("conflict_type")
        
        # Filter clauses by conflict type
        relevant_clauses = [
            c for c in self.clauses 
            if c["conflict_type"] == conflict_type
        ]
        
        # Separate by bias
        vc_clauses = [c for c in relevant_clauses if c["bias"] == "VC_bias"]
        founder_clauses = [c for c in relevant_clauses if c["bias"] == "Founder_bias"]
        neutral_clauses = [c for c in relevant_clauses if c["bias"] == "Neutral"]
        
        return {
            "vc_win": vc_clauses,
            "founder_win": founder_clauses,
            "winwin": neutral_clauses
        }
    
    def get_alignment_score(self, clauses: List[Dict], perspective: str) -> int:
        """
        Calculate alignment score (0-100) for a set of clauses
        
        Args:
            clauses: List of clause dicts
            perspective: "vc" or "founder"
            
        Returns:
            Alignment score 0-100
        """
        if not clauses:
            return 50
        
        if perspective == "vc":
            # Lower founder risk = higher VC alignment
            avg_risk = sum(c["risk_score_founder"] for c in clauses) / len(clauses)
            return int(avg_risk)
        elif perspective == "founder":
            # Lower VC risk = higher founder alignment
            avg_risk = sum(c["risk_score_vc"] for c in clauses) / len(clauses)
            return int(avg_risk)
        else:
            # Neutral: balance both scores
            avg_founder_risk = sum(c["risk_score_founder"] for c in clauses) / len(clauses)
            avg_vc_risk = sum(c["risk_score_vc"] for c in clauses) / len(clauses)
            balance = 100 - abs(avg_founder_risk - avg_vc_risk)
            return int(balance)

