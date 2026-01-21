# Windows C: Drive Setup for Claude Code Projects

Since you're running in a Linux environment but want to use your Windows C: drive, here's how to set it up:

## Option 1: Use WSL (Recommended)

If you're on Windows, use Windows Subsystem for Linux (WSL) to access your C: drive directly:

### 1. Open PowerShell as Administrator and enable WSL:
```powershell
wsl --install
```

### 2. After WSL is installed, access C: drive:
```bash
# In WSL, your C: drive is mounted at /mnt/c
cd /mnt/c
mkdir ClaudeCodeProjects
cd ClaudeCodeProjects
```

### 3. Run the setup script:
```bash
bash /home/user/context-engineering-intro/setup-claude-workspace.sh
```

### 4. Your workspace will be at:
- Windows path: `C:\ClaudeCodeProjects`
- WSL path: `/mnt/c/ClaudeCodeProjects`

## Option 2: Manual Windows Setup

If not using WSL, manually create the directory on Windows:

### 1. Open Command Prompt or PowerShell:
```cmd
cd C:\
mkdir ClaudeCodeProjects
cd ClaudeCodeProjects
mkdir personal
mkdir work
mkdir experiments
mkdir templates
```

### 2. Install Claude Code CLI on Windows:
```cmd
npm install -g @anthropic-ai/claude-code
```

### 3. Verify installation:
```cmd
claude --version
```

### 4. Start using Claude Code:
```cmd
cd C:\ClaudeCodeProjects\personal
mkdir my-first-project
cd my-first-project
git init
claude
```

## Option 3: Current Linux Environment

I've already created a workspace in your current environment at:
```
/home/user/ClaudeCodeProjects
```

You can use this right now for all your Claude Code projects.

## Directory Structure

Your workspace is organized as:

```
ClaudeCodeProjects/
├── personal/          # Personal projects
├── work/             # Work-related projects
├── experiments/      # Testing and experimental code
├── templates/        # Project templates
└── README.md         # Quick reference guide
```

## PyCharm Setup

### Launch PyCharm:
```bash
/opt/pycharm-community-2024.3.2/bin/pycharm.sh
```

### Create Desktop Shortcut (Linux):
```bash
# Create a launcher script
cat > ~/pycharm.sh << 'EOF'
#!/bin/bash
/opt/pycharm-community-2024.3.2/bin/pycharm.sh "$@"
EOF
chmod +x ~/pycharm.sh

# Now you can run: ~/pycharm.sh
```

### Open a Project in PyCharm:
```bash
# From WSL/Linux
/opt/pycharm-community-2024.3.2/bin/pycharm.sh /mnt/c/ClaudeCodeProjects/personal/my-project

# Or from current environment
/opt/pycharm-community-2024.3.2/bin/pycharm.sh ~/ClaudeCodeProjects/personal/my-project
```

### Configure PyCharm with Claude Code:
1. Open PyCharm
2. Go to: Settings → Tools → Terminal
3. Set Shell path to your preferred shell
4. You can now use `claude` command from PyCharm's terminal

## Creating Your First Repo

### 1. Navigate to your workspace:
```bash
cd ~/ClaudeCodeProjects/personal
# or if using WSL: cd /mnt/c/ClaudeCodeProjects/personal
```

### 2. Create a new project:
```bash
mkdir my-awesome-project
cd my-awesome-project
```

### 3. Initialize Git:
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 4. Create initial files:
```bash
# Create a README
echo "# My Awesome Project" > README.md

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
venv_linux/
*.egg-info/
.pytest_cache/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
EOF

# Create CLAUDE.md for project-specific instructions
cat > CLAUDE.md << 'EOF'
# Project Instructions for Claude

## Project Overview
[Describe your project here]

## Development Guidelines
- Use Python 3.x
- Follow PEP8 style guide
- Write tests for new features

## Dependencies
[List main dependencies]
EOF
```

### 5. Create first commit:
```bash
git add .
git commit -m "Initial commit: Project setup"
```

### 6. Create GitHub repo and push:
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/yourusername/my-awesome-project.git
git branch -M main
git push -u origin main
```

### 7. Start Claude Code:
```bash
claude
```

## Quick Reference

### Navigate to Projects
```bash
# Linux environment
cd ~/ClaudeCodeProjects

# WSL (Windows C: drive)
cd /mnt/c/ClaudeCodeProjects
```

### Start New Project
```bash
cd ~/ClaudeCodeProjects/personal
mkdir new-project && cd new-project
git init
claude
```

### Open in PyCharm
```bash
/opt/pycharm-community-2024.3.2/bin/pycharm.sh ~/ClaudeCodeProjects/personal/new-project
```

### Launch Claude Code
```bash
claude                    # Start new session
claude -c                # Continue last session
claude --help           # Show help
```

## WebStorm Integration

Since you have WebStorm installed, you can also use it for JavaScript/TypeScript projects:

```bash
# Find WebStorm installation
which webstorm

# Open project in WebStorm
webstorm ~/ClaudeCodeProjects/work/my-web-project
```

## Tips

1. **Use CLAUDE.md**: Create this file in each project with specific instructions
2. **Virtual Environments**: For Python projects, always create a venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Git Workflow**: Commit often, push regularly
4. **Organization**: Use the subdirectories (personal/work/experiments) to keep projects organized
5. **Templates**: Create project templates in the templates/ directory for quick starts

## Next Steps

1. ✅ PyCharm installed
2. ✅ Claude Code CLI installed
3. ✅ Workspace directory created
4. ⏭️ Create your first project
5. ⏭️ Set up GitHub integration
6. ⏭️ Configure PyCharm settings
