# Deployment

Platonic Ideal deploys as a static Vite app to GitHub Pages.

## Current deployment assumptions

- repository: `my-platonic-app`
- public URL: `https://laurent1056.github.io/my-platonic-app/`
- deploy command: `npm run deploy`

## Data deployment

- `public/platonic_ideal.csv` is bundled into the deployed site
- no backend fetch layer is involved

## Base URL behavior

The app uses `import.meta.env.BASE_URL` and the current Pages subpath.

## Post-deploy checks

- site loads at the project URL
- category count matches the CSV
- one `DECLARED`, one `EMPTY`, and one `CANDIDATE` row render correctly
- page title updates on category navigation
- canonical root URL and meta description exist in the served HTML

