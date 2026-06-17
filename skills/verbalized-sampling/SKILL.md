---
name: verbalized-sampling
description: "Generate diverse, high-quality responses by producing multiple candidates with probability distributions instead of a single answer. Use when the user asks for brainstorming, creative options, diverse alternatives, original ideas, or when you detect a task that benefits from exploring multiple approaches before committing to one. Also use when explicitly asked for 'verbalized sampling', 'diverse candidates', 'tail sampling', or 'show me options'. Covers creative writing, synthetic data, dialogue simulation, open-ended QA, and any task where mode collapse (repetitive/predictable outputs) is a risk."
---

# Verbalized Sampling

Training-free prompting technique that mitigates LLM mode collapse by generating multiple candidate responses with explicit probability assignments, then selecting from the distribution. Based on [the VS research paper](https://arxiv.org/abs/2510.01171) — achieves 1.6-2.1x diversity increase over direct prompting.

## When to Apply Automatically

Apply VS internally (without the user asking) when detecting:
- Brainstorming or ideation requests
- "Give me something original/creative/unexpected"
- Tasks where the first instinct feels generic or predictable
- Requests for multiple options or alternatives

## Core Workflow

### 1. Generate Candidates

Internally generate k candidate responses using this structure:

```xml
<response>
<text>Candidate response content.</text>
<probability>0.07</probability>
</response>
```

**Default parameters:** k=5 candidates, probability threshold tau=0.10.

### 2. Choose a Mode

| Mode | Instruction | Best for |
|------|-------------|----------|
| **Standard** | Generate k responses with probabilities | General diversity |
| **Tail** | Add: "probability of each response is less than 0.10" | Maximum creativity, breaking patterns |
| **CoT** | Prepend: "Think step-by-step about different approaches first" | Analytical/reasoning tasks |
| **Multi** | Request additional distinct candidates in follow-up turns | Exhaustive exploration |

**Default to Tail mode** for creative tasks. Use Standard for analytical tasks. See [references/prompt-templates.md](references/prompt-templates.md) for exact prompt text.

### 3. Select Output

After generating candidates internally, select using one of these strategies:

- **Present all options** — Show the user all k candidates when they want to choose (human-in-the-loop)
- **Weighted random** — Pick one, weighted by probabilities (default for creative tasks)
- **Best-of-k** — Pick highest probability (default for factual/analytical tasks)
- **Tail pick** — Pick lowest probability for maximum surprise
- **Merge** — Synthesize best elements from multiple candidates

See [references/selection-strategies.md](references/selection-strategies.md) for detailed guidance on each strategy.

### 4. Present the Result

When running VS transparently (user asked for options): show all candidates with brief probability context.

When running VS internally (auto-detected creative task): present only the selected output. Optionally mention that you explored multiple approaches.

## Parameter Tuning

- **k=3**: Simple tasks, quick options
- **k=5**: Default, good balance of diversity and efficiency
- **k=7-10**: Maximum diversity, brainstorming sessions
- **tau=0.10**: Default tail threshold
- **tau=0.05**: Extreme divergence, very unconventional outputs
- **tau=0.20**: Mild diversity, closer to standard generation

## Fork Mode (Advanced)

For complex agentic workflows, execute VS in a "context fork":

1. Spawn a separate reasoning path
2. Generate k candidates with probabilities
3. Evaluate candidates against task requirements internally
4. Return only the best candidate to the main conversation

Use fork mode when the user wants a single polished answer but the task benefits from internal exploration. Do not show the fork process unless asked.
