# CareLoop Repository

**Canonical Repository:** https://github.com/jahua/CareLoop

## About

CareLoop is a standalone Git repository. All CareLoop code lives here and should be pushed directly to `github.com/jahua/CareLoop`.

## Git Operations

### Check remote
```bash
cd CareLoop
git remote -v
# Should show: origin https://github.com/jahua/CareLoop.git
```

### Push changes
```bash
cd CareLoop
git add -A
git commit -m "your commit message"
git push origin main
```

### Clone (fresh setup)
```bash
git clone https://github.com/jahua/CareLoop.git
cd CareLoop
```

## Troubleshooting

### "Could not read from remote repository"
- Ensure you have push access to `github.com/jahua/CareLoop`
- If using 2FA, use a Personal Access Token instead of password
- For SSH: `git remote set-url origin git@github.com:jahua/CareLoop.git`
