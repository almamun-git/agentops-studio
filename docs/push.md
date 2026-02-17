# Pushing to GitHub

If `git push` fails with authentication errors:

1. **Authenticate with GitHub CLI**
   ```bash
   gh auth login
   git push
   ```

2. **Or use SSH**
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/agentops-studio.git
   git push
   ```

3. **Or configure HTTPS credentials**
   ```bash
   git config credential.helper store
   git push
   # Enter your GitHub username and a Personal Access Token when prompted
   ```
