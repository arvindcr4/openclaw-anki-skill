# OpenClaw Anki Skill

Push flashcards directly to [Anki](https://apps.ankiweb.net/) via [AnkiConnect](https://foosoft.net/projects/anki-connect/) over [Tailscale](https://tailscale.com/). Designed as an [OpenClaw](https://openclaw.ai/) skill so AI agents can create and push flashcards on demand.

## Setup

### On your Mac (Anki host)

1. Install [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on (code `2055492159`)
2. In Anki: **Tools → Add-ons → AnkiConnect → Config**, set:
   ```json
   "webBindAddress": "0.0.0.0"
   ```
3. Restart Anki

### On your VPS / server

1. Ensure Tailscale is connected to the same tailnet as your Mac
2. Update `ANKICONNECT_URL` in `anki_push.py` to your Mac's Tailscale IP
3. Copy the skill to your OpenClaw skills directory:
   ```bash
   cp -r . ~/.openclaw/workspace/skills/anki/
   ```

## Usage

```bash
# Check connectivity
python3 anki_push.py health

# Add a single card
python3 anki_push.py add "Deck::Name" "Question?" "Answer." "tag1,tag2"

# Add multiple cards (JSON)
python3 anki_push.py batch "Deck::Name" '[{"front":"Q1","back":"A1","tags":"t1"},{"front":"Q2","back":"A2","tags":"t2"}]'

# Import from pipe-delimited file (Question | Answer | Tags)
python3 anki_push.py import "Deck::Name" cards.txt

# List decks
python3 anki_push.py decks

# Deck statistics
python3 anki_push.py stats "Deck::Name"

# Trigger AnkiWeb sync
python3 anki_push.py sync
```

## OpenClaw Integration

Place `_meta.json`, `SKILL.md`, and `anki_push.py` in `~/.openclaw/workspace/skills/anki/`. OpenClaw agents will automatically discover the skill and can push cards via tool calls.

## License

MIT
