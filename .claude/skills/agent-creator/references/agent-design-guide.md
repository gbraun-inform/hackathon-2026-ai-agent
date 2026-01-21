# Agent Design Guide

This guide covers design patterns, architectural decisions, and workflow planning for Claude Code agents.

## Design Patterns

### 1. Sequential Workflow Pattern

**When to use:** Tasks with clear, step-by-step procedures where each step depends on the previous one.

```
Phase 1: Input Processing
  ↓
Phase 2: Analysis
  ↓
Phase 3: Decision Making
  ↓
Phase 4: Action Execution
  ↓
Phase 5: Output Generation
```

**Example:** Code analysis agent
1. Load and parse code
2. Identify patterns and issues
3. Prioritize findings
4. Generate recommendations
5. Format report

**Implementation:**
```python
def execute(self, task_input):
    # Phase 1
    data = self._process_input(task_input)

    # Phase 2
    analysis = self._analyze(data)

    # Phase 3
    decisions = self._make_decisions(analysis)

    # Phase 4
    results = self._execute_actions(decisions)

    # Phase 5
    output = self._format_output(results)

    return output
```

### 2. Decision Tree Pattern

**When to use:** Tasks requiring different paths based on conditions.

```
Start
  ↓
Condition Check
  ├─ Branch A → Actions → Merge
  ├─ Branch B → Actions → Merge
  └─ Branch C → Actions → Merge
  ↓
Final Processing
  ↓
Output
```

**Example:** Deployment agent
- If production: rigorous validation
- If staging: standard validation
- If development: minimal validation

**Implementation:**
```python
def execute(self, task_input):
    env = self._detect_environment(task_input)

    if env == "production":
        return self._deploy_production(task_input)
    elif env == "staging":
        return self._deploy_staging(task_input)
    else:
        return self._deploy_development(task_input)
```

### 3. Iterative Refinement Pattern

**When to use:** Tasks requiring quality improvement through repeated cycles.

```
Initial Pass
  ↓
Evaluate
  ├─ Meets criteria → Return
  └─ Needs improvement
      ↓
    Refine
      ↓
    Evaluate (repeat)
```

**Example:** Report generation agent
1. Generate initial report
2. Evaluate against criteria
3. If gaps identified, refine and retry
4. Repeat until meets quality standard

**Implementation:**
```python
MAX_ITERATIONS = 3

def execute(self, task_input):
    result = self._generate_initial(task_input)

    for attempt in range(MAX_ITERATIONS):
        if self._meets_criteria(result):
            return result

        gaps = self._identify_gaps(result)
        result = self._refine(result, gaps)

    return result
```

### 4. Multi-Agent Coordination Pattern

**When to use:** Complex tasks that can be decomposed into independent sub-tasks.

```
Coordinator
  ├─ Agent 1 (parallel)
  ├─ Agent 2 (parallel)
  ├─ Agent 3 (parallel)
  └─ Aggregator → Output
```

**Example:** System analysis with multiple agents
- Security analyzer
- Performance analyzer
- Cost analyzer
- Results aggregator

**Implementation:**
```python
def execute(self, task_input):
    results = {
        "security": self._run_security_agent(task_input),
        "performance": self._run_performance_agent(task_input),
        "cost": self._run_cost_agent(task_input),
    }

    return self._aggregate_results(results)
```

## Error Handling Strategies

### Retry with Backoff

```python
def _call_with_retry(self, func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # exponential backoff
                logger.info(f"Retry {attempt + 1} after {wait_time}s")
                time.sleep(wait_time)
            else:
                logger.error(f"Failed after {max_retries} attempts")
                raise
```

### Graceful Degradation

```python
def execute(self, task_input):
    try:
        primary_result = self._use_premium_tool(task_input)
    except ToolUnavailable:
        logger.warning("Premium tool unavailable, using fallback")
        primary_result = self._use_fallback_tool(task_input)

    return primary_result
```

### Partial Success Handling

```python
def execute(self, task_input):
    results = []
    errors = []

    for item in task_input:
        try:
            result = self._process_item(item)
            results.append(result)
        except Exception as e:
            errors.append({"item": item, "error": str(e)})

    return {
        "success": results,
        "failed": errors,
        "status": "partial" if errors else "complete"
    }
```

## Input Validation

Always validate input early:

```python
def execute(self, task_input):
    # Validate input format
    if not isinstance(task_input, dict):
        raise ValueError("Input must be a dictionary")

    # Validate required fields
    required_fields = ["source", "target"]
    for field in required_fields:
        if field not in task_input:
            raise ValueError(f"Missing required field: {field}")

    # Validate field values
    if not isinstance(task_input["source"], str):
        raise ValueError("source must be a string")

    # Proceed with processing
    return self._process(task_input)
```

## State Management

### Lightweight State Tracking

```python
class MyAgent:
    def __init__(self):
        self.state = {
            "current_phase": None,
            "items_processed": 0,
            "errors_encountered": [],
            "start_time": None
        }

    def execute(self, task_input):
        self.state["start_time"] = time.time()
        self.state["current_phase"] = "initialization"

        # ... rest of execution ...

        self.state["items_processed"] = len(results)
        return self._format_output()
```

### Checkpoint-based Recovery

```python
def execute(self, task_input):
    checkpoint_file = f"checkpoint_{task_input['id']}.json"

    # Resume from checkpoint if available
    if os.path.exists(checkpoint_file):
        state = self._load_checkpoint(checkpoint_file)
        logger.info(f"Resuming from checkpoint")
    else:
        state = self._initialize_state(task_input)

    while not state["complete"]:
        state = self._execute_phase(state)
        self._save_checkpoint(checkpoint_file, state)

    return state["results"]
```

## Logging and Debugging

Include strategic logging at key points:

```python
def execute(self, task_input):
    logger.info(f"Agent started with input: {task_input}")

    try:
        logger.debug(f"Phase 1: Starting analysis")
        analysis = self._analyze(task_input)
        logger.debug(f"Phase 1: Completed, found {len(analysis)} items")

        logger.debug(f"Phase 2: Starting processing")
        results = self._process(analysis)
        logger.info(f"Phase 2: Completed, processed {len(results)} items")

        return results
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
        raise
```

## Performance Optimization

### Token Usage Considerations

1. **Minimize context**: Only load necessary references
2. **Reuse results**: Cache intermediate results when appropriate
3. **Batch operations**: Process multiple items in single passes
4. **Streaming**: For large outputs, stream results incrementally

### Execution Time Optimization

1. **Parallel processing**: Run independent tasks concurrently
2. **Early termination**: Stop as soon as criteria are met
3. **Lazy evaluation**: Only compute what's needed
4. **Timeout handling**: Set reasonable timeouts on long operations

```python
def execute(self, task_input):
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(self._process_batch, batch): i
            for i, batch in enumerate(self._split_input(task_input))
        }

        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    return self._merge_results(results)
```

## Testing Agent Workflows

### Unit Testing Individual Steps

```python
def test_analysis_step():
    agent = MyAgent()
    input_data = {"key": "value"}
    result = agent._analyze(input_data)
    assert len(result) > 0
    assert all("score" in item for item in result)
```

### Integration Testing Complete Workflow

```python
def test_full_execution():
    agent = MyAgent()
    input_data = build_test_input()
    result = agent.execute(input_data)

    assert result["status"] == "success"
    assert len(result["data"]) > 0
```

### Testing Error Scenarios

```python
def test_error_handling():
    agent = MyAgent()
    invalid_input = {"incomplete": "data"}

    with pytest.raises(ValueError):
        agent.execute(invalid_input)
```

## Documentation Template

Every agent should include clear documentation:

- **Purpose**: What the agent does in one sentence
- **Inputs**: Exact format and required fields
- **Outputs**: Exact format of results
- **Workflow**: Step-by-step process description
- **Success Criteria**: When work is considered done
- **Error Handling**: How failures are managed
- **Performance Notes**: Typical execution time and token usage
- **Configuration**: Any tunable parameters
- **Examples**: Real usage examples

See AGENT.md template for complete structure.
