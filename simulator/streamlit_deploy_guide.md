# Deploying to Streamlit Cloud

This guide provides step-by-step instructions for deploying the Council Funding Simulator to Streamlit Cloud.

## What is Streamlit Cloud?

Streamlit Cloud is a hosting service specifically designed for Streamlit apps. It offers:

- Free hosting for public repositories
- Automatic updates when you push to GitHub
- Authentication options
- Custom domains
- Seamless integration with GitHub

## Prerequisites

1. A GitHub account
2. Your simulator code in a GitHub repository
3. A Streamlit Cloud account (you can sign up with your GitHub account)

## Step 1: Prepare Your Repository

Ensure your repository has the following structure:

```
simulator/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .streamlit/            # Streamlit configuration
│   └── config.toml        # Streamlit theme and settings
└── data/                  # Data directories
    ├── results/           # For storing simulation results
    ├── figures/           # For storing generated figures
    └── configs/           # For storing configurations
```

## Step 2: Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "Continue with GitHub" to sign in with your GitHub account
3. Authorize Streamlit Cloud to access your GitHub repositories

## Step 3: Deploy Your App

1. Once logged in, click the "New app" button
2. Select your GitHub repository from the list
3. Configure your app:
   - **Repository**: Your GitHub repository
   - **Branch**: The branch to deploy (usually `main` or `master`)
   - **Main file path**: The path to your main app file (e.g., `simulator/app.py`)
   - **Advanced settings** (optional):
     - Python version: 3.10
     - Packages: Any additional packages not in requirements.txt

4. Click "Deploy!"

## Step 4: Wait for Deployment

Streamlit Cloud will now:
1. Clone your repository
2. Install dependencies from requirements.txt
3. Run your Streamlit app
4. Provide a URL where your app is accessible

This process usually takes 1-2 minutes.

## Step 5: Access Your App

Once deployment is complete, you'll see a URL where your app is accessible (e.g., `https://username-app-name.streamlit.app`).

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   
   If your app fails to deploy due to missing dependencies:
   - Check the build logs
   - Ensure all required packages are listed in `requirements.txt`
   - Add any missing packages and push the changes to GitHub

2. **Import Errors**
   
   If your app has import errors:
   - Ensure all imports use relative paths correctly
   - Check that your file structure matches what your code expects

3. **Memory or Performance Issues**
   
   If your app runs out of memory or is slow:
   - Use `@st.cache_data` and `@st.cache_resource` decorators for expensive operations
   - Optimize data loading and processing
   - Consider breaking large operations into smaller chunks

4. **File Not Found Errors**
   
   If your app can't find data files:
   - Use relative paths with `Path(__file__).parent`
   - Create directories if they don't exist
   - Include placeholder files in your repository

## Updating Your App

Streamlit Cloud automatically updates your app when you push changes to GitHub:

1. Make changes to your code locally
2. Commit and push to GitHub
3. Streamlit Cloud will detect the changes and redeploy your app

## Additional Features

### Custom Domain

To use a custom domain:
1. Go to your app's settings
2. Click on "Custom domain"
3. Follow the instructions to set up DNS records

### Authentication

To add authentication:
1. Go to your app's settings
2. Click on "Settings" > "Sharing"
3. Choose your authentication method (Google, GitHub, etc.)

### Secrets Management

To use secrets (API keys, etc.):
1. Go to your app's settings
2. Click on "Settings" > "Secrets"
3. Add your secrets as key-value pairs

## Conclusion

Streamlit Cloud is the easiest way to deploy Streamlit apps. It's specifically designed for Streamlit and handles most of the deployment complexity for you.

If you encounter any issues not covered in this guide, check the [Streamlit Cloud documentation](https://docs.streamlit.io/streamlit-cloud) or reach out to Streamlit support. 