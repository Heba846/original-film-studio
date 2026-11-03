# Audit: NarratorAI-Studio/narrator-ai-cli (and why it is optional here)

**Scope of the audit:** a brief read-only look at the public `README.md` and the head of `install.py` on the
`main` branch (fetched as plain text). Nothing was installed, no skill was installed, no API key was created and
**no request was made to its service**. Pricing, licence and server-side behaviour were **not** verified.

## What it is (per its README)
- A CLI client for the hosted "Narrator AI" platform (`ai.jieshuo.cn`) that makes **movie narration / recap videos**:
  pick a movie from "93 built-in movies", match a narration template, auto-write a script, voice it, compose footage.
- Needs an **API key obtained from the vendor** (the README says to email them), configured with
  `narrator-ai-cli config set app_key ...`. A `task budget` command estimates "credits" - i.e. the vendor's own metering.
- Commands such as `file upload` send your files to the vendor's server; narration, voices and composition happen remotely.
- Install is `curl ... install.py | python3`, which clones the repo and creates a virtualenv under your home folder.
- The companion "skill" repo exists to let an AI agent drive the CLI autonomously (including unattended batch runs).

## Why it is optional and NOT part of this toolkit
1. **Different product.** It is built around recapping existing films. Original Film Studio is for the owner's ORIGINAL
   fictional films; recap footage from catalogued third-party movies adds copyright/Content-ID risk and cannot be used for originals.
2. **External paid service, separate billing.** It calls a third-party API with a vendor-issued key and vendor "credits".
   The promotional Claude cloud-session credit pays for Claude model usage inside this session only; it does not
   pay for, or unlock, third-party services. Using it would mean separate sign-up/payment outside Claude - which was out of scope.
3. **Voice/data policy.** The brief is that narration is recorded or cloned by the owner elsewhere and imported. Sending
   scripts/audio/files to a remote narration service contradicts "do not upload audio to external services".
4. **Supply-chain surface.** Piping a remote installer into Python and giving an agent skill authority to run a
   remote-controlling CLI is unnecessary for a local MVP.

The baseline here works fully offline with Python + FFmpeg and **no paid APIs and no credentials**. If the owner ever
wants a hosted narration/video service, wrap it as an *optional, separately-funded* step that outputs a file which is then
imported like any other asset - the pipeline already supports that without code changes.
