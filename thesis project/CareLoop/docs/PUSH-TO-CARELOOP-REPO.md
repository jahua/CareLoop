# Pushing CareLoop to github.com/jahua/CareLoop

Your main repo is **thesis-papeer** (whole thesis project). The **CareLoop** code lives under `thesis project/CareLoop/`. To sync that folder to [github.com/jahua/CareLoop](https://github.com/jahua/CareLoop):

## Option A: Add remote and push using subtree (from thesis repo root)

Run from **the 2026 repo root** (parent of `thesis project/`), i.e. `/Users/huaduojiejia/MyProject/hslu/2026`:

```bash
# Add the CareLoop repo as a remote (run once)
git remote add careloop https://github.com/jahua/CareLoop.git

# Push only the CareLoop subtree to careloop/main
git subtree push --prefix="thesis project/CareLoop" careloop main
```

If `careloop` remote already exists but URL is wrong:

```bash
git remote set-url careloop https://github.com/jahua/CareLoop.git
```

## Option B: Separate clone of CareLoop

1. Clone CareLoop in a separate directory:
   ```bash
   git clone https://github.com/jahua/CareLoop.git CareLoop-repo
   cd CareLoop-repo
   ```
2. Copy contents from `thesis project/CareLoop/` into `CareLoop-repo/` (overwrite).
3. Commit and push:
   ```bash
   git add -A
   git commit -m "Sync from thesis project"
   git push origin main
   ```

## If push says "Could not read from remote repository"

- **Access:** You must have **push** access to `github.com/jahua/CareLoop` (same GitHub user `jahua` or a collaborator).
- **Auth:** If you use 2FA, use a **Personal Access Token** instead of password when Git asks for credentials, or use SSH:  
  `git remote set-url careloop git@github.com:jahua/CareLoop.git`  
  then `git push careloop main` (or subtree command above).
