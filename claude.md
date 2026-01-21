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
- **Status**: ⚠️ Not currently installed
- **Note**: JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm, etc.) need to be installed separately
- **Recommended**: PyCharm (for Python development)
- **Installation Options**:
  - Download JetBrains Toolbox: https://www.jetbrains.com/toolbox-app/
  - Direct download PyCharm: https://www.jetbrains.com/pycharm/download/
  - Or use manual installation (see below)

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

## Notes
- This session is working on branch: `claude/setup-claude-md-cli-iQlLI`
- Virtual environment: `venv_linux` (for Python commands)
- All git operations should be performed on the feature branch
- Session files stored in: `/home/user/context-engineering-intro`
