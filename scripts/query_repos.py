#!/usr/bin/env python3
"""
Query GitHub Repositories Database
Helper script to query and filter the local repository database.

Usage:
    python query_repos.py --skills "aws,python,data-engineering"
    python query_repos.py --language Python --min-stars 5
    python query_repos.py --category "Cloud & AWS"
"""

import sqlite3
import json
import argparse
from pathlib import Path
from typing import List, Optional


class RepoQuery:
    """Query the GitHub repositories database."""
    
    def __init__(self, db_path: str = "github_repos.db"):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {db_path}. Run fetch_github_repos.py first.")
    
    def get_repos_by_language(self, language: str, min_stars: int = 0) -> List[dict]:
        """Get repositories by programming language."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, description, url, stars, updated_at
            FROM repositories
            WHERE language = ? AND stars >= ? AND is_fork = 0
            ORDER BY stars DESC
        """, (language, min_stars))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "name": r[0],
                "description": r[1],
                "url": r[2],
                "stars": r[3],
                "updated_at": r[4]
            }
            for r in results
        ]
    
    def get_repos_by_topics(self, topics: List[str]) -> List[dict]:
        """Get repositories that contain any of the specified topics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, description, url, topics, stars FROM repositories WHERE is_fork = 0")
        all_repos = cursor.fetchall()
        conn.close()
        
        matching_repos = []
        for name, desc, url, topics_json, stars in all_repos:
            repo_topics = json.loads(topics_json) if topics_json else []
            if any(topic.lower() in [t.lower() for t in repo_topics] for topic in topics):
                matching_repos.append({
                    "name": name,
                    "description": desc,
                    "url": url,
                    "topics": repo_topics,
                    "stars": stars
                })
        
        return sorted(matching_repos, key=lambda x: x["stars"], reverse=True)
    
    def get_skills_by_category(self, category: str) -> List[dict]:
        """Get all skills in a specific category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT skill_name, repo_count
            FROM skills
            WHERE category = ?
            ORDER BY repo_count DESC
        """, (category,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{"skill": r[0], "repo_count": r[1]} for r in results]
    
    def get_all_categories(self) -> List[str]:
        """Get all skill categories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM skills ORDER BY category")
        results = cursor.fetchall()
        conn.close()
        
        return [r[0] for r in results]
    
    def get_top_skills(self, limit: int = 20) -> List[dict]:
        """Get top skills by repository count."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT skill_name, category, repo_count
            FROM skills
            ORDER BY repo_count DESC
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {"skill": r[0], "category": r[1], "repo_count": r[2]}
            for r in results
        ]
    
    def search_repos(self, keyword: str) -> List[dict]:
        """Search repositories by keyword in name or description."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, description, url, language, stars
            FROM repositories
            WHERE (name LIKE ? OR description LIKE ?) AND is_fork = 0
            ORDER BY stars DESC
        """, (f"%{keyword}%", f"%{keyword}%"))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "name": r[0],
                "description": r[1],
                "url": r[2],
                "language": r[3],
                "stars": r[4]
            }
            for r in results
        ]
    
    def generate_cv_skills_list(self, categories: Optional[List[str]] = None) -> str:
        """Generate a formatted skills list for CV."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if categories:
            placeholders = ",".join("?" * len(categories))
            cursor.execute(f"""
                SELECT category, skill_name, repo_count
                FROM skills
                WHERE category IN ({placeholders})
                ORDER BY category, repo_count DESC
            """, categories)
        else:
            cursor.execute("""
                SELECT category, skill_name, repo_count
                FROM skills
                ORDER BY category, repo_count DESC
            """)
        
        results = cursor.fetchall()
        conn.close()
        
        skills_by_category = {}
        for category, skill, count in results:
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(f"{skill} ({count})")
        
        output = []
        for category, skills in skills_by_category.items():
            output.append(f"\n{category}:")
            output.append("  " + ", ".join(skills[:10]))
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Query GitHub repositories database")
    parser.add_argument("--db", default="github_repos.db", help="Database path")
    parser.add_argument("--language", help="Filter by programming language")
    parser.add_argument("--topics", help="Filter by topics (comma-separated)")
    parser.add_argument("--category", help="Show skills in category")
    parser.add_argument("--search", help="Search keyword in repo name/description")
    parser.add_argument("--min-stars", type=int, default=0, help="Minimum stars")
    parser.add_argument("--top-skills", type=int, help="Show top N skills")
    parser.add_argument("--cv-skills", action="store_true", help="Generate CV skills list")
    parser.add_argument("--categories", help="Categories for CV skills (comma-separated)")
    
    args = parser.parse_args()
    
    query = RepoQuery(db_path=args.db)
    
    if args.language:
        repos = query.get_repos_by_language(args.language, args.min_stars)
        print(f"\nRepositories using {args.language} (min {args.min_stars} stars):")
        for repo in repos:
            print(f"\n  {repo['name']} ⭐ {repo['stars']}")
            print(f"    {repo['description']}")
            print(f"    {repo['url']}")
    
    elif args.topics:
        topics = [t.strip() for t in args.topics.split(",")]
        repos = query.get_repos_by_topics(topics)
        print(f"\nRepositories with topics: {', '.join(topics)}")
        for repo in repos:
            print(f"\n  {repo['name']} ⭐ {repo['stars']}")
            print(f"    {repo['description']}")
            print(f"    Topics: {', '.join(repo['topics'])}")
    
    elif args.category:
        skills = query.get_skills_by_category(args.category)
        print(f"\nSkills in '{args.category}':")
        for skill in skills:
            print(f"  {skill['skill']}: {skill['repo_count']} repos")
    
    elif args.search:
        repos = query.search_repos(args.search)
        print(f"\nSearch results for '{args.search}':")
        for repo in repos:
            print(f"\n  {repo['name']} ({repo['language']}) ⭐ {repo['stars']}")
            print(f"    {repo['description']}")
    
    elif args.top_skills:
        skills = query.get_top_skills(args.top_skills)
        print(f"\nTop {args.top_skills} Skills:")
        for i, skill in enumerate(skills, 1):
            print(f"  {i}. {skill['skill']} ({skill['category']}): {skill['repo_count']} repos")
    
    elif args.cv_skills:
        categories = [c.strip() for c in args.categories.split(",")] if args.categories else None
        skills_text = query.generate_cv_skills_list(categories)
        print("\nCV Skills List:")
        print(skills_text)
    
    else:
        categories = query.get_all_categories()
        print("\nAvailable categories:")
        for cat in categories:
            print(f"  - {cat}")
        print("\nUse --help to see query options")


if __name__ == "__main__":
    main()
