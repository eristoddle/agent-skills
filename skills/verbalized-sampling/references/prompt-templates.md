# Verbalized Sampling Prompt Templates

## VS-Standard (Default)

System prompt addition:

```
You are a helpful assistant. For each query, generate a set of {k} possible responses,
each within a separate <response> tag. Each <response> must include a <text> and a
numeric <probability>.
```

## VS-Tail (Creative/Divergent Mode)

Append this constraint to force tail sampling:

```
Sample at random from the tails of the distribution, such that the probability of
each response is less than 0.10.
```

## VS-CoT (Reasoning Mode)

Prepend chain-of-thought before generating the distribution:

```
Think step-by-step about the different ways to approach this query before generating
your responses. Then generate {k} possible responses, each within a separate <response>
tag. Each <response> must include a <text> and a numeric <probability>.
```

## VS-Multi (Multi-Turn Expansion)

After receiving the initial k responses, request additional candidates:

```
Generate {k} more responses that are distinct from the ones above, maintaining the
same <response>, <text>, and <probability> format.
```

## Response Format Example

```xml
<response>
<text>First candidate response here.</text>
<probability>0.08</probability>
</response>

<response>
<text>Second candidate response here.</text>
<probability>0.06</probability>
</response>

<response>
<text>Third candidate response here.</text>
<probability>0.04</probability>
</response>
```

## Parameter Guide

| Parameter | Default | Description |
|-----------|---------|-------------|
| k         | 5       | Number of candidate responses. Use 3 for simple tasks, 5-7 for creative, 10 for maximum diversity. |
| tau (threshold) | 0.10 | Max probability per response. Lower = more divergent. Use 0.05 for extreme creativity. |
| temperature | model default | Orthogonal to VS; can be combined for additional diversity. |
