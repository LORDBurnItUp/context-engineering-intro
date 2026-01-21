# Claude Code Session Information

## Session Details
- **Session Directory**: `/home/user/context-engineering-intro`
- **Session Date**: 2026-01-21
- **Branch**: `claude/setup-claude-md-cli-iQlLI`

## Environment Setup

### Claude Code CLI
- **Status**: ✅ Installed and Working
- **Version**: 2.1.14 (Claude Code)
- **Installation Method**: npm global package
- **Package**: `@anthropic-ai/claude-code`
- **Command**: `claude` (not `claude-code`)
- **Binary Location**: `/opt/node22/bin/claude`

### JetBrains IDE
- **PyCharm Status**: ✅ Installed
- **PyCharm Version**: Community 2024.3.2
- **Location**: `/opt/pycharm-community-2024.3.2`
- **Launch Command**: `/opt/pycharm-community-2024.3.2/bin/pycharm.sh`
- **WebStorm**: ✅ Already installed by user

### Project Structure
- Main configuration file: `CLAUDE.md` (uppercase)
- Planning document: `PLANNING.md`
- Task tracking: `TASK.md`
- Project root: `/home/user/context-engineering-intro`

## Quick Commands

### Start Claude Code CLI
```bash
claude
```

### Get Claude CLI Help
```bash
claude --help
```

### Navigate to Project
```bash
cd /home/user/context-engineering-intro
```

### Check Git Status
```bash
git status
```

### View Project Files
```bash
ls -la
```

## JetBrains Installation (Manual)

If you want to install PyCharm manually:

```bash
# Download JetBrains Toolbox (recommended)
cd ~/Downloads
wget https://download.jetbrains.com/toolbox/jetbrains-toolbox-latest.tar.gz
tar -xzf jetbrains-toolbox-latest.tar.gz
cd jetbrains-toolbox-*
./jetbrains-toolbox
```

Or install PyCharm directly:
```bash
# Download PyCharm Community Edition
wget https://download.jetbrains.com/python/pycharm-community-latest.tar.gz
tar -xzf pycharm-community-latest.tar.gz -C /opt/
# Run PyCharm
/opt/pycharm-community-*/bin/pycharm.sh
```

## Session Configuration

### .claude Directory Structure
```
.claude/
├── settings.local.json    # Permissions and settings
└── commands/             # Custom commands
    ├── execute-prp.md
    └── generate-prp.md
```

### Allowed Permissions
- Bash commands: grep, ls, source, find, mv, mkdir, tree, ruff, touch, cat, pytest, python
- WebFetch: docs.anthropic.com, github.com

## Claude Code Projects Workspace

### Main Workspace Directory
- **Linux Path**: `/root/ClaudeCodeProjects` (or `~/ClaudeCodeProjects`)
- **Windows C: Drive**: See `WINDOWS_SETUP.md` for WSL configuration

### Workspace Structure
```
ClaudeCodeProjects/
├── personal/          # Personal projects
├── work/             # Work-related projects
├── experiments/      # Testing and experimental code
├── templates/        # Project templates
└── README.md         # Quick reference
```

### Quick Start New Project
```bash
cd ~/ClaudeCodeProjects/personal
mkdir my-new-project && cd my-new-project
git init
claude
```

### Open Project in PyCharm
```bash
/opt/pycharm-community-2024.3.2/bin/pycharm.sh ~/ClaudeCodeProjects/personal/my-project
```

## Notes
- This session is working on branch: `claude/setup-claude-md-cli-iQlLI`
- Virtual environment: `venv_linux` (for Python commands)
- All git operations should be performed on the feature branch
- Session files stored in: `/home/user/context-engineering-intro`
- **See WINDOWS_SETUP.md for C: drive configuration**
