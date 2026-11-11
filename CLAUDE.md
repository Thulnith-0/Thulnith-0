# Profile README: notes for Claude

This repo is Thulnith's GitHub profile (`README.md` renders on github.com/Thulnith-0).
`README.md` and `assets/` are generated: edit `.github/profile/content.py`, then run
`python .github/profile/build_static.py`. Live cards are built by
`.github/workflows/profile-cards.yml` (`build_live.py`) and published to the `output` branch.

## The owner's standing preferences

- **Show all repo activity, including private repos.** Repos are private only to hide
  their code. Their names, commit counts and other activity should be shown on the
  profile, never filtered out or lumped into "other". The only exception is the
  owner's explicit hide list, `content.HIDDEN_REPO_HASHES` (stored as hashes so the
  names can't be read in this public repo): those names stay off the profile and their
  commits show only as a total. Never write a hidden repo's name into any file here.
- **Some projects are kept off the profile by name** (their repos are on the hidden
  list): no project cards, timeline points, repo names or headline mentions for them.
  If unsure whether a project is one of them, ask the owner before adding it.
- **Repo lists show the top repos by commits** (top 7 in "Contributed to", top 10 in
  "Top repositories"), re-ranked on every build; the rest are a "+ N more" total.
- **Never show the student ID** (e.g. `w2120618`, `20232673`, or the IIT email). Strip
  it from any displayed repo name (`content.STUDENT_ID_PATTERNS`).
- **Count Claude's commits as the owner's.** Commits authored by Claude Code
  (`noreply@anthropic.com`) count as the owner's work (`content.EXTRA_AUTHOR_EMAILS`).
  Other collaborators' commits do not.
- **Look:** premium Apple/Google style, light and dark versions of every image, calm
  motion. **No purple anywhere**: the accent is a blue-to-teal gradient
  (`design.THEMES[*]["grad"]`). No light-sweep "shine"; the card effect is a subtle
  gradient border flow (`design.border_flow`).
- **Snake:** follows real Snake rules (grid moves, no reversing, walls, no self-collision,
  +1 per meal) and must eat every active square.
- Never commit tokens. The stats token is the `PROFILE_TOKEN` repo secret (fine-grained,
  Contents read-only). The email shown on the profile is `thulnithperera870@gmail.com`.
