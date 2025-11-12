"""Database manager for DuckDB and Supabase"""
import duckdb
import json
from pathlib import Path
from typing import Optional
import config


class DBManager:
    """Manages local DuckDB and optional Supabase sync"""
    
    def __init__(self, db_path: str = config.DUCKDB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._init_schema()
    
    def _init_schema(self):
        """Create tables if they don't exist"""
        # Episodes table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                episode_id VARCHAR PRIMARY KEY,
                title VARCHAR,
                conflict_type VARCHAR,
                scene TEXT,
                founder_action TEXT,
                vc_action TEXT,
                result TEXT,
                legal_stakes TEXT
            )
        """)
        
        # Clauses table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS clauses (
                clause_id VARCHAR PRIMARY KEY,
                conflict_type VARCHAR,
                bias VARCHAR,
                clause_type VARCHAR,
                short_text TEXT,
                full_text TEXT,
                explanation TEXT,
                risk_score_founder INTEGER,
                risk_score_vc INTEGER
            )
        """)
        
        # Simulations table (persists user generations)
        self.conn.execute("""
            CREATE SEQUENCE IF NOT EXISTS simulations_seq START 1;
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY DEFAULT nextval('simulations_seq'),
                episode_id VARCHAR,
                scenario_type VARCHAR,
                clauses_json TEXT,
                narrative TEXT,
                alignment_scores_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def load_episodes(self, json_path: str):
        """Load episodes from JSON into DuckDB"""
        with open(json_path, 'r') as f:
            episodes = json.load(f)
        
        for ep in episodes:
            self.conn.execute("""
                INSERT OR REPLACE INTO episodes VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ep['episode_id'], ep['title'], ep['conflict_type'],
                ep['scene'], ep['founder_action'], ep['vc_action'],
                ep['result'], ep['legal_stakes']
            ])
    
    def load_clauses(self, json_path: str):
        """Load clauses from JSON into DuckDB"""
        with open(json_path, 'r') as f:
            clauses = json.load(f)
        
        for clause in clauses:
            self.conn.execute("""
                INSERT OR REPLACE INTO clauses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                clause['clause_id'], clause['conflict_type'], clause['bias'],
                clause['clause_type'], clause['short_text'], clause['full_text'],
                clause['explanation'], clause['risk_score_founder'], 
                clause['risk_score_vc']
            ])
    
    def get_episode(self, episode_id: str) -> Optional[dict]:
        """Fetch episode by ID"""
        result = self.conn.execute(
            "SELECT * FROM episodes WHERE episode_id = ?", 
            [episode_id]
        ).fetchone()
        
        if not result:
            return None
        
        cols = [desc[0] for desc in self.conn.description]
        return dict(zip(cols, result))
    
    def get_all_episodes(self) -> list[dict]:
        """Fetch all episodes"""
        results = self.conn.execute("SELECT * FROM episodes").fetchall()
        cols = [desc[0] for desc in self.conn.description]
        return [dict(zip(cols, row)) for row in results]
    
    def save_simulation(
        self, 
        episode_id: str, 
        scenario_type: str, 
        clauses: list, 
        narrative: str, 
        alignment_scores: dict
    ):
        """Save simulation result for resume/portfolio use"""
        self.conn.execute("""
            INSERT INTO simulations (
                episode_id, scenario_type, clauses_json, 
                narrative, alignment_scores_json
            ) VALUES (?, ?, ?, ?, ?)
        """, [
            episode_id, scenario_type, json.dumps(clauses),
            narrative, json.dumps(alignment_scores)
        ])
    
    def close(self):
        """Close database connection"""
        self.conn.close()

