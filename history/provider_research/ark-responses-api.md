# Ark Responses API Integration Reference

## Status and Authority

- **Recorded:** 2026-08-27
- **Purpose:** Preserve provider-integration evidence for future implementation and troubleshooting.
- **Authority:** This is a non-authoritative research record. Current behavior is owned by `docs/02_AI_System_Design.md`, `docs/05_Backend_Technical_Design.md`, and `planning/PLAN.md`.
- **Privacy:** This record contains no API key, résumé content, job description, follow-up question, prompt, raw provider payload, or generated provider response.

## Provider Documentation

- [Ark document understanding](https://docs.volcengine.com/docs/82379/1902647)
- [Ark structured output for the Responses API](https://docs.volcengine.com/docs/82379/1958523)
- [Ark OpenAI SDK compatibility](https://docs.volcengine.com/docs/82379/1330626)
- [Ark model list](https://docs.volcengine.com/docs/82379/1330310)

The provider clarification received on 2026-08-27 established that documented PDF input for `doubao-seed-2-1-pro-260628` uses Ark's Responses API rather than the Chat Completions endpoint. Inline Base64 PDF transport and strict structured output were validated historically on that path. The current approved MVP no longer sends the PDF: it sends the user-verified fixed Markdown as text and retains the PDF only for recruiter preview/download.

## Approved MVP Mapping

The Goal 7 implementation uses:

- LangChain `ChatOpenAI` with `use_responses_api=True`;
- Ark base URL `https://ark.cn-beijing.volces.com/api/v3`, which resolves the operation to `/api/v3/responses`;
- the exact fixed, user-verified `mei_chang_resume.md` as the first stable `input_text` block;
- dynamic job or conversation content as later `input_text` blocks;
- strict JSON Schema through Responses API `text.format`;
- `thinking={"type": "disabled"}`;
- non-streaming execution;
- `max_retries=0` at the client and one shared two-attempt application budget;
- a finite 180-second timeout per provider attempt;
- `X-Client-Request-Id` correlation with privacy-safe execution logging.

LangChain 1.6 converts the internal text blocks and strict schema used by the current adapter as follows:

```text
text
→ input_text

response_format json_schema
→ text.format json_schema
```

## Validation Evidence

Network-free transport validation confirmed:

- request path `/api/v3/responses`;
- two `input_text` content blocks with the verified résumé text before dynamic content;
- strict `text.format` JSON Schema;
- top-level disabled-thinking setting;
- `stream=false`;
- correlation header propagation.

The historical fixed-PDF public-API test passed for matching and follow-up in approximately 75 seconds. The corrected current test then passed with the verified fixed Markdown and production-shaped strict schemas in 34.28 seconds (35.91 seconds command wall time), with both workflows succeeding on their first attempt. Generated content was not printed or stored in this record, and isolated database records were cleaned by the test fixture.

The native Ark SDK was not added because the primary `ChatOpenAI` Responses path passed the compatibility gate.

## Boundaries and Troubleshooting

Do not replace this path with any of the following without a separately approved design update:

- Files API upload or another provider-managed file lifecycle;
- request-time PDF extraction, preprocessing, page rendering, or RAG;
- streaming output;
- schema weakening or a frontend-visible structured-report contract;
- another model or provider.

When troubleshooting, verify the current official provider documentation and locked dependency behavior before relying on this dated record. Keep diagnostics privacy-safe: record only correlation ID, model/client path, attempt count, duration, validation status, and safe error category.
