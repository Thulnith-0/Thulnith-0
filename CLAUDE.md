# Profile README: notes for Claude

This repo is Thulnith's GitHub profile (`README.md` renders on github.com/Thulnith-0).
`README.md` and `assets/` are generated: edit `.github/profile/content.py`, then run
`python .github/profile/build_static.py`. Live cards are built by
`.github/workflows/profile-cards.yml` (`build_live.py`) and published to the `output` branch.

## The owner's standing preferences

- **Show all repo activity, including private repos.** Repos are private only to hide
  their code. Their names, commit counts and other activity should be shown on the
  profile, never filtered out or lumped into "other". The only exception is the
  owner's explicit hide list, `content.HIDDEN_REPOS` (Carbonware_Website, md,
  MD_Preview, challenge_1): those names stay off the profile and their commits show
  only as a total.
- **Never show the student ID** (e.g. `w2120618`, `20232673`, or the IIT email). Strip
  it from any displayed repo name (`content.STUDENT_ID_PATTERNS`).
- **Count Claude's commits as the owner's.** Commits authored by Claude Code
  (`noreply@anthropic.com`) count as the owner's work (`content.EXTRA_AUTHOR_EMAILS`).
  Other collaborators' commits do not.
- **Look:** premium Apple/Google style, light and dark versions of every image, calm
  motion. No purple on the contribution snake.
- **Snake:** follows real Snake rules (grid moves, no reversing, walls, no self-collision,
  +1 per meal) and must eat every active square.
- Never commit tokens. The stats token is the `PROFILE_TOKEN` repo secret (fine-grained,
  Contents read-only). The email shown on the profile is `thulnithperera870@gmail.com`.
