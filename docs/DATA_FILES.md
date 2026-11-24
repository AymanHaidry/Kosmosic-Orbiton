# Data Files & Storage

Stag stores its user profile locally in the home directory.

## Current storage

| Path | Purpose | Can delete? |
|---|---|---|
| `~/.stag/profile.json` | Locally saved user facts and preferences | Yes — Stag will no longer remember them |
| OS temporary directory | Short-lived TTS playback files | Yes — removed automatically |

The profile directory is created on first save. Stag does not ship or load a bundled facts database, custom `intel_*.json` files, or a local Wikipedia dump.

## Legacy migration

If `~/.neuro_link_memory.json` exists and the new profile does not, Stag copies the old file to `~/.stag/profile.json` on first launch. The original file is left untouched as a backup.

The old `~/.neuro_link_intel/` custom-facts directory and `~/.neuro_link_wiki_cache/` cache are no longer read. They are not deleted automatically; remove them manually if you no longer need them.

## Privacy

The profile stays on the device. General knowledge requests contact Wikipedia over the internet; voice recognition and neural text-to-speech also use their configured online providers. Do not store passwords, payment details, or other sensitive secrets in the profile.
