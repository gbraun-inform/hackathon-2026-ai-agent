# Expertise YAML File Requirements

Expertise files must follow this structure to work with the expert agent.

## Required Structure

```yaml
name: string                    # Short kebab-case name
description: string             # 1-2 sentence overview of what this expertise covers
domain: string                  # Primary domain (e.g., "authentication", "payment-processing")
subdomain: string (optional)    # More specific area within domain

concepts:                       # Key concepts and patterns
  - concept: string             # Name of concept/pattern
    description: string         # What it is and why it matters
    related_files: []           # File patterns where this applies

architectural_decisions:        # Important design decisions
  - decision: string            # What was decided
    rationale: string           # Why this approach was chosen
    tradeoffs: string           # What was gained/lost
    related_files: []           # Where this is implemented

domain_knowledge:               # Business/domain-specific knowledge
  - topic: string               # Subject area
    details: string             # Key information to know
    related_files: []           # Where this is relevant

integration_patterns:           # How this integrates with other parts
  - pattern: string             # Type of integration
    description: string         # How it works
    related_files: []           # Implementation locations

related_files: []               # Top-level file patterns
```

## Guidelines

### Focus on Concepts, Not Implementation Details

Good: "Uses JWT tokens for stateless authentication"
Bad: "The verifyToken() function in auth.js line 42 checks JWT signatures"

### File Patterns

Use glob patterns for related_files:
- `src/auth/**/*.ts` - All auth TypeScript files
- `config/auth*.yaml` - Auth configuration files
- `src/middleware/auth.ts` - Specific file

### Keep It Maintainable

- Avoid overly specific details that change frequently
- Focus on stable architectural patterns
- Don't duplicate information across multiple expertise files
- Keep descriptions concise but complete

### Domains vs Subdomains

- **Domain**: Broad area (authentication, data-access, ui-components)
- **Subdomain**: Specific aspect (oauth2, database-pooling, form-validation)

## Example Expertise File

```yaml
name: authentication
description: JWT-based authentication system with OAuth2 integration for third-party providers
domain: security
subdomain: authentication

concepts:
  - concept: JWT Token Flow
    description: Stateless authentication using JSON Web Tokens with refresh token rotation
    related_files:
      - src/auth/jwt.ts
      - src/middleware/auth-middleware.ts

  - concept: OAuth2 Integration
    description: Third-party authentication via Google and GitHub OAuth2 providers
    related_files:
      - src/auth/oauth/**/*.ts
      - config/oauth.yaml

architectural_decisions:
  - decision: JWT over session-based auth
    rationale: Enables horizontal scaling without session store, reduces database load
    tradeoffs: Cannot invalidate tokens before expiry, slightly larger request size
    related_files:
      - src/auth/jwt.ts

domain_knowledge:
  - topic: Token Expiry Strategy
    details: Access tokens expire in 15 minutes, refresh tokens in 7 days. Refresh token rotation prevents token reuse attacks.
    related_files:
      - config/auth.yaml
      - src/auth/token-manager.ts

integration_patterns:
  - pattern: Middleware Integration
    description: Express middleware validates JWT on protected routes, injects user context
    related_files:
      - src/middleware/auth-middleware.ts
      - src/routes/**/*.ts

related_files:
  - src/auth/**/*.ts
  - src/middleware/auth-middleware.ts
  - config/auth.yaml
```
