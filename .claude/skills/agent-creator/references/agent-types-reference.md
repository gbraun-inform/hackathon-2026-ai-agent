# Agent Types Reference

Common agent archetypes used in Claude Code applications. Choose the pattern that best fits your task.

## 1. Analysis Agents

**Purpose:** Examine data, code, or systems and produce detailed reports or insights.

**Characteristics:**
- Input: Raw data, code, logs, or configuration
- Process: Systematic examination and evaluation
- Output: Structured findings, scores, recommendations
- Timeline: Typically completes in single execution

**Common Tasks:**
- Code quality analysis
- Security vulnerability scanning
- Performance profiling
- Data quality assessment

**Example: Security Code Analyzer**

```python
class SecurityCodeAnalyzer:
    def __init__(self):
        self.checks = [
            "sql_injection_patterns",
            "xss_vulnerabilities",
            "weak_cryptography",
            "insecure_deserialization"
        ]

    def execute(self, code_input):
        findings = []
        for check in self.checks:
            results = self._run_check(check, code_input)
            findings.extend(results)

        return {
            "status": "complete",
            "total_issues": len(findings),
            "critical": len([f for f in findings if f["severity"] == "critical"]),
            "findings": findings
        }
```

**Key Design Points:**
- Clear check/rule definitions
- Scoring or severity levels
- Actionable recommendations
- Traceable results

---

## 2. Automation Agents

**Purpose:** Execute workflows that modify systems, deploy code, or perform operational tasks.

**Characteristics:**
- Input: Task specifications and target systems
- Process: Step-by-step execution with state tracking
- Output: Execution status, changes made, results
- Timeline: May span multiple phases or retry cycles

**Common Tasks:**
- Code deployment and rollback
- Infrastructure provisioning
- Database migrations
- Batch processing

**Example: Deployment Agent**

```python
class DeploymentAgent:
    def execute(self, deployment_spec):
        logger.info(f"Starting deployment to {deployment_spec['target']}")

        phases = [
            self._validate_artifacts,
            self._prepare_environment,
            self._execute_deployment,
            self._verify_deployment,
            self._cleanup
        ]

        for phase in phases:
            result = phase(deployment_spec)
            if result["status"] == "error":
                return self._rollback(deployment_spec)

        return {
            "status": "success",
            "deployed_version": deployment_spec["version"],
            "duration": time.time() - start
        }
```

**Key Design Points:**
- Clear phase progression
- Rollback capabilities
- State verification between phases
- Atomic operations where possible

---

## 3. Research Agents

**Purpose:** Gather information, synthesize findings, and answer complex questions.

**Characteristics:**
- Input: Research questions or topics
- Process: Multi-step information gathering and synthesis
- Output: Comprehensive findings with citations
- Timeline: Iterative - may refine searches multiple times

**Common Tasks:**
- Competitive analysis
- Technology evaluation
- Documentation synthesis
- Trend analysis

**Example: Technology Evaluator**

```python
class TechnologyEvaluator:
    def execute(self, tech_query):
        research_areas = [
            "capabilities",
            "adoption_rate",
            "ecosystem",
            "performance_profile",
            "cost_model"
        ]

        findings = {}
        for area in research_areas:
            findings[area] = self._research_area(tech_query, area)

        evaluation = self._synthesize_findings(findings)

        return {
            "technology": tech_query,
            "evaluation": evaluation,
            "recommendation": self._make_recommendation(evaluation),
            "sources": self._gather_sources(findings)
        }
```

**Key Design Points:**
- Structured research areas
- Source tracking
- Cross-reference validation
- Synthesis logic

---

## 4. Planning Agents

**Purpose:** Break down complex problems and create execution plans.

**Characteristics:**
- Input: Problem statement or goal
- Process: Decomposition, dependency analysis, sequencing
- Output: Step-by-step plan with resource requirements
- Timeline: Single execution producing detailed plan

**Common Tasks:**
- Project planning
- Architecture design
- Implementation roadmapping
- Migration planning

**Example: Implementation Planner**

```python
class ImplementationPlanner:
    def execute(self, feature_spec):
        # Phase 1: Decompose feature into components
        components = self._decompose_feature(feature_spec)

        # Phase 2: Identify dependencies
        dependencies = self._analyze_dependencies(components)

        # Phase 3: Sequence components
        sequence = self._topological_sort(components, dependencies)

        # Phase 4: Estimate effort
        timeline = self._estimate_timeline(sequence)

        # Phase 5: Create implementation plan
        plan = self._create_plan(sequence, timeline)

        return {
            "feature": feature_spec["name"],
            "components": len(components),
            "estimated_effort": timeline["total_hours"],
            "plan": plan,
            "risks": self._identify_risks(plan)
        }
```

**Key Design Points:**
- Clear decomposition logic
- Dependency tracking
- Realistic estimation
- Risk identification

---

## 5. Coordination Agents

**Purpose:** Orchestrate multiple agents or services to solve complex problems.

**Characteristics:**
- Input: Complex task requiring multiple perspectives
- Process: Delegate to specialized sub-agents, aggregate results
- Output: Unified findings incorporating all perspectives
- Timeline: Parallel execution of sub-tasks

**Common Tasks:**
- System health assessments
- Multi-stakeholder decision making
- Cross-functional analysis
- Comprehensive evaluations

**Example: System Health Coordinator**

```python
class SystemHealthCoordinator:
    def __init__(self):
        self.analyzers = {
            "security": SecurityAnalyzer(),
            "performance": PerformanceAnalyzer(),
            "reliability": ReliabilityAnalyzer(),
            "cost": CostAnalyzer()
        }

    def execute(self, system_id):
        # Parallel execution of analyzers
        results = {}
        for name, analyzer in self.analyzers.items():
            results[name] = analyzer.analyze(system_id)

        # Aggregate findings
        executive_summary = self._create_summary(results)

        # Create unified recommendations
        recommendations = self._synthesize_recommendations(results)

        return {
            "system": system_id,
            "overall_health": self._calculate_health_score(results),
            "summary": executive_summary,
            "detailed_findings": results,
            "recommendations": recommendations
        }
```

**Key Design Points:**
- Clear task delegation
- Parallel execution where possible
- Result aggregation logic
- Unified scoring system

---

## 6. Iterative Refinement Agents

**Purpose:** Improve outputs through repeated cycles of generation and evaluation.

**Characteristics:**
- Input: Initial requirements or data
- Process: Generate → Evaluate → Refine cycle
- Output: High-quality result meeting strict criteria
- Timeline: Multiple iterations until criteria met

**Common Tasks:**
- Code generation and optimization
- Content creation and refinement
- Test case generation
- Configuration optimization

**Example: Test Case Generator**

```python
class TestCaseGenerator:
    def execute(self, code_spec):
        test_cases = self._generate_initial_tests(code_spec)
        iteration = 0
        max_iterations = 5

        while iteration < max_iterations:
            coverage = self._calculate_coverage(test_cases, code_spec)

            if coverage >= 0.85:  # Success criteria
                return {
                    "status": "success",
                    "test_cases": test_cases,
                    "coverage": coverage,
                    "iterations": iteration
                }

            gaps = self._identify_coverage_gaps(test_cases, code_spec)
            test_cases = self._add_tests_for_gaps(test_cases, gaps)
            iteration += 1

        return {
            "status": "partial",
            "test_cases": test_cases,
            "coverage": coverage,
            "iterations": iteration
        }
```

**Key Design Points:**
- Clear quality metrics
- Refinement strategy
- Iteration limits to prevent loops
- Partial success handling

---

## 7. Validation Agents

**Purpose:** Verify correctness, compliance, or quality of inputs or outputs.

**Characteristics:**
- Input: Items to validate against criteria
- Process: Systematic validation against rules
- Output: Pass/fail with detailed feedback
- Timeline: Can process multiple items

**Common Tasks:**
- Configuration validation
- Data integrity checking
- Compliance verification
- Output quality validation

**Example: Configuration Validator**

```python
class ConfigurationValidator:
    def __init__(self):
        self.rules = {
            "required_fields": [...],
            "type_constraints": {...},
            "value_ranges": {...},
            "dependency_rules": [...]
        }

    def execute(self, config):
        issues = []

        # Check required fields
        issues.extend(self._validate_required_fields(config))

        # Check types
        issues.extend(self._validate_types(config))

        # Check value ranges
        issues.extend(self._validate_ranges(config))

        # Check dependencies
        issues.extend(self._validate_dependencies(config))

        return {
            "valid": len(issues) == 0,
            "issue_count": len(issues),
            "issues": issues,
            "config": config if len(issues) == 0 else None
        }
```

**Key Design Points:**
- Comprehensive rule set
- Detailed issue reporting
- Clear validation hierarchy
- Actionable feedback

---

## Choosing Your Agent Type

| Task Type | Best Agent Type | Why |
|-----------|-----------------|-----|
| Find bugs or vulnerabilities | Analysis | Systematic examination, structured output |
| Deploy code or infrastructure | Automation | State tracking, error recovery, validation |
| Answer research questions | Research | Multi-step information gathering, synthesis |
| Create implementation roadmap | Planning | Decomposition, sequencing, estimation |
| Complex multi-perspective task | Coordination | Parallel sub-tasks, aggregation |
| Generate high-quality content | Iterative Refinement | Quality metrics, repeated improvement |
| Ensure compliance or quality | Validation | Rule-based checking, detailed feedback |

---

## Agent Composition

You can combine agent types:

```
Complex Application
├── Planning Agent (creates roadmap)
├── Validation Agent (checks plan)
├── Coordination Agent (orchestrates specialists)
│   ├── Architecture Agent (analysis)
│   ├── Security Agent (analysis)
│   └── Performance Agent (analysis)
└── Reporting Agent (synthesizes findings)
```

This modular approach keeps agents focused and reusable.
