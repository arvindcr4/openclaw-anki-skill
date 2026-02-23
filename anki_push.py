#!/usr/bin/env python3
"""OpenClaw skill: Push flashcards to Anki via AnkiConnect over Tailscale."""

import json
import sys
import urllib.request
import urllib.error

ANKICONNECT_URL = "http://100.108.20.44:8765"


def anki_request(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    req = urllib.request.Request(
        ANKICONNECT_URL,
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"AnkiConnect unreachable at {ANKICONNECT_URL}: {e}"}))
        sys.exit(1)
    if result.get("error"):
        print(json.dumps({"error": result["error"]}))
        sys.exit(1)
    return result.get("result")


def add_card(deck, front, back, tags=""):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    # Ensure deck exists
    anki_request("createDeck", deck=deck)
    result = anki_request(
        "addNote",
        note={
            "deckName": deck,
            "modelName": "Basic",
            "fields": {"Front": front, "Back": back},
            "tags": tag_list,
            "options": {"allowDuplicate": False},
        },
    )
    print(json.dumps({"ok": True, "noteId": result, "deck": deck}))


def add_batch(deck, cards_json):
    """cards_json: JSON array of {"front": "...", "back": "...", "tags": "..."}"""
    cards = json.loads(cards_json)
    anki_request("createDeck", deck=deck)
    notes = []
    for c in cards:
        tag_list = [t.strip() for t in c.get("tags", "").split(",") if t.strip()]
        notes.append({
            "deckName": deck,
            "modelName": "Basic",
            "fields": {"Front": c["front"], "Back": c["back"]},
            "tags": tag_list,
            "options": {"allowDuplicate": False},
        })
    results = anki_request("addNotes", notes=notes)
    added = sum(1 for r in results if r is not None)
    dupes = sum(1 for r in results if r is None)
    print(json.dumps({"ok": True, "added": added, "duplicates": dupes, "deck": deck}))


def list_decks():
    result = anki_request("deckNames")
    print(json.dumps({"decks": result}))


def deck_stats(deck):
    result = anki_request("getDeckStats", decks=[deck])
    print(json.dumps(result))


def sync():
    anki_request("sync")
    print(json.dumps({"ok": True, "synced": True}))


def health():
    ver = anki_request("version")
    print(json.dumps({"ok": True, "ankiconnect_version": ver, "url": ANKICONNECT_URL}))


def import_file(deck, filepath):
    """Import pipe-delimited cards from a text file (Question | Answer | Tags)."""
    with open(filepath) as f:
        lines = f.readlines()
    cards = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 2:
            cards.append({
                "front": parts[0],
                "back": parts[1],
                "tags": parts[2] if len(parts) > 2 else "",
            })
    if not cards:
        print(json.dumps({"error": "No valid cards found in file"}))
        sys.exit(1)
    add_batch(deck, json.dumps(cards))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: anki_push.py <command> [args...]")
        print("Commands: health, add, batch, import, decks, stats, sync")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "health":
        health()
    elif cmd == "add":
        if len(sys.argv) < 5:
            print("Usage: anki_push.py add <deck> <front> <back> [tags]")
            sys.exit(1)
        add_card(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")
    elif cmd == "batch":
        if len(sys.argv) < 4:
            print("Usage: anki_push.py batch <deck> '<json_array>'")
            sys.exit(1)
        add_batch(sys.argv[2], sys.argv[3])
    elif cmd == "import":
        if len(sys.argv) < 4:
            print("Usage: anki_push.py import <deck> <filepath>")
            sys.exit(1)
        import_file(sys.argv[2], sys.argv[3])
    elif cmd == "decks":
        list_decks()
    elif cmd == "stats":
        if len(sys.argv) < 3:
            print("Usage: anki_push.py stats <deck>")
            sys.exit(1)
        deck_stats(sys.argv[2])
    elif cmd == "sync":
        sync()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
