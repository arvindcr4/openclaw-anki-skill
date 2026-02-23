---
name: anki
description: Push flashcards directly to Anki on Arvind's Mac via AnkiConnect over Tailscale.
---

# Anki Card Pusher

Push flashcards to the Anki desktop app running on the Mac (100.108.20.44) via AnkiConnect API over Tailscale.

## Prerequisites
- Anki desktop must be running on the Mac
- AnkiConnect add-on installed (code 2055492159)
- AnkiConnect config: `"webBindAddress": "0.0.0.0"` (to accept Tailscale connections)
- Tailscale active on both VPS and Mac

## Usage

### Check connectivity
`exec python3 ~/.openclaw/workspace/skills/anki/anki_push.py health`

### Add a single card
`exec python3 ~/.openclaw/workspace/skills/anki/anki_push.py add "AI::ML" "What is gradient descent?" "An optimization algorithm that iteratively adjusts parameters by moving in the direction of steepest descent of the loss function." "ML,optimization"`

### Add multiple cards at once
`exec python3 ~/.openclaw/workspace/skills/anki/anki_push.py batch "AI::ML" '[{"front":"Q1","back":"A1","tags":"tag1"},{"front":"Q2","back":"A2","tags":"tag2"}]'`

### Import from a pipe-delimited file
`exec python3 ~/.openclaw/workspace/skills/anki/anki_push.py import "AI::Books" "~/.openclaw/workspace-kimi/ai_books_anki.txt"`

### List all decks
`exec python3 ~/.openclaw/workspace/skills/anki/anki_push.py decks`

### Get deck stats
`exec python3 ~/.openclaw/workspace/skills/anki/anki_push.py stats "AI::ML"`

### Trigger AnkiWeb sync
`exec python3 ~/.openclaw/workspace/skills/anki/anki_push.py sync`

## When to use
- User asks to create flashcards from a topic, book, or conversation
- User asks to push existing card files to Anki
- User asks to check Anki status or sync
- After generating study material, automatically push it to Anki
