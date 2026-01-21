#!/bin/bash
# Setup Claude Code Workspace on C: Drive

echo "🚀 Claude Code Workspace Setup"
echo "================================"

# Check if C: drive is accessible (WSL)
if [ -d "/mnt/c" ]; then
    WORKSPACE_PATH="/mnt/c/ClaudeCodeProjects"
    echo "✅ C: drive accessible via WSL"
    echo "📁 Creating workspace at: $WORKSPACE_PATH"

    # Create main workspace directory
    mkdir -p "$WORKSPACE_PATH"

    # Create subdirectories for organization
    mkdir -p "$WORKSPACE_PATH/personal"
    mkdir -p "$WORKSPACE_PATH/work"
    mkdir -p "$WORKSPACE_PATH/experiments"
    mkdir -p "$WORKSPACE_PATH/templates"

    # Create a README
    cat > "$WORKSPACE_PATH/README.md" << 'EOF'
# Claude Code Projects Workspace

This directory contains all your Claude Code projects organized by category.

## Directory Structure

- **personal/** - Personal projects and experiments
- **work/** - Work-related projects
- **experiments/** - Testing and experimental code
- **templates/** - Project templates and starter code

## Quick Start

### Start a new project
```bash
cd /mnt/c/ClaudeCodeProjects/personal
mkdir my-new-project
cd my-new-project
git init
claude
```

### Open in PyCharm
```bash
/opt/pycharm-community-2024.3.2/bin/pycharm.sh /mnt/c/ClaudeCodeProjects/personal/my-project
```

### Configure Git (if not done already)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Claude Code CLI Quick Reference

- Start Claude: `claude`
- Continue last session: `claude -c`
- Help: `claude --help`
- Version: `claude --version`

## Tips

1. Always run `git init` in new projects
2. Create a `.gitignore` file for your project type
3. Use `CLAUDE.md` for project-specific instructions
4. Set up virtual environments for Python projects
EOF

    echo ""
    echo "✅ Workspace created successfully!"
    echo ""
    echo "📂 Your Claude Code workspace structure:"
    tree -L 2 "$WORKSPACE_PATH" 2>/dev/null || ls -la "$WORKSPACE_PATH"

    echo ""
    echo "🔗 Symbolic link created in home directory:"
    ln -sf "$WORKSPACE_PATH" ~/ClaudeCodeProjects
    echo "   ~/ClaudeCodeProjects -> $WORKSPACE_PATH"

    echo ""
    echo "📝 To start working:"
    echo "   cd $WORKSPACE_PATH"
    echo "   # or"
    echo "   cd ~/ClaudeCodeProjects"

else
    # Not in WSL, create workspace in home directory
    WORKSPACE_PATH="$HOME/ClaudeCodeProjects"
    echo "⚠️  C: drive not accessible (not in WSL)"
    echo "📁 Creating workspace at: $WORKSPACE_PATH"

    # Create main workspace directory
    mkdir -p "$WORKSPACE_PATH"
    mkdir -p "$WORKSPACE_PATH/personal"
    mkdir -p "$WORKSPACE_PATH/work"
    mkdir -p "$WORKSPACE_PATH/experiments"
    mkdir -p "$WORKSPACE_PATH/templates"

    # Create README (same as above)
    cat > "$WORKSPACE_PATH/README.md" << 'EOF'
# Claude Code Projects Workspace

This directory contains all your Claude Code projects organized by category.

## Directory Structure

- **personal/** - Personal projects and experiments
- **work/** - Work-related projects
- **experiments/** - Testing and experimental code
- **templates/** - Project templates and starter code

## Quick Start

### Start a new project
```bash
cd ~/ClaudeCodeProjects/personal
mkdir my-new-project
cd my-new-project
git init
claude
```

### Open in PyCharm
```bash
/opt/pycharm-community-2024.3.2/bin/pycharm.sh ~/ClaudeCodeProjects/personal/my-project
```

### Configure Git (if not done already)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Claude Code CLI Quick Reference

- Start Claude: `claude`
- Continue last session: `claude -c`
- Help: `claude --help`
- Version: `claude --version`
EOF

    echo ""
    echo "✅ Workspace created successfully!"
    echo ""
    echo "📂 Your Claude Code workspace structure:"
    tree -L 2 "$WORKSPACE_PATH" 2>/dev/null || ls -la "$WORKSPACE_PATH"

    echo ""
    echo "📝 To start working:"
    echo "   cd $WORKSPACE_PATH"

    echo ""
    echo "💡 Note: To use C: drive, you need to:"
    echo "   1. Run this in WSL (Windows Subsystem for Linux)"
    echo "   2. Or manually create C:\\ClaudeCodeProjects on Windows"
fi

echo ""
echo "🚀 PyCharm is installed at: /opt/pycharm-community-2024.3.2"
echo "   Launch with: /opt/pycharm-community-2024.3.2/bin/pycharm.sh"

echo ""
echo "✨ Setup complete!"
