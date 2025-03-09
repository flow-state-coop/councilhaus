# Streamlit Cloud Deployment Checklist

Use this checklist to ensure you have everything ready for deploying to Streamlit Cloud.

## Repository Structure

- [ ] Main app file (`app.py`) is present and working
- [ ] Requirements file (`requirements.txt`) includes all dependencies
- [ ] Streamlit configuration (`.streamlit/config.toml`) is set up
- [ ] Data directories are created with `.gitkeep` files
  - [ ] `data/results/`
  - [ ] `data/figures/`
  - [ ] `data/configs/`

## Code Preparation

- [ ] Imports use relative paths or include path adjustments
- [ ] App creates necessary directories if they don't exist
- [ ] Caching is implemented for expensive operations
- [ ] Progress indicators are used for long-running operations

## GitHub Repository

- [ ] Code is pushed to a GitHub repository
- [ ] Repository is public (or you have a paid Streamlit Cloud account)
- [ ] `.gitignore` is configured to exclude unnecessary files
- [ ] README includes deployment instructions

## Streamlit Cloud Account

- [ ] You have signed up for Streamlit Cloud
- [ ] You have connected your GitHub account
- [ ] You have authorized Streamlit Cloud to access your repositories

## Deployment Configuration

- [ ] Repository: Your GitHub repository
- [ ] Branch: The branch to deploy (usually `main` or `master`)
- [ ] Main file path: The path to your main app file (e.g., `simulator/app.py`)
- [ ] Python version: 3.10 (optional)
- [ ] Additional packages: Any packages not in requirements.txt (optional)

## Post-Deployment

- [ ] App is accessible at the provided URL
- [ ] All functionality works as expected
- [ ] Performance is acceptable
- [ ] No errors in the logs

## Optional Configuration

- [ ] Custom domain is set up (if needed)
- [ ] Authentication is configured (if needed)
- [ ] Secrets are managed securely (if needed)
- [ ] App settings are optimized for performance 