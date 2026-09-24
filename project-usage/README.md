# Galaxy Bar: model usage, time and API-equivalent cost

Snapshot: **2026-09-24T01:45:24.312Z**. This covers the single Galaxy Bar conversation
beginning 2026-09-20T14:25:46.798Z, before the request for this accounting note.
The accounting/deployment turn itself is excluded. These are resource records,
not evidence of scientific validity or an API invoice.

- Configured model: **GPT-6 Astra**, all 6,976 requests; low/high/xhigh reasoning.
- Total: **1,034,073,460 tokens**.
- Input: 1,028,644,692; cached: 1,001,658,112; uncached:
  26,986,580; cache writes: zero.
- Output: **5,428,768**, including 2,403,599
  reasoning tokens. The reasoning subset is not added to output again.
- Client-recorded reasoning/message intervals: **24.34 hours**;
  context compaction: **3.60 hours**;
  their merged total: **27.94 hours**.
- Active turns: **64.37 hours** including tools and waiting;
  elapsed calendar span: **83.33 hours**.
- Hypothetical API token cost: **$1,542.96 Standard** or
  **$3,085.92 Fast**. Actual service tier is not recorded.

## Where the work went

The original galaxy/control campaign and noisy moving-resonance benchmark take
the largest shares of recorded model time. They included physics design, solver
implementation, numerical checks, interpretation, monitoring, visualization and
publication. These chronological stages overlap kinds of work; they do not
classify private reasoning or imply all activity was numerical research.

| Stage | Total tokens | Model hours | Active hours | Standard USD |
| --- | ---: | ---: | ---: | ---: |
| Galaxy simulations, controls and first website | 457,153,081 | 8.81 | 24.38 | 643.23 |
| Prescribed-field response and numerical diagnostics | 115,949,641 | 4.31 | 8.71 | 195.87 |
| Noisy moving-resonance benchmark and reproduction | 253,806,668 | 8.24 | 17.00 | 388.72 |
| Halo population weighting and response kernels | 93,150,926 | 3.41 | 6.79 | 146.81 |
| Population accuracy diagnostic and estimator cost | 62,818,309 | 2.16 | 4.72 | 95.80 |
| Canonical article, learning guide and editorial releases | 51,194,835 | 1.00 | 2.76 | 72.54 |

## Accounting method and limits

Sum unique `token_usage_record.usage` entries, not their cumulative copies.
The resulting six counters exactly equal the last `thread_token_usage` before
the cutoff. Duplicate response IDs: zero. The much smaller thread-list usage
field is not used as a lifetime counter. Cached context is counted on every
request: total request tokens are not unique text authored by the model.
Model attribution uses turn settings, not independent provider routing logs.
No delegated-agent calls appear; other chats and outside review are excluded.

Durations use client `item_completed` start/end timestamps. Reasoning,
message and context-compaction intervals are merged before summing. Active-turn
intervals use completion/abort timestamp minus reported duration. Overlapping
background commands are not summed into model time. These are latency records,
not provider GPU seconds; they do not separately identify prefill or queueing.
The timing CSVs contain only relative times and item types, never item text.

All requests are below 272,000 input tokens. At the rates checked on 24 September
2026, Standard dollars = (10 × uncached input + 1 × cached input + 12.5 × cache
writes + 50 × output) / 1,000,000. Fast is twice that. Cache writes are an
alternative input rate, not an extra charge added to all input. The recorded
cache-write count is zero. Tools, electricity, hosting, hardware and external
review are excluded. This is not the user's subscription charge.

Sources: [model rates](https://developers.openai.com/api/docs/models/gpt-6-astra),
[pricing and tiers](https://developers.openai.com/api/docs/pricing),
[caching](https://developers.openai.com/api/docs/guides/prompt-caching).

## Inspect or verify

Download `summary.json`, `requests.csv`, `timings.csv`, `turns.csv` and `verify.py`
from this directory; run `python3 verify.py .` (standard library, seconds).
This checks supplied public records; it does not independently authenticate a
private session or execute any astrophysics simulation.

`analyze.py` is the extraction code; rerunning it requires the authorized private
rollout JSONL. That file is not published. Its pre-cutoff SHA256 is recorded in
`summary.json` for the maintainer's provenance. The extractor allowlists metadata
and does not export conversation content, reasoning, tool arguments or host paths.
Use `python3 analyze.py INPUT.jsonl OUTPUT_DIR --cutoff 2026-09-24T01:45:24.312Z`.
