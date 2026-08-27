# Security and Privacy

## Current model

- static site on GitHub Pages
- no user accounts
- no server-side persistence

## Oracle caveat

- Oracle uses a user-supplied Anthropic API key sent directly from the browser to Anthropic
- the key uses session storage by default; persistent device storage is explicit opt-in
- the key is not committed to the repo
- Oracle output should be treated as draft text, not trusted fact
- browser-direct keys are appropriate only for the private authoring surface, not a public multi-user workflow

## Privacy posture

- no analytics integration is part of the current tracked product
- no cookies are required for browsing the catalog
