# Exploration Categories

When autonomously exploring a codebase, identify expertise in these categories:

## 1. Domain Categories

Business and functional areas:

- **Authentication & Authorization** - User identity, permissions, access control
- **Data Management** - CRUD operations, repositories, data access patterns
- **Business Logic** - Core domain rules, workflows, processes
- **API/Integration** - External service integrations, API clients
- **Messaging/Events** - Event-driven patterns, message queues, pub/sub
- **Payment Processing** - Payment flows, transaction handling
- **User Management** - User profiles, registration, account management
- **Notification System** - Email, SMS, push notifications
- **Search & Discovery** - Search functionality, filtering, indexing
- **Analytics & Reporting** - Metrics, dashboards, data analysis

## 2. Architecture Categories

Technical patterns and structure:

- **Layered Architecture** - Presentation, business logic, data access layers
- **Microservices** - Service boundaries, inter-service communication
- **Event-Driven Architecture** - Event sourcing, CQRS, event handlers
- **API Design** - REST, GraphQL, RPC patterns
- **Data Access** - ORM patterns, query builders, database abstraction
- **Caching Strategy** - Cache layers, invalidation patterns
- **State Management** - Application state, client-side state patterns
- **Error Handling** - Exception patterns, error propagation
- **Logging & Monitoring** - Observability, tracing, metrics
- **Security Patterns** - Input validation, sanitization, CSRF protection

## 3. Technology Stack Categories

Framework and tool-specific patterns:

- **Frontend Framework** - React/Vue/Angular patterns, component structure
- **Backend Framework** - Express/Django/Spring patterns
- **Database** - PostgreSQL/MongoDB/Redis usage patterns
- **Build System** - Webpack/Vite/build configuration
- **Testing** - Test organization, mocking patterns
- **CI/CD** - Deployment pipelines, automation

## 4. Design System Categories

UI/UX patterns (for frontend codebases):

- **Component Library** - Reusable UI components, design tokens
- **Layout Patterns** - Responsive design, grid systems
- **Form Handling** - Validation, submission patterns
- **Navigation** - Routing, menu structures
- **Theming** - Dark mode, customization

## 5. Infrastructure Categories

Deployment and operations:

- **Deployment Strategy** - Blue/green, canary, rolling deployments
- **Configuration Management** - Environment configs, feature flags
- **Database Migrations** - Schema versioning, migration patterns
- **Secrets Management** - Credential storage, key rotation
- **Monitoring & Alerting** - Health checks, alerting rules

## Exploration Strategy

### Start Broad
- Identify major directories and their purposes
- Look for architectural patterns (layers, services, modules)
- Understand technology stack

### Narrow Down
- Within each category, identify specific subdomains
- Look for repeated patterns and conventions
- Find integration points between areas

### Document Relationships
- How do domains interact?
- What are the key integration patterns?
- What are the data flow paths?

## Example Findings

A typical codebase exploration might discover:

**Domain expertise needed:**
- `authentication.yaml` - JWT auth with OAuth2
- `payment-processing.yaml` - Stripe integration patterns
- `notification-system.yaml` - Multi-channel notifications

**Architecture expertise needed:**
- `layered-architecture.yaml` - Controller/Service/Repository pattern
- `event-driven.yaml` - Domain events and handlers
- `api-design.yaml` - REST API conventions

**Design system expertise needed:**
- `component-library.yaml` - Reusable React components
- `form-patterns.yaml` - Form validation and submission
