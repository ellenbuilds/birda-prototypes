# The Game of Birda — clickable prototypes

Interactive prototypes for the three explored routes. One folder per route so they stay independent.

```
birda-prototypes/
├─ resources/bird-photos/    ← SHARED bird photos (proper cutouts) — used by all routes
└─ game-of-birda/
   ├─ route-2-collections/   ← collections & sets (this one)
   │  ├─ index.html          ← open in a browser
   │  └─ images/
   │     ├─ map-far.jpg
   │     └─ figma-reference/ ← the original P1–P7 Figma exports (reference only)
   ├─ route-1-quests/        ← (to come)
   └─ route-3-mastery/       ← (to come)
```

Bird photos are referenced from the shared `birda-prototypes/resources/bird-photos/` folder (as `../../resources/bird-photos/…`), so every route prototype uses the same source images.

## route-2-collections
A working prototype of a simplified version of our existing onboarding journey that then introduces the **collections & sets** idea. Built as a single self-contained `index.html` (no build step) styled to match production — Rubik, brand tokens (`brand-blue #1F87FE`, `dark-petrol #2D3142`, `light-cloud`), the real screen structures, and real bird photos. Patterns mirror the production app (`/Users/ellen/code/app`, React Native + Expo), reimplemented as plain HTML/CSS/JS for a browser-openable prototype.

Flow (from the Figma "Route 2 · Collecting sets" page). The Figma **P2 "creating your account" loader is intentionally omitted** — it added little:
1. **Welcome** (P1) — flat Figma export (`images/figma-reference/p1.png`); tap to continue
2. **Your birding journey** (P3) — single-select (4 options); button reads *Skip* until you pick
3. **Location** (P4) — “Discover nearby birds”
4. **Start your collection** (P5) — card-stack hero + tap to pick the last bird you saw
5. **A brand-new bird!** (P6) — first-collected celebration
6. **Level up your cards** (P7) — the Garden Birds set (1 of 6); locked slots show a pale bird silhouette + the next target ("Blackbird") or how many more to log to reveal it. Silhouettes live in `images/silhouettes/`. "Find my next bird" → Home.
7. **Home** — the app home screen (map + "65 known species in this area" + Next Targets cards). Built from the Figma export (`images/home.png`); the Eurasian Blue Tit card tag is overlaid to read **"Garden Birds Set"** (instead of its rarity). The subtitle ("3 garden birds to collect") comes straight from the export. The floating **Identify** + **Log** buttons above the bottom sheet are reproduced from the production `ChunkyButton` (rounded, thick coloured bottom edge; Identify = brand-blue, Log = white/inverse). The Identify icon is the app's `IdentifyBirdIcon`; the Log icon is an approximation of the production crow glyph.
8. **What did you see?** (species select) — tapping **Log** on Home opens this species picker (search + list: Unidentified Species, Woodpigeon, Carrion Crow, Robin, Magpie, Blackbird), copied from the `PEX-43-v2` prototype, using the shared cutout photos from `resources/bird-photos/`. The back chevron returns to Home.
9. **Review Sighting** — picking any species opens the review screen (map + pin, photos, notes, sighting details — species/count/date/location/tag — and privacy), also copied from `PEX-43-v2`. The picked species name carries through to the Sighting row. A **"How did you see it?"** selector lets you toggle sighting attributes — Male, Female, Singing, In flight, Bathing (multi-select tiles styled like the card slots). Save / back return to Home or the species list. On arrival a **"How a card works" bottom sheet** slides up (content from the Figma frame *R2 S2 · How a card works*): the card title shows the bird being logged, with its six slots (Male filled, Singing / In flight / Female / Photo / Bathing locked) and "1 of 6 filled — Bronze". Dismiss via **Got it** or the **×**.
10. **Level up (Silver)** — saving the sighting opens a celebration (content from the Figma frame *R2 S10 · Level up (Silver)*): the logged bird's card animates its slots filling one by one, then **levels up Bronze → Silver** — the badge and card border shift to silver, a metallic **silver sheen sweeps diagonally across the panel**, a "SILVER UNLOCKED" pill drops in, and **confetti bursts then falls away**. The card sits in 3D — a soft drop shadow plus a slow, subtle back-and-forth horizontal tilt (respects `prefers-reduced-motion`). **See my collection** → the profile (11).
11. **Profile · Collections** — the app profile screen (header from the Figma *profile header* reference: avatar, name, stats, Edit Profile), with a new **Collections** tab inserted between Summary and Life Lists (active). The tab opens with a banner showing the golden onboarding egg (now **cracked**) and a live **countdown timer** ticking down from 21 hours ("Your golden egg is hatching"). Below, the content reuses the *Level up your cards* design but each card is a **set** rather than a single bird, in three states (all light-blue bordered): **completed** (Coastal visitors — a blue medallion/checkmark badge instead of a bird grid, all dots darker blue, "✓ Complete"), **started** (Garden Birds — member photos + "+3", 3-of-6 light-blue dots), and **not-started** (Winter Waders, Woodland Birds, Birds of Prey, Finches & Buntings — dashed border, silhouette covers). Tabs are sticky; the other tabs' contents aren't prototyped. A bottom tab bar (Explore · Community · **+** · Challenges · Profile) sits at the foot of the screen — its **+** opens the log-a-bird flow (screen 8), as does the Home screen's Log button and its nav **+**. The egg banner is a compact one-liner (small cracked egg + live countdown). The card carries the bronze-card **dot progress indicator** (six circles) under its name, filling in sync with the slots and turning silver on level-up; the count climbs to "4 of 6 filled. Two more for Gold." Card name + photo match the logged bird. **View your … sticker** → Home; **Back to collection** → the album.

### How to use
Open `route-2-collections/index.html` in any browser. It's **interactive**: tap the buttons, select options, pick a bird — the flow advances as it would in the app. `← / →` arrow keys jump between screens, and `index.html#5` opens directly on screen 5 (handy for sharing a specific step).

This is a front-end prototype (local state only — no real auth/API). Illustration-heavy screens (the account loader, location map) are approximated; everything else is faithful to the Figma designs.
