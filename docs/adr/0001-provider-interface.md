# ADR 0001: Provider Interface

## Decision

Every source should implement a provider that returns a shared `CapturedItem`.

## Reason

The UI and Obsidian writer should not know whether content came from Reddit, GitHub, or a future source.
