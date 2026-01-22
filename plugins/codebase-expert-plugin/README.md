# Expertise Management Plugin for Claude Code

A Claude Code plugin that provides tools and agents for discovering, curating, and managing expertise files for your codebase.

## Features

### Skills
- **discover-expertise**: Discover and generate expertise files for new codebases
- **expertise-curator**: Curate and maintain expertise YAML files
- **validate-expertise**: Validate expertise YAML files for structure and required fields
- **skill-creator**: Guide for creating effective skills
- **agent-creator**: Guide for creating custom Claude Code agents

### Agents
- **expert**: Expert researcher for brownfield codebases using expertise YAML files

## Installation

### Via Git Repository (Recommended)

Users can install this plugin directly from the git repository:

#### Step 1: Add the marketplace

```bash
/plugin marketplace add https://github.com/anthropics/hackathon-2026-ai-agent.git
```

Or if using GitHub shorthand:

```bash
/plugin marketplace add anthropics/hackathon-2026-ai-agent
```

#### Step 2: Install the plugin

```bash
/plugin install expertise-management
```

### Installation Scopes

You can install at different scopes:

- **User scope** (default): Available across all your projects
  ```bash
  /plugin install expertise-management --scope user
  ```

- **Project scope**: Shared with your team via version control
  ```bash
  /plugin install expertise-management --scope project
  ```

- **Local scope**: Project-specific, gitignored
  ```bash
  /plugin install expertise-management --scope local
  ```

## Usage

Once installed, you can use the provided skills:

```bash
/discover-expertise
/expertise-curator
/validate-expertise
/skill-creator
/agent-creator
```

And access the expert agent for brownfield codebase research.

## Development

### Plugin Structure

```
hackathon-2026-ai-agent/
├── .claude-plugin/           # Plugin metadata
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace distribution config
├── .claude/
│   ├── skills/              # Plugin skills
│   │   ├── discover-expertise/
│   │   ├── expertise-curator/
│   │   ├── validate-expertise/
│   │   ├── skill-creator/
│   │   └── agent-creator/
│   └── agents/              # Plugin agents
│       └── expert.md
└── ai-docs/                 # Documentation
```

### Testing Locally

To test the plugin locally during development:

```bash
claude --plugin-dir D:\Repositories\hackathon-2026-ai-agent
```

## Distribution

This plugin is distributed via git repository. When users add the marketplace and install the plugin, Claude Code will:

1. Clone the repository
2. Copy plugin files to the cache directory
3. Make skills and agents available to Claude Code

## License

MIT
