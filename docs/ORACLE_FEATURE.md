# Oracle Feature

The Oracle is an optional front-end helper for drafting CSV content.

## What it does

- accepts a prompt
- sends it to Anthropic from the browser
- returns draft text to review and paste into the CSV manually

## What it does not do

- write to the CSV automatically
- override the one-declaration rule
- become a required browsing dependency

## Current implementation truth

- API key stays in the browser and is sent directly to Anthropic
- session storage is the default; optional “remember” uses `localStorage` under `PI_ORACLE_KEY`
- “Forget key” clears both browser stores
- the default model is `claude-sonnet-5`
- output is plain draft text, not an auto-applied mutation
- output follows the register's exact editorial headings and identifies evidence still needed
- the rest of the site must continue to work without a configured key
