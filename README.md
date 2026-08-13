# PaperGate-IEEE

**Free LaTeX pre-submission risk scanner + optional reviewer-style manuscript audit.**

PaperGate catches avoidable reviewer and submission risks *before* you upload a manuscript: broken labels, weak contribution positioning, missing experimental evidence, over-strong claims, and reliability/calibration gaps.

> **Independent tool. Not affiliated with or endorsed by IEEE.** Always follow the exact, current author instructions of your target publication.

## Try it in 30 seconds

```bash
python paper_gate.py examples/risky_manuscript.tex
```

No package installation. Python 3.9+ is enough.

A deliberately weak sample manuscript scores **38/100 (HIGH RISK)** and triggers findings for broken references, missing calibration evidence, weak novelty positioning, missing ablations, selective-decision gaps, and over-strong claims. See `examples/risky_audit_report.txt`.

For a healthier example:

```bash
python paper_gate.py examples/sample_manuscript.tex
```

Machine-readable output:

```bash
python paper_gate.py main.tex --json --out audit.json
```

## What the free checker audits

- **Submission hygiene:** abstract length/self-containment, labels/references, figures/tables, citation-key consistency when bibliography entries are embedded.
- **Technical story:** introduction, method, evaluation and conclusion visibility; explicit contribution positioning; over-strong claim language.
- **Evidence:** ablations, repeated-run/statistical-variation cues, limitations, implementation/code availability.
- **Industrial relevance:** explicit system/deployment/real-world framing cues.
- **Reliability claims:** if a paper discusses uncertainty/reliability, PaperGate looks for calibration metrics and selective-decision/coverage evidence.

The output is a **0–100 risk-oriented score**, three gate scores, and actionable findings ranked `HIGH`, `MEDIUM`, and `LOW`.

## Why this exists

A paper can be technically strong and still lose reviewer confidence because the contribution is hard to locate, the evidence chain is incomplete, references are broken, the abstract lacks quantitative outcomes, or reliability claims are made without calibration/selective-risk evidence.

PaperGate turns those failure modes into a repeatable preflight check.

## Who it is for

Researchers preparing IEEE-style journal or conference manuscripts, especially work involving industrial AI, edge intelligence, condition monitoring, uncertainty, reliability, or safety-sensitive decision making.

## Need a human-level adversarial audit?

The free scanner is deterministic and intentionally conservative. For manuscript-level reasoning, launch pricing is:

- **Quick Risk Audit — ¥49 / US$7:** top 5 reviewer attack points, novelty/contribution check, missing evidence, and revise/submit recommendation.
- **Full Reviewer Audit — ¥99 / US$15:** prioritized issue ledger covering novelty positioning, method logic, experiment closure, reliability/calibration, industrial relevance, figure/table effectiveness, and likely reviewer objections.

Open a GitHub issue with the **Pro manuscript audit request** form. Start with your target venue, title/anonymized title, and abstract or short summary. Do **not** upload a private manuscript publicly. Payment and private file exchange are arranged only after scope is agreed.

Full scope: `PRO_AUDIT.md`.

## Privacy

The local checker runs entirely on your machine and sends nothing anywhere.

For Pro requests, do not post unpublished manuscripts, confidential data, personal information, account credentials, or proprietary datasets in public GitHub issues.

## Limits

PaperGate is heuristic. It does not decide acceptance, verify scientific truth, replace human peer review, or guarantee compliance with a particular journal. Target-publication requirements change, so the publication's current author instructions remain authoritative.

## Roadmap

- Multi-file LaTeX project support
- `.bib` cross-file validation
- Journal profiles
- HTML report
- Figure readability checks
- Claim-to-evidence traceability

## License

MIT
