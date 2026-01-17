# Deployment Instructions - Fixing API Key Exposure

## Current Situation
- Your Gemini API key was exposed in the JavaScript bundle
- This repo contains only build artifacts (deployed files)
- Source code is on your desktop

## Steps to Fix (Do these on your DESKTOP in your source code folder)

### Step 1: Find Your Source Code Folder
Navigate to your Platonic App source code on your desktop (wherever you run `npm run dev` or `npm run build`)

---

### Step 2: Create Environment File

Create a file called `.env` in the root of your source folder (next to `package.json`):

```
VITE_GEMINI_API_KEY=paste_your_new_api_key_here
```

**Important:** Replace `paste_your_new_api_key_here` with your actual new restricted API key from Google Cloud Console.

---

### Step 3: Update Your Source Code

Find the file where you make the Gemini API call. Look for this pattern:

```javascript
// FIND THIS (around line 100-200 in your main component file):
const apiKey = "AIzaSyBD5KZoZPLhpLvpuVoDB9PbNuexd0qSI0o";
```

**Replace it with:**

```javascript
// NEW CODE:
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
```

**There are TWO places** in your code where the API key is used. You need to replace BOTH:

1. In the main Oracle consultation function
2. In the "Challenge the Verdict" function

Search your source files for `AIzaSyBD5KZoZPLhpLvpuVoDB9PbNuexd0qSI0o` and replace all instances.

---

### Step 4: Create/Update .gitignore

Create or update `.gitignore` in your source folder:

```
# Environment variables - NEVER commit these!
.env
.env.local
.env*.local

# Dependencies
node_modules/

# Build output
dist/

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

---

### Step 5: Test Locally

In your source folder:

```bash
npm run dev
```

Visit `http://localhost:5173` (or whatever port Vite uses) and test the Oracle feature to make sure it works.

---

### Step 6: Build

```bash
npm run build
```

This creates a `dist` folder with your updated build files.

---

### Step 7: Deploy to GitHub Pages

Copy the contents of your `dist` folder to this repository:

**On Mac/Linux:**
```bash
# From your source folder
cp -r dist/* /path/to/my-platonic-app/

# Go to this repo
cd /path/to/my-platonic-app/

# Add and commit
git add .
git commit -m "Fix: Replace hardcoded API key with environment variable"
git push origin claude/review-changes-mkiwksje7p2c29a3-8kpwK
```

**On Windows (PowerShell):**
```powershell
# From your source folder
Copy-Item -Recurse -Force dist\* C:\path\to\my-platonic-app\

# Go to this repo
cd C:\path\to\my-platonic-app\

# Add and commit
git add .
git commit -m "Fix: Replace hardcoded API key with environment variable"
git push origin claude/review-changes-mkiwksje7p2c29a3-8kpwK
```

---

## Verification Checklist

- [ ] Old API key revoked in Google Cloud Console
- [ ] New API key created with HTTP referrer restrictions (`https://laurent1056.github.io/*`)
- [ ] New API key restricted to only Generative Language API
- [ ] `.env` file created in source folder (NOT in this repo)
- [ ] `.env` added to `.gitignore` in source folder
- [ ] Source code updated to use `import.meta.env.VITE_GEMINI_API_KEY`
- [ ] Tested locally with `npm run dev`
- [ ] Built with `npm run build`
- [ ] Deployed dist folder to this repo
- [ ] Tested on live site at https://laurent1056.github.io/my-platonic-app/

---

## Security Note

Even with environment variables, the API key will still be visible in the browser because GitHub Pages is static hosting. The protection comes from:

1. **HTTP referrer restrictions** - Key only works from your domain
2. **API restrictions** - Key only works with Gemini API
3. **Not committing `.env`** - Key not in source control history

For even better security, consider migrating to Vercel/Netlify with serverless functions in the future.
