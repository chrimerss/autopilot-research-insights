# autopilot-research-insights

A minimal, auto-updating **research-insights dashboard** for Zhi Li (Allen Li). Drop a paper
PDF into [`interest/`](interest/), and a GitHub Action reads it with Claude, writes a 5-part
insight grounded in your own publications, and opens a Pull Request that adds it to the site.

**Live site:** https://chrimerss.github.io/autopilot-research-insights/
&nbsp;·&nbsp; **About / methodology:** https://chrimerss.github.io/autopilot-research-insights/project.html

---

## How it works

```
You:    add interest/<slug>/paper.pdf  →  git push
Action: read PDF (Claude) → extract text + a figure → synthesize a 5-section insight
        grounded in _data/publications.yml → open a run-scoped Pull Request
You:    review the PR → merge → GitHub Pages rebuilds → the card appears under its subject tab
```

Each insight has five sections: **Summary & Key Contributions · Connections to My Work ·
Critique & Limitations · Gaps & Ideas · How to Advance/Disrupt the Field** (with recommended
data and methods). The dashboard is organized as **subject tabs → dated accordion cards**.

## Adding a paper

1. Put the paper's PDF in a folder under `interest/` — the folder name becomes the card id, and
   the PDF can be named anything (e.g. `interest/brown-ocean-effect/brown-ocean-effect.pdf` or
   `interest/brown-ocean-effect/paper.pdf`; if several PDFs are in the folder, `paper.pdf` wins).
   You can also upload via the GitHub web UI.
2. Push. Within a few minutes a PR titled `Insights: …` appears.
3. Review and merge. The site updates automatically.

The Action also commits the extracted `interest/<slug>/paper.md` (main text) and a representative
figure under `assets/figures/<slug>/`. Nothing is committed for a paper whose insight fails to
generate, so a bad run never leaves half-baked files.

## Setup

One-time, after the repo exists:

```bash
# 1. Add your Anthropic API key as a repo secret (this is the only secret needed).
gh secret set ANTHROPIC_API_KEY --repo chrimerss/autopilot-research-insights

# 2. Allow GitHub Actions to open pull requests (required, or the PR step 403s).
gh api -X PUT repos/chrimerss/autopilot-research-insights/actions/permissions/workflow \
  -F default_workflow_permissions=write -F can_approve_pull_request_reviews=true

# 3. Enable GitHub Pages (build from the main branch).
gh api -X POST repos/chrimerss/autopilot-research-insights/pages \
  -f build_type=legacy -f 'source[branch]=main' -f 'source[path]=/'
```

> If your account is under an organization/Enterprise, a higher-tier policy can still block
> step 2; an org admin must allow Actions to create PRs.

### Model (optional)

The analyzer uses `claude-sonnet-4-6` by default. To use Opus instead, set the repo variable to
the **full** model id:

```bash
gh variable set INSIGHTS_MODEL --repo chrimerss/autopilot-research-insights --body claude-opus-4-8
```

### Using AWS Bedrock instead of the Anthropic API

The analyzer is provider-flexible. To run Claude via **AWS Bedrock** with **GitHub OIDC**
(no long-lived AWS keys in the repo):

1. **Enable model access** in the AWS Console → Bedrock → *Model access* for the Claude model
   you want, in your region.

2. **One-time: an IAM OIDC provider for GitHub** (skip if your account already has one):
   ```bash
   aws iam create-open-id-connect-provider \
     --url https://token.actions.githubusercontent.com \
     --client-id-list sts.amazonaws.com \
     --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
   ```

3. **An IAM role the Action can assume.** Save `trust.json` (replace `<ACCOUNT_ID>`):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Principal": { "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com" },
       "Action": "sts:AssumeRoleWithWebIdentity",
       "Condition": {
         "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
         "StringLike": { "token.actions.githubusercontent.com:sub": "repo:chrimerss/autopilot-research-insights:*" }
       }
     }]
   }
   ```
   and `bedrock.json` (replace `<REGION>` and `<ACCOUNT_ID>`):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
       "Resource": [
         "arn:aws:bedrock:<REGION>::foundation-model/anthropic.claude-*",
         "arn:aws:bedrock:*:<ACCOUNT_ID>:inference-profile/*"
       ]
     }]
   }
   ```
   then:
   ```bash
   aws iam create-role --role-name research-insights-bedrock \
     --assume-role-policy-document file://trust.json
   aws iam put-role-policy --role-name research-insights-bedrock \
     --policy-name bedrock-invoke --policy-document file://bedrock.json
   ```

4. **Point the repo at Bedrock** (no `ANTHROPIC_API_KEY` needed):
   ```bash
   R=chrimerss/autopilot-research-insights
   gh variable set INSIGHTS_PROVIDER --repo $R --body bedrock
   gh variable set AWS_REGION        --repo $R --body <REGION>
   gh variable set AWS_ROLE_ARN      --repo $R --body arn:aws:iam::<ACCOUNT_ID>:role/research-insights-bedrock
   # Bedrock model/inference-profile id — e.g. an Opus 4.x profile in your region:
   gh variable set INSIGHTS_MODEL    --repo $R --body us.anthropic.claude-opus-4-1-20250805-v1:0
   ```

The workflow assumes the role via OIDC and the script uses `AnthropicBedrock`. `INSIGHTS_MODEL`
**must** be a Bedrock model/inference-profile id (the `us.anthropic.claude-...-v1:0` form), not the
direct-API name. To switch back to the direct API, set `INSIGHTS_PROVIDER=anthropic` and add the
`ANTHROPIC_API_KEY` secret.

### Adding research history (optional, improves synthesis)

`_data/publications.yml` is already seeded with your 20 most-recent Scholar papers, which is
enough for the "Connections to My Work" grounding. For deeper, full-text connections, add the
paper's main text as `published/<slug>.md` (see [`published/README.md`](published/README.md)).

## Local development

```bash
# Site (requires Ruby; GitHub Pages builds this for you on push):
bundle install
bundle exec jekyll serve            # → http://localhost:4000/autopilot-research-insights/

# Analyzer — zero-API-spend smoke test and unit tests:
python -m venv .venv && . .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/analyze_paper.py --dry-run interest/<slug>/paper.pdf   # canned response, no spend
python -m unittest scripts.test_analyze -v

# Generate a real insight locally instead of in CI (uses your ANTHROPIC_API_KEY):
python scripts/analyze_paper.py --local interest/<slug>/paper.pdf
```

## Figures & fair use

A representative figure may be extracted from a third-party paper and shown on its card, under
academic **fair-use / scholarly-commentary** for non-commercial research discussion; every card
links to the original source. Delete `assets/figures/<slug>/` in the PR to suppress one.

## Layout

```
_config.yml                 Jekyll config (baseurl /autopilot-research-insights)
_data/subjects.yml          subject tabs (seeded; analyzer may append new ones last)
_data/publications.yml      research history (grounds the insights)
_insights/<date>-<slug>.md  generated insight cards (Jekyll collection)
_layouts/ _includes/ _sass/ dashboard layout, tabs/card includes, styling
assets/                     compiled CSS, tab JS, extracted figures
interest/<slug>/paper.pdf   INPUT: papers you add
published/<slug>.md         your research history (full text, optional)
scripts/analyze_paper.py    the analysis pipeline (+ tests, fixtures)
.github/workflows/          the push-triggered Action
project.html                methodology + build/run log (served live)
```
