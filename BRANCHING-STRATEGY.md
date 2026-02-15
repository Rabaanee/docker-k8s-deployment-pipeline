# Git Branching Strategy

## Branches
- `main` — Production-ready. Protected. Requires PR + CI pass.
- `develop` — Integration branch. Auto-deploys to dev.
- `feature/*` — Feature work. Branch from develop, PR back to develop.
- `hotfix/*` — Emergency fixes. Branch from main, merge to main + develop.

## Workflow
1. Create feature branch: `git checkout -b feature/add-logging`
2. Commit with conventional commits: `feat:`, `fix:`, `docs:`, `chore:`
3. Push and open PR → CI runs automatically
4. Reviewer approves → Merge → CD deploys to dev
5. Release: merge develop → main → CD deploys to prod (with approval gate)

## Branch Protection (main)
- Require pull request before merging
- Require CI status checks to pass
- Require at least 1 approval
- No direct pushes