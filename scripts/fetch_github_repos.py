#!/usr/bin/env python3
"""
GitHub Repository Scraper
Fetches all repository names and descriptions from a GitHub user profile
and stores them in a local database for CV updates.

Usage:
    python fetch_github_repos.py [--username USERNAME] [--output OUTPUT]
"""

import requests
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import argparse
from typing import List, Dict, Optional


class GitHubRepoFetcher:
    """Fetch and store GitHub repository information."""
    
    def __init__(self, username: str = "dar4datascience", db_path: str = "github_repos.db"):
        self.username = username
        self.db_path = Path(db_path)
        self.api_base = "https://api.github.com"
        
    def fetch_repositories(self) -> List[Dict]:
        """Fetch all public repositories for the user."""
        repos = []
        page = 1
        per_page = 100
        
        print(f"Fetching repositories for {self.username}...")
        
        while True:
            url = f"{self.api_base}/users/{self.username}/repos"
            params = {
                "page": page,
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc"
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break
                
            data = response.json()
            
            if not data:
                break
                
            repos.extend(data)
            print(f"  Fetched page {page} ({len(data)} repos)")
            page += 1
            
        print(f"Total repositories fetched: {len(repos)}")
        return repos
    
    def extract_repo_info(self, repos: List[Dict]) -> List[Dict]:
        """Extract relevant information from repository data."""
        extracted = []
        
        for repo in repos:
            info = {
                "name": repo.get("name", ""),
                "full_name": repo.get("full_name", ""),
                "description": repo.get("description", ""),
                "url": repo.get("html_url", ""),
                "language": repo.get("language", ""),
                "topics": repo.get("topics", []),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
                "is_fork": repo.get("fork", False),
                "is_archived": repo.get("archived", False),
            }
            extracted.append(info)
            
        return extracted
    
    def create_database(self):
        """Create SQLite database and tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                full_name TEXT UNIQUE NOT NULL,
                description TEXT,
                url TEXT,
                language TEXT,
                topics TEXT,
                stars INTEGER,
                forks INTEGER,
                created_at TEXT,
                updated_at TEXT,
                is_fork BOOLEAN,
                is_archived BOOLEAN,
                fetched_at TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name TEXT UNIQUE NOT NULL,
                category TEXT,
                repo_count INTEGER DEFAULT 0,
                last_updated TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
    def save_to_database(self, repos: List[Dict]):
        """Save repository information to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fetched_at = datetime.now().isoformat()
        
        for repo in repos:
            cursor.execute("""
                INSERT OR REPLACE INTO repositories 
                (name, full_name, description, url, language, topics, stars, forks, 
                 created_at, updated_at, is_fork, is_archived, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                repo["name"],
                repo["full_name"],
                repo["description"],
                repo["url"],
                repo["language"],
                json.dumps(repo["topics"]),
                repo["stars"],
                repo["forks"],
                repo["created_at"],
                repo["updated_at"],
                repo["is_fork"],
                repo["is_archived"],
                fetched_at
            ))
        
        conn.commit()
        conn.close()
        print(f"Saved {len(repos)} repositories to {self.db_path}")
    
    def extract_skills(self):
        """Extract and categorize skills from repositories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT language, topics FROM repositories WHERE is_fork = 0 AND is_archived = 0")
        rows = cursor.fetchall()
        
        skills = {}
        
        for language, topics_json in rows:
            if language:
                skills[language] = skills.get(language, 0) + 1
            
            if topics_json:
                topics = json.loads(topics_json)
                for topic in topics:
                    skills[topic] = skills.get(topic, 0) + 1
        
        updated_at = datetime.now().isoformat()
        
        for skill, count in skills.items():
            category = self._categorize_skill(skill)
            cursor.execute("""
                INSERT OR REPLACE INTO skills (skill_name, category, repo_count, last_updated)
                VALUES (?, ?, ?, ?)
            """, (skill, category, count, updated_at))
        
        conn.commit()
        conn.close()
        print(f"Extracted {len(skills)} unique skills")
    
    def _categorize_skill(self, skill: str) -> str:
        """Categorize a skill based on keywords."""
        skill_lower = skill.lower()
        
        categories = {
            "Programming Languages": ["python", "r", "javascript", "typescript", "java", "go", "rust", "sql"],
            "Data Engineering": ["data-engineering", "etl", "pipeline", "airflow", "spark", "kafka", "dbt"],
            "Cloud & AWS": ["aws", "cloud", "lambda", "s3", "ec2", "rds", "dynamodb", "cloudformation", "terraform"],
            "AI & ML": ["machine-learning", "ai", "deep-learning", "nlp", "tensorflow", "pytorch", "scikit-learn"],
            "Backend & Web": ["backend", "django", "flask", "fastapi", "api", "rest", "graphql"],
            "Databases": ["postgres", "postgresql", "mysql", "mongodb", "redis", "database"],
            "Big Data": ["big-data", "hadoop", "spark", "hive", "presto"],
            "DevOps": ["docker", "kubernetes", "ci-cd", "github-actions", "jenkins"],
            "Data Visualization": ["visualization", "dashboard", "plotly", "d3", "tableau", "powerbi"],
            "Other": []
        }
        
        for category, keywords in categories.items():
            if any(keyword in skill_lower for keyword in keywords):
                return category
        
        return "Other"
    
    def export_to_json(self, output_path: str = "github_repos.json"):
        """Export repository data to JSON file."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM repositories")
        columns = [description[0] for description in cursor.description]
        repos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM skills ORDER BY repo_count DESC")
        columns = [description[0] for description in cursor.description]
        skills = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        
        data = {
            "repositories": repos,
            "skills": skills,
            "metadata": {
                "username": self.username,
                "total_repos": len(repos),
                "total_skills": len(skills),
                "exported_at": datetime.now().isoformat()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Exported data to {output_path}")
    
    def print_summary(self):
        """Print a summary of the data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM repositories WHERE is_fork = 0")
        original_repos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM repositories WHERE is_fork = 1")
        forked_repos = cursor.fetchone()[0]
        
        cursor.execute("SELECT language, COUNT(*) as count FROM repositories WHERE is_fork = 0 GROUP BY language ORDER BY count DESC LIMIT 5")
        top_languages = cursor.fetchall()
        
        cursor.execute("SELECT category, COUNT(*) as count FROM skills GROUP BY category ORDER BY count DESC")
        skill_categories = cursor.fetchall()
        
        conn.close()
        
        print("\n" + "="*60)
        print("REPOSITORY SUMMARY")
        print("="*60)
        print(f"Original repositories: {original_repos}")
        print(f"Forked repositories: {forked_repos}")
        print(f"\nTop 5 Languages:")
        for lang, count in top_languages:
            print(f"  {lang or 'None'}: {count}")
        print(f"\nSkills by Category:")
        for category, count in skill_categories:
            print(f"  {category}: {count}")
        print("="*60 + "\n")
    
    def run(self, export_json: bool = True):
        """Run the complete fetch and store process."""
        self.create_database()
        repos = self.fetch_repositories()
        
        if not repos:
            print("No repositories found.")
            return
        
        extracted = self.extract_repo_info(repos)
        self.save_to_database(extracted)
        self.extract_skills()
        
        if export_json:
            self.export_to_json()
        
        self.print_summary()


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub repositories and create local database")
    parser.add_argument("--username", default="dar4datascience", help="GitHub username")
    parser.add_argument("--output", default="github_repos.db", help="Output database path")
    parser.add_argument("--no-json", action="store_true", help="Skip JSON export")
    
    args = parser.parse_args()
    
    fetcher = GitHubRepoFetcher(username=args.username, db_path=args.output)
    fetcher.run(export_json=not args.no_json)


if __name__ == "__main__":
    main()
