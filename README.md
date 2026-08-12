# PaperGate-IEEE

**A zero-dependency LaTeX pre-submission auditor for IEEE-style research papers.**

PaperGate catches avoidable reviewer and submission risks *before* you upload a manuscript: broken labels, abstract problems, weak contribution positioning, missing experimental evidence, over-strong claims, and reliability/calibration gaps.

> **Independent tool. Not affiliated with or endorsed by IEEE.** Always follow the exact, current author instructions of your target publication.

## Why this exists

A paper can be technically strong and still lose reviewer confidence because the contribution is hard to locate, the evidence chain is incomplete, references are broken, the abstract lacks quantitative outcomes, or reliability claims are made without calibration/selective-risk evidence.

PaperGate turns those failure modes into a repeatable preflight check.

## 30-second use

```bash
python paper_gate.py main.tex
```

No package installation. Python 3.9+ is enough.

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

## Example

```text
PaperGate-IEEE — Pre-Submission Audit
==========================================
Score: 96/100   Verdict: READY
Gates: submission_hygiene=100 | technical_story=100 | evidence=96
Detected: 5 sections, 1 figures, 0 tables, 1 citations

[01] LOW    | reliability | ...
```

## Who it is for

Researchers preparing IEEE-style journal or conference manuscripts, especially work involving industrial AI, edge intelligence, condition monitoring, uncertainty, reliability, or safety-sensitive decision making.

## Free vs Pro

**Free / open-source:** deterministic preflight checks in this repository.

**Pro manuscript audit (launch offer: ¥99 / US$15):** adversarial reviewer-style audit of one manuscript, delivered as a prioritized issue ledger covering novelty positioning, method logic, experiment closure, claim-evidence consistency, industrial relevance, figure/table redundancy, and likely reviewer attacks. Payment will only be arranged after scope is agreed.

### Request a Pro audit

Open a GitHub issue using the **Pro Audit Request** template. You do **not** need to upload private manuscript files publicly. Start with your title + abstract + target venue; private file transfer/payment can be arranged only after scope is agreed.

## Privacy

The local checker runs entirely on your machine and sends nothing anywhere.

For Pro requests, do not post unpublished manuscripts, confidential data, personal information, account credentials, or proprietary datasets in public GitHub issues.

## Limits

PaperGate is intentionally conservative and heuristic. It does not decide acceptance, verify scientific truth, replace human peer review, or guarantee compliance with a particular journal. Target-publication requirements change, so the publication's current author instructions remain authoritative.

## Roadmap

- Multi-file LaTeX project support
- `.bib` cross-file validation
- Journal profiles
- HTML report
- Figure readability checks
- Claim-to-evidence traceability

## License

MIT
