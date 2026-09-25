---
name: cv-tailoring
description: Score Daniel's CV against a job description the way an ATS would (details, qualifications, skills, personality traits), tag each JD attribute as knockout / required / preferred / nice-to-have, audit CV consistency, and tailor the CV truthfully. Use when the user pastes a job description, recruiter message, or asks to tailor/score/adapt the CV for a role.
argument-hint: "<job description text or file>"
triggers:
  - user
  - model
---

# CV Tailoring (ATS Scorecard + Truthful Tailoring)

Goal: predict how an Applicant Tracking System (and the recruiter reading its output) would score the CV for a specific job, then close gaps **only with true claims**.

## Sources of truth

Read these before scoring. Never invent experience that is not backed by them or by the user.

| File | Role |
|---|---|
| `.devin/skills/cv-tailoring/candidate-facts.md` | **Verified facts + known gaps + open questions.** Highest authority after the user. Update it whenever the user confirms/denies something. |
| `detailed_cv.qmd` | Detailed CV (Quarto, `classic-cv-pdf`). Best base for tailoring. |
| `danielamievarodriguez_cv.pdf` | Short CV served on the website (generated from `cv types/dar_cv_engineer_short.ods` via `_targets.R` + `AutoCV.qmd`). Extract with `pdftotext -layout`. |
| `work_experience_details/*.md` | Long-form role notes; mine for extra true evidence. |
| `cv types/Example Resume 4 AgileEngine 🚀.txt` | Older resume. Claims here are **unverified** until confirmed in candidate-facts. |
| `index.qmd`, `portfolio.qmd` | Portfolio pages. Also **unverified** for CV purposes. |

## Workflow

### 1. Parse the job description into attributes
Extract every attribute from: explicit "key skills / requirements", responsibilities, location/work-mode, language, seniority, and **implied** attributes (years of experience, degree, work authorization).

### 2. Tag each attribute
| Tag | Rule of thumb |
|---|---|
| **KNOCKOUT** | Binary screening question that auto-rejects: location/work-mode, work authorization, required spoken language level, mandatory certification/clearance, minimum years if stated as "must". |
| **REQUIRED** | Listed under "Key Skills", "Requirements", "Must have", or repeated across title + skills + responsibilities. Usually keyword-matched hard. |
| **PREFERRED** | Appears only in responsibilities; weighted in ranking but not auto-reject. |
| **NICE-TO-HAVE** | "Plus", "bonus", "familiarity", or very new/niche tech that recruiters routinely relax (e.g. a vendor's months-old AI feature), even if listed as key. Say explicitly when a tag is "required on paper, nice-to-have in practice". |
| **IMPLIED** | Not written but standard for the role/company (years from dated roles, degree for background check, English for global consultancies). |

Watch for **false-positive keyword matches** and call them out rather than exploiting them (e.g. "Snowflake schema" data modeling ≠ Snowflake the platform; "Spark" in a course title ≠ production Spark).

### 3. Map evidence
For each attribute cite where it appears (file + section) or mark ❌ missing / ⚠️ partial, plus the nearest *adjacent* true experience.

### 4. Score (per CV version present)
Default weights (adjust if the JD is clearly skill- or seniority-heavy, and say so):

- **Skills 40%**: one line per REQUIRED/PREFERRED/NICE attribute, points proportional to tag weight (required ≈ 15–20, preferred ≈ 5–10, nice ≈ 5).
- **Qualifications 25%**: years computed **from dated roles only** (not the summary claim) /40; degree /25; relevant certifications /15; title-history relevance /20.
- **Details 15%**: contact completeness (phone, email, LinkedIn URL, location, GitHub) /30; location match /25; parseability /25; date consistency /20.
- **Personality traits 20%**: derive 3–4 traits from JD cues (communication/language, ownership, collaboration/client-facing, reliability/optimization); score each from resume evidence.

Parseability checks: run `pdftotext -layout <pdf>` and look for hyphenation splitting keywords, contact info only in header/footer (parsers often drop it), certifications filed under Education, missing degree, year-only dates, multi-column bleed.

State clearly that numbers are estimates of a typical ATS (Workday/Taleo/Phenom/Greenhouse-style), not real system output.

### 5. Consistency audit
Compare every CV version + role notes for conflicting job titles, start/end dates, and metrics. Background-check-heavy employers (large consultancies) verify these. List each conflict and ask the user which is correct; record the answer in `candidate-facts.md`.

### 6. Gap handling (truth rules)
- Missing skill the user **has** → add it with a concrete, true bullet (ask for context if unknown).
- Missing skill the user **lacks** → do not add. Instead surface adjacent experience with honest framing (e.g. "schema-as-code lifecycle with Dataform/dbt" for a Snowflake schema-lifecycle ask) and suggest a talking point for the recruiter call.
- Unknown → ask the user; never guess. Persist the answer in `candidate-facts.md`.

### 7. Tailor (only after the user approves the scorecard)
- Copy `detailed_cv.qmd` to `<company>_<role>_cv.qmd` at repo root (keep the same YAML/`classic-cv-pdf` format) and edit there; do not overwrite the base CVs.
- Mirror JD wording for skills the candidate truly has (exact keyword + common variant, e.g. "CI/CD" and "continuous deployment").
- Reorder bullets so REQUIRED evidence appears first in each role; keep quantified outcomes.
- Always include: phone, LinkedIn URL, location, language section (English level), degree.
- Render with `quarto render <file>.qmd`, then re-run the parse check on the new PDF.
- Report a projected score after tailoring.

## Output template

1. **Attribute tag table**: JD attribute | Tag | Why | Resume evidence.
2. **Scorecard**: one table per category, a column per CV version, then an overall weighted row + knockout status + likely outcome.
3. **Cross-cutting fixes**: consistency conflicts, parse issues, missing contact/language/degree.
4. **Projected score after truthful tailoring** (with and without any unconfirmed skills).
5. **Questions for the user** (only unresolved facts).

Tone: follow the active communication rule (caveman) for chat; tables and CV text in normal professional English.
