# Selection Strategies

After generating k candidates with probabilities, select the final output using one of these strategies.

## Weighted Random (Default)

Sample one response weighted by assigned probabilities. Preserves the distribution shape while narrowing to a single output. Best for creative tasks where you want controlled randomness.

## Best-of-k

Select the response with the highest probability. Use when you want the model's own assessment of quality. Good for factual or analytical tasks where diversity in generation is useful but the final answer should be "best."

## Lowest Probability (Tail Pick)

Select the response with the lowest probability. Forces maximally divergent output. Use for brainstorming, breaking out of patterns, or generating surprising alternatives.

## Human-in-the-Loop

Present all k candidates to the user and let them choose. Best for collaborative workflows where the user wants to see options before committing.

## Ensemble / Merge

Synthesize elements from multiple candidates into a single response. Use when candidates each capture different valuable aspects of the answer.

## Filtering Then Selection

Apply quality filters first (factual accuracy, safety, relevance), then select from remaining candidates. Use for tasks where diversity is desired but constraints are non-negotiable.
