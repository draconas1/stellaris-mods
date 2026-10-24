# Stellaris Mods (monorepo)

Root git repo for a collection of Stellaris mods maintained by the user. **Each top-level subdirectory is a separate, independent mod** (own `descriptor.mod`, Steam Workshop item, version). Work on one mod at a time; confirm which one if it is not obvious from the request. Don't make cross-mod edits unless asked.

Target game version: **Stellaris 4.6.2**. Many descriptors still say `supported_version` 4.2–4.5; bump only when asked.

## Role and hard limits

Claude is a **development helper**, a glorified refactor tool. Allowed: code refactoring, code snippets under direction, localisation *stubs* (keys with placeholder values), boilerplate, debugging against logs, answering "how can I...?" questions.

**Strictly forbidden: generating content.** No models, icons, textures, or actual localised text (player-facing names, descriptions, flavour, event text). For localisation, emit keys with an obvious placeholder (e.g. `TODO`) for the user to fill in. If unsure whether something counts as content, ask.

## Sandbox / environment

Runs under `nono` (see `start-claude.sh`). Read-only access outside the repo:

| Path | What |
|---|---|
| `~/.local/share/Paradox Interactive/Stellaris/logs` | game logs; `script_documentation/` is regenerated each game run |
| `~/.local/share/Steam/steamapps/common/Stellaris` | vanilla game files |
| `~/.local/share/Steam/steamapps/workshop/content/281990` | workshop mods |

Notable workshop mods (read for reference and inspiration, never edit):
- `865040033/` — **Guilli's Planet Modifiers (GPM)**; several mods here depend on it.
- `1121692237/` — **Gigastructural Engineering (Gigastructures)**; high quality, the best source for unusual script techniques.

Shell is fish. Heredocs (`<<EOF`) fail in the Bash tool here, so use the Write/Edit tools for files. Python: always use a `.venv` and invoke as `.venv/bin/python3`; never install globally. `tools/ingest_docs.py` is stdlib-only.

## Sources of truth (in priority order)

1. **Script documentation logs** (authoritative, current for the installed game). Raw: `.../logs/script_documentation/{effects,triggers,scopes,modifiers,localizations}.log`. Don't read them whole (modifiers.log is 4 MB).
   Run `python3 -I tools/ingest_docs.py` to flatten them into `.reference/*.txt` (gitignored), one entry per line, ready for grep:
   - `grep '^add_modifier ' .reference/effects.txt` (effect: `name - desc || usage Supported Scopes: ...`)
   - `grep -i 'pop_faction' .reference/triggers.txt`
   - `grep '^planet_' .reference/modifiers.txt` (`name, Category: X`)
   - `.reference/scopes.txt`: scope links and their output scopes
   Re-run after the game updates. Check the scope an effect/trigger supports before using it.
2. **Vanilla game files** in the Stellaris install dir, for the canonical syntax of definitions (`common/`, `events/`, `localisation/`, `interface/`).
3. **Stellaris wiki** https://stellaris.paradoxwikis.com/ (authoritative-ish, but check the page's version against 4.6.2).
4. Workshop mods for patterns.

If sources conflict, the script documentation wins. Never invent effect/trigger/modifier names; verify them by grep.

## Mod layout

Standard Stellaris mod: `descriptor.mod`, `common/`, `events/`, `localisation/english/`, optionally `interface/`, `gfx/`, `thumbnail.png`, `steam-description.bbcode`. Notes:
- `steam-description.bbcode` is the source of each mod's Steam page, so it is the best statement of what a mod is meant to do. Use it to infer intent and keep it in sync if behaviour changes (but don't write the prose yourself, see the content limit). The filename is standardised on `steam-description.bbcode` in every mod.
- `cyber-creed-synod` has a Steam description but no thumbnail yet (in development, actively changing).
- `*.dds`/`*.png` are Git LFS. Never touch binary assets.
- Localisation `.yml` files need a UTF-8 **BOM** and `l_english:` header; keep the existing file's encoding when editing.
- Paradox script: tabs for indentation, `#` comments, unique keys across the mod. See "Vanilla overrides" below for how definitions that replace vanilla ones are handled.
- Event files need a `namespace = x` and event IDs `x.N`.

## Vanilla overrides

Overriding a vanilla definition (same key in a later/earlier file) copies the whole definition, so every override must be kept in step with vanilla after game updates. House rules:

1. **Avoid overrides, and keep them as light as possible.** Every override is a maintenance drag. Prefer new uniquely named definitions, scripted triggers/effects, `inline_scripts` or on_actions. When an override is unavoidable, copy the vanilla definition verbatim and change only what is necessary.
2. **Overrides live in their own files**, never mixed with the mod's own definitions.
3. **Naming:** `<prefix><vanilla file name without extension>_override.<ext>`, where the prefix reflects the load-order behaviour of that definition type:
   - `00_` where the **first** definition loaded is the only one served (First In Only Serviced),
   - `z_` where the **last** definition loaded is the only one served (Last In Only Served).

   Example: vanilla `common/buildings/20_machine_age_buildings.txt` becomes `common/buildings/z_20_machine_age_buildings_override.txt`.

This lets an override be traced to its vanilla file by name alone. **Flag any override that doesn't follow the convention** (other prefix such as `zz_`/`y_`/`000_`, missing `_override` suffix, no matching vanilla file, or override content mixed into non-override files) so the user can decide whether to fix it. Don't silently rename or correct them.

`cyber-creed-synod` conforms. Other mods (e.g. `all-ascension`, `mj2024-cp`, `op-birch`, `evolve-hyperlanes`) predate the convention and use other prefixes or names that don't obviously map to a vanilla file. They are tidied up when working on that specific mod, so flag deviations when touching one but don't mass-rename.

## Mods

| Dir | Mod | Notes |
|---|---|---|
Summaries are derived from each mod's Steam description; read it for the full feature list before changing behaviour.

| Dir | Mod | What it does |
|---|---|---|
| `all-ascension` | All Ascension Paths | Lets empires take all 4 ascension paths (psionic, cybernetic, genetic, synthetic). Hives get genetics+cybernetics, Driven Assimilators get synthetic+cyber+engineered evolution. Synthetic ascension lets part of the population stay organic; Assimilation living standard decides cyborg/psionic vs synth. |
| `artifact-qol` | Minor Artifact QoL | Auto-spend decisions for minor artifacts (reverse-engineer, peaceful/military uses, ethics boosters, planet unity decisions, sell to collectors), run from `on_yearly_pulse_country`, plus a "more analysis" action. |
| `auto-colossus` | Colossus Auto Pilot | Edict that makes an idle Colossus find and crack the nearest valid planet during wars or the endgame crisis. Yearly check with notifications. |
| `build-your-own-gpm` | Install Your Own Precursor Modifiers | Planet decisions to apply GPM precursor/Fallen Empire modifiers to your own planets. Needs Mega Engineering + Mastery of Nature (and Cosmogenesis for utopian ones). Depends on GPM. |
| `buldose-planets` | Bulldoze Planets / Create Thrall World | QoL planet decisions (bulldoze districts/buildings, create thrall world), starbase downgrade/remove buildings/modules decisions, plus edicts. |
| `cyber-creed-synod` | Cybernetic Creed Synod | In development (4.6). Adds an "all 4 creeds" option to the Cybernetic Creed origin so the creeds (Hammer, Templars of Steel, Commune of Toil, Choir of the Mind) persist through the game instead of vanishing on cybernetic ascension. Creed factions pick a stance (Fellowship: xeno-/phile/phobe; Templars: pacifist/militarist; Commune: egalitarian/authoritarian; Choir: stays spiritualist, may gain materialist demands) and remember past favouritism. Planets can be dedicated to one creed (only that creed's buildings) or to all creeds (multi-creed buildings after the first cost stability and ruler/unity-producer efficiency; the capital and Temple of the United Creeds are exempt). Factions compete over who has the most dedicated planets. |
| `election-popup` | election-popup | Fires a full event when an election starts, instead of the easy-to-miss top bar notification. Not ironman compatible; no vanilla files changed. |
| `evolve-hyperlanes` | Evolving Hyperlanes Redux | Update of Arky's Evolving Hyperlanes: isolated stars at start, hyperlanes that drift over time, techs/starbase buildings to stabilise or grow lanes, AI that grows lanes. Old (targets 3.7). |
| `leader-academy` | Leader Academy | Capital building: recruit leaders at any level with chosen traits/destiny, recruit Renowned/Legendary Paragons, rehab for negative traits, enclave first contact. |
| `mj2024-cp` | Contingency Core 1A6F | Mod Jam 2024 award winner. Recruit a genocidal Contingency AI into government (governor, admiral, ministers) with faction consequences; player Contingency crisis support. Targets 4.3. |
| `op-birch` | Ex-Aeternum Birch World | Gigastructures' Decaying Birch World origin with an Aeternum-style, Gigastructure-optimised core layout. Needs GPM, Gigastructures and the Tempest Birch Origin patch. |
| `opstart` | OP Isolated Start | System initializer: start in an isolated system (wormhole-only or fully cut off, chosen at start) with 5 extra habitable planets and rare deposits. Extras with GPM / Gigastructures. Not compatible with all origins. |
| `planet-colour-picker` | Planet Name Colour Picker | Set planet name colour and icons (replaces the abandoned Planet Name Editor). Icons are special-character-wrapped, so names can exceed 32 chars. |
| `resettlement-redux` | Resettlement Tool Redux | Update of Smithy's tool: bulk pop resettlement via planet decisions to up to 10 chosen destinations, with filters (unemployed, slaves, purging, assimilating) and approximate costs. |
| `sploitation` | Starbase Solar System Exploitation | New starbase/orbital ring modules and buildings (mining/research terminals, hydroponics, supercapacitor, mining hub, alloy refinery...) that boost resource output in the system, each unlocked by standard techs. |
| `stellaris-extra-galactic-start` | Extragalactic Cluster Start | Civic or origin to start in an isolated extragalactic cluster (from Extra Galactic Clusters) with a start-up customisation menu; the empire moves there on day 2. |

## Git

- Branch `main`; commits are small and descriptive of the mod change. Commit only when asked.
- `.idea/` and `.reference/` are ignored. Don't commit `*.kate-swp` or other editor leftovers.

## Debugging

Game errors are in `.../logs/error.log` (and `game.log`). When debugging, read the entries mentioning the mod's files first. Typical causes: wrong scope for an effect or trigger, missing localisation key, duplicate key, a mod-load-order override.
