# Candidate Facts: Daniel Amieva Rodriguez

Source of truth for the `cv-tailoring` skill. Update this file whenever the user confirms or denies something.

## Confirmed by user

| Topic | Fact | Confirmed |
|---|---|---|
| English | Fluent (state as "English: Fluent / C2" in language section) | 2026-09-24 |
| Terraform | Has used Terraform (role/context not yet specified) | 2026-09-24 |
| AWS CloudFormation | Has used CloudFormation (role/context not yet specified; SAM at TeamStation is CloudFormation-based) | 2026-09-24 |
| Informatica | **Never used.** Do not claim. Adjacent: Glue, DMS, Python ETL with 10+ enterprise API integrations | 2026-09-24 |
| Snowflake (platform) | **Not currently using.** Do not claim current use. | 2026-09-24 |
| Location | Mexico City, Mexico | CV |

## Known false-positive keywords (never exploit)

- "Snowflake schema" in `work_experience_details/teamstation_detailed.md`, `portfolio.qmd`, `index.qmd` is the **data modeling pattern**, not the Snowflake platform.

## Known CV gaps (fix in every tailored CV)

- No phone number.
- No LinkedIn URL (email is a passmail relay).
- No language section (ODS `language_skills` sheet exists but is not rendered).
- Short CV (`danielamievarodriguez_cv.pdf`): Education section lists only certifications, no UNAM degree; only 2023+ roles dated, so ATS computes ~3 yrs despite "6+ years" summary; DiDi and DGTIC UNAM roles omitted.
- Terraform / CloudFormation missing from both CVs despite real use.

## Open questions (ask before tailoring)

1. **Snowflake past use**: ever used Snowflake the platform in a past job/project? If yes: where, what (loading, modeling, deployments)?
2. **Terraform / CloudFormation context**: which role(s), what was provisioned?
3. **Conflicting titles/dates/metrics across CV versions**: which is correct?
   - Rackspace title: "Senior Business Developer Engineer" (short CV) vs "Business Intelligence Engineer IV" (detailed CV)
   - Baz title: "Business Developer Engineer" (short CV + AgileEngine resume) vs "Senior BI Engineer" (detailed CV)
   - TeamStation start: 2024 (`teamstation_detailed.md`) vs 2025 (both CVs)
   - Rackspace savings: USD 500,000 (short CV) vs USD 1,000,000 (detailed CV)
4. **Phone + LinkedIn URL** to include.
5. **AgileEngine resume claims** (Databricks, Snowflake, Docker, Looker, DGTIC UNAM 2019–2021 Data Engineer role): which are real?

## Application log

| Date | Company / Role | Base CV | Est. score before → after | Notes |
|---|---|---|---|---|
| 2026-09-24 | Cognizant / Data Engineer (AWS, Snowflake, Cortex Code, GitHub Actions, CI/CD, Informatica) | detailed_cv.qmd | ~68 → ~75–78 (no Snowflake) | Knockouts: location ✅, English ✅ (fluent, must be added). Main gap: Snowflake + Informatica (not held). Pitch: GitHub Actions CI/CD, AWS serverless + SAM/CloudFormation + Terraform, schema-as-code via Dataform/dbt. |
