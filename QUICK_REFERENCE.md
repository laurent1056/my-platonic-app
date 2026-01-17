# Quick Reference - What Changed

## In Your Source Code (Desktop)

### File 1: `.env` (NEW FILE - create this)
```
VITE_GEMINI_API_KEY=your_new_api_key_here
```

### File 2: Your Main Component File (EDIT THIS)

**FIND (appears twice in your code):**
```javascript
const apiKey = "AIzaSyBD5KZoZPLhpLvpuVoDB9PbNuexd0qSI0o";
```

**REPLACE WITH:**
```javascript
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
```

### File 3: `.gitignore` (create or update)
```
.env
.env.local
.env*.local
node_modules/
dist/
.DS_Store
```

---

## Google Cloud Console Settings

When you create your new API key:

### Application Restrictions
- Type: **HTTP referrers**
- Allowed referrers:
  - `https://laurent1056.github.io/*`
  - `http://localhost:*`

### API Restrictions
- Type: **Restrict key**
- APIs: **Generative Language API** only

---

## Common Issues

**"Error: import.meta.env.VITE_GEMINI_API_KEY is undefined"**
- Make sure `.env` file is in the root of your source folder
- Restart your dev server (`npm run dev`)
- Make sure the key starts with `VITE_`

**"403 Forbidden" error on live site**
- Make sure you added `https://laurent1056.github.io/*` to HTTP referrers
- Wait a few minutes for Google's changes to propagate

**Git won't let me push**
- Make sure you're on the correct branch: `claude/review-changes-mkiwksje7p2c29a3-8kpwK`
- Run: `git checkout claude/review-changes-mkiwksje7p2c29a3-8kpwK`
