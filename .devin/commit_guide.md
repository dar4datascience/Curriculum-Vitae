# Commit Message Guide

## Format

```
<type>: <subject>

<body>

<footer>
```

## Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding tests
- **chore**: Maintenance tasks, dependencies, build process

## Examples from This Session

### ✅ Good Commits

```bash
# Feature with detailed body
feat: add interactive portfolio with yesenia.io-style animations

Portfolio Features:
- Complete scrolling portfolio with 6 animated sections
- D3.js bubble chart with physics simulation
- Infinite tech stack carousel (DevOps focused)

Highlights DevOps & CI/CD Expertise:
- CI/CD, GitHub Actions, Docker, Kubernetes bubbles
- Infrastructure as Code (Terraform)
```

```bash
# Refactor with clear changes
refactor: modernize R code and fix CV metadata

R Code Improvements:
- Remove unnecessary return() statements
- Use case_when() with .default for cleaner logic
- Combine multiple mutate() calls

CV Fixes:
- Update AutoCV.qmd: TeamStation AI (was Rackspace)
```

```bash
# Chore with specific actions
chore: update .gitignore with Quarto best practices

- Ignore Quarto build artifacts (*_files/, *_cache/)
- Ignore LaTeX intermediate files (*.log, *.tex)
- Ignore targets pipeline cache (_targets/)
- Document tracking guidelines
```

## Quick Reference

### Daily Work
```bash
# Small fix
git commit -m "fix: correct date in timeline (2024 → 2025)"

# Add feature
git commit -m "feat: add contact form validation"

# Update docs
git commit -m "docs: add setup instructions to README"
```

### Larger Changes
```bash
git commit -m "feat: implement user authentication

- Add JWT token generation
- Create login/logout endpoints
- Add middleware for protected routes
- Update database schema for users table"
```

### Breaking Changes
```bash
git commit -m "refactor!: change API response format

BREAKING CHANGE: API now returns data in camelCase instead of snake_case

Migration guide:
- Update all API clients to use new format
- See MIGRATION.md for details"
```

## Tips

1. **Use present tense**: "add feature" not "added feature"
2. **Be specific**: "fix login button alignment" not "fix UI"
3. **Explain why**: Include context in the body
4. **Group related changes**: Don't mix features and fixes
5. **Keep commits atomic**: One logical change per commit

## Workflow

```bash
# 1. Check what changed
git status

# 2. Stage related files
git add file1.js file2.js

# 3. Commit with message
git commit -m "feat: add user profile page"

# 4. Repeat for different changes
git add tests/
git commit -m "test: add profile page tests"
```

## Recent Commits Summary

1. **Remove build artifacts** - Clean up tracked build files
2. **Update .gitignore** - Add Quarto best practices
3. **Modernize R code** - Refactor with modern patterns
4. **Fix Quarto config** - Exclude markdown from rendering
5. **Add portfolio** - Interactive animations showcase
6. **Add Python tools** - CV management and GitHub scraper
7. **Update website** - Rebuild with latest changes
8. **Remove obsolete files** - Clean up old CV versions
