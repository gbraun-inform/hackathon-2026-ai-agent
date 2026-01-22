---
name: discover-expertise
description: Discover and generate expertise files for new codebases. Use when a user wants to bootstrap expertise for an unfamiliar codebase or systematically document architectural patterns, domains, and design decisions. This skill guides a multi-phase workflow of interviewing, autonomous exploration, user feedback, and targeted expertise file generation.
---

# Discover Expertise

## Overview

This skill helps discover and generate expertise YAML files for brownfield codebases. It guides a structured 4-phase workflow: (1) interview user about the codebase, (2) autonomously explore to identify domains and patterns, (3) present findings and gather user feedback, (4) generate expertise files that work with the expert agent.

## Workflow

### Phase 1: User Interview

Ask the user about their codebase to establish exploration context. Use the AskUserQuestion tool to gather information in these areas:

**Questions to ask:**

1. **Domains and Subdomains**
   - "What are the main functional areas or domains in your codebase? (e.g., authentication, payment processing, user management, notifications)"
   - "Are there any specific subdomains or specialized areas we should focus on?"

2. **Architecture Patterns**
   - "What architectural patterns does your codebase use? Select all that apply:"
     - Layered architecture (presentation/business/data layers)
     - Microservices
     - Event-driven architecture
     - MVC/MVVM
     - Other/Not sure

3. **Technology Context**
   - "What is your primary tech stack? (e.g., React + Node.js + PostgreSQL, Django + React, Spring Boot + MongoDB)"

4. **Documentation Goals**
   - "What would you like the expertise system to help with?"
     - Understanding existing architecture
     - Onboarding new developers
     - Documenting domain knowledge
     - Capturing design decisions
     - All of the above

**Important:** Keep the interview concise. Don't overwhelm the user with too many questions. Focus on gathering enough context to guide autonomous exploration.

### Phase 2: Autonomous Exploration

Use the interview responses to guide systematic codebase exploration. Spawn multiple Explore subagents in parallel to efficiently map the codebase.

**Exploration strategy:**

1. **Spawn Parallel Explorers** - Launch multiple Task tool calls with subagent_type=Explore in a SINGLE message to explore different areas concurrently:
   - Directory structure and organization
   - Each domain mentioned by user
   - Technology-specific patterns (based on tech stack)
   - Common architectural patterns

2. **Exploration Categories** - Look for expertise in these areas (see references/exploration-categories.md for complete list):
   - **Domain categories**: Authentication, data management, business logic, API integration, payment processing, etc.
   - **Architecture categories**: Layered architecture, event-driven patterns, API design, data access, caching, state management, etc.
   - **Technology stack categories**: Framework-specific patterns, database usage, build systems, testing patterns
   - **Design system categories** (if frontend): Component library, layout patterns, form handling, theming
   - **Infrastructure categories**: Deployment strategy, configuration management, database migrations

3. **What to Look For**:
   - Repeated patterns and conventions
   - Architectural decisions (why was X chosen over Y?)
   - Integration points between domains
   - Business logic and domain rules
   - Design system patterns
   - Technology-specific idioms

**Output from Phase 2:** A comprehensive map of potential expertise areas, including:
- List of domains identified
- Architectural patterns found
- Key integration points
- Suggested expertise files to create

### Phase 3: Present Findings and Gather Feedback

Present the discovered domains and patterns to the user. For each potential expertise file, get user feedback using AskUserQuestion.

**Presentation format:**

```markdown
## Discovered Expertise Areas

Based on exploration, I've identified these potential expertise files:

### Domain Expertise
1. **authentication** - JWT-based auth with OAuth2 integration
2. **payment-processing** - Stripe payment flows and webhooks
3. **notification-system** - Multi-channel notifications (email, SMS, push)

### Architecture Expertise
4. **layered-architecture** - Controller/Service/Repository pattern
5. **event-driven** - Domain events with event handlers
6. **api-design** - REST API conventions and patterns

### [Other Categories]
...
```

**For each expertise file**, use AskUserQuestion with multiSelect=false:

```
Question: "Should I generate expertise for: [expertise-name]?"
Options:
  - "Yes - Generate this expertise" (Recommended if high confidence)
  - "No - Skip this expertise"
  - "Adjust - Needs modification"
```

If user selects "Adjust", follow up with a clarifying question about what should be changed.

**Important:**
- Present findings clearly and concisely
- Group by category (domain, architecture, design, infrastructure)
- Explain what each expertise would cover
- Don't ask about more than 8-10 expertise files at once (split into multiple rounds if needed)

### Phase 4: Generate Expertise Files

For each approved expertise file, spawn a specialized subagent to deeply explore that specific area and generate the YAML file.

**Generation process:**

1. **Spawn Expertise Generator** - For each approved expertise, use Task tool with subagent_type=general-purpose:

```
Prompt: "Generate expertise file for [domain/pattern name].

Context: [Summary of what was discovered about this area]

Requirements:
1. Deep dive into [specific file patterns or areas]
2. Identify concepts, architectural decisions, domain knowledge, integration patterns
3. Follow the expertise YAML structure from assets/expertise-template.yaml
4. See references/expertise-requirements.md for detailed structure requirements
5. Write the expertise file to expertise/[name].yaml

Focus on:
- Key concepts and patterns (not implementation details)
- Architectural decisions and rationale
- Domain-specific knowledge
- Integration patterns with other parts of codebase
- Use glob patterns for related_files

Generate a high-quality, conceptual expertise file that will help future exploration of this area."
```

2. **Run Generators in Parallel** - Launch multiple Task calls in a SINGLE message for efficiency

3. **Validate Generated Files** - After generation, use the validate-expertise skill to check each file:
   ```
   Skill: validate-expertise
   Args: expertise/[name].yaml
   ```

4. **Report Results** - Summarize what was generated:
   ```markdown
   ## Generated Expertise Files

   Created [N] expertise files:
   - `expertise/authentication.yaml` - JWT auth with OAuth2
   - `expertise/payment-processing.yaml` - Stripe integration patterns
   - `expertise/layered-architecture.yaml` - Controller/Service/Repository pattern

   All files validated successfully.
   ```

## Guidelines

### Keep User in the Loop

- Interview phase: Be conversational, don't overwhelm
- Presentation phase: Be clear about what each expertise covers
- Generation phase: Report progress and results

### Prioritize Quality Over Quantity

- Better to have 5 high-quality expertise files than 20 superficial ones
- Focus on stable, architectural knowledge
- Avoid overly specific implementation details

### Use Parallel Execution

- Phase 2: Spawn multiple explorers in a single message
- Phase 4: Generate multiple expertise files in parallel
- This significantly speeds up the workflow

### Validate Everything

- Use validate-expertise skill after generating each file
- Fix any validation errors before moving to next file
- Ensure files match the requirements in references/expertise-requirements.md

## Resources

### References

- **expertise-requirements.md** - Detailed YAML structure requirements for expertise files
- **exploration-categories.md** - Categories and patterns to look for during exploration

### Assets

- **expertise-template.yaml** - Template structure for generating expertise files

## Example Usage

**User:** "Help me create expertise files for my e-commerce platform"

**Skill execution:**
1. Interview: Ask about domains (products, cart, checkout, etc.), architecture (microservices? monolith?), tech stack
2. Explore: Spawn parallel explorers for product catalog, shopping cart, payment processing, user management, API patterns
3. Present: Show discovered expertise areas, get feedback on which to generate
4. Generate: Create approved expertise files with deep exploration of each area
5. Validate: Run validate-expertise on all generated files
6. Report: Summary of created expertise files

**Result:** A bootstrapped expertise system ready for use with the expert agent.
