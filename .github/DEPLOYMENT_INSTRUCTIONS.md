# GitHub Pages Deployment Setup

## Required Repository Settings Change

After pushing this commit, you need to update your GitHub repository settings:

### Steps:

1. Go to your repository: https://github.com/dar4datascience/Curriculum-Vitae
2. Click **Settings** tab
3. Click **Pages** in the left sidebar
4. Under **Build and deployment**:
   - **Source**: Change from "Deploy from a branch" to **"GitHub Actions"**
   
That's it! The workflow will automatically deploy on the next push.

## What Changed

### Before:
- Used classic deployment pointing at `docs/` folder on `main` branch
- Manual control over what gets published

### After:
- Uses GitHub Actions workflow with `actions/deploy-pages@v4`
- Proper artifact upload with `actions/upload-pages-artifact@v3`
- Better caching and optimization
- Follows Quarto's official best practices
- Ensures correct website structure and navigation rendering

## Workflow Details

The workflow (`.github/workflows/publish.yml`) now:
1. Checks out the repository
2. Sets up Quarto (latest release)
3. Installs R 4.2.0
4. Installs R dependencies via renv
5. Renders the Quarto project
6. Uploads the `docs/` folder as a Pages artifact
7. Deploys to GitHub Pages

## Permissions

The workflow requires these permissions (already configured):
- `contents: write` - To check out the repo
- `pages: write` - To deploy to Pages
- `id-token: write` - For OIDC authentication

## Reference

Based on: https://github.com/quarto-dev/quarto-actions/tree/main/examples
