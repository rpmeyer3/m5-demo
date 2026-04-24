# FreshKeep - Milestone 5 Hi-Fi Prototype

**Group 11: Beer Buddies**
Ryan Meyer, Kristian Pitshugin, Matt Harpur, Daniel Fairchild
CSCI 4800 Human Computer Interaction - Spring 2026 - University of Georgia

## What it is

FreshKeep is a mobile app concept that eliminates invisible food waste. Users
scan grocery receipts, and computer vision + ML automatically build a digital
pantry inventory with personalized expiration estimates, reminders, and recipe
suggestions.

This repository contains the high-fidelity interactive prototype built for
Milestone 5, revised from the low-fi prototype based on Milestone 4 pilot
usability testing.

## How to run the prototype

The prototype is a single-page HTML/CSS/JS mobile-app mockup. No build step,
no package install.

### Option 1: Open the file directly
Double-click `index.html` in a file browser. It will open in your default web
browser.

### Option 2: Serve locally (recommended)
From the repo root, run any static server. For example:

```bash
python -m http.server 8000
```

Then open http://localhost:8000 in a mobile-width viewport (or use the browser
devtools device toolbar, iPhone 13/14 size recommended).

### Option 3: Deploy to Vercel
The included `vercel.json` configures serving `index.html` as the default route.
Run `vercel` from the repo root, or connect the repo to a Vercel project.

## Target platform

iPhone / Android mobile phone (375 x 812 px baseline, iPhone 13/14 size). The
prototype frame is fixed at that size and centered on a desktop viewport for
demonstration.

## Implemented task flows

1. **Task 1 (Simple) - Check an item's expiration status.**
   Home -> Inventory tab -> tap item row -> Item Detail screen with best-by
   date, storage, days remaining, and AI freshness assessment.

2. **Task 2 (Moderate) - Scan a receipt and review imported items.**
   Home -> Scan Receipt card -> camera viewfinder -> Capture -> review 6
   detected items (edit with pencil, remove with X) -> Confirm -> success
   screen -> View Inventory.

3. **Task 3 (Complex) - Connect a grocery store account and configure
   notifications.**
   Settings tab -> Link My Grocery Accounts section -> Connect on Kroger ->
   sign-in modal -> Authorize -> store row updates to Connected -> scroll to
   Notification Preferences to toggle reminders.

## Changes from the lo-fi prototype (Milestone 4)

Applied per the Milestone 4 Report Design Recommendations:

1. Scan Receipt shortcut added directly to the Inventory screen (not just Home).
2. Settings section renamed from "Connected Stores" to "Link My Grocery Accounts".
3. First-run onboarding coachmark points new users at the Scan Receipt card.
4. Notification Preferences moved above Connected Stores and highlighted with a
   priority banner.

Additional hi-fi improvements:

- Live search + functional (mutually-exclusive) filter pills on Inventory.
- Per-item edit and remove on the Scan Results screen.
- Manual "+" add-item FAB with a form modal.
- Tappable Home recipe card opens a full Recipe Detail screen.
- Quick Sync now routes to a QR code scanning screen.
- All icons replaced with Lucide icons for a consistent visual system.

## Limitations

- Wizard of Oz prototype only: camera capture, OCR, store auth, and QR pairing
  are simulated.
- Inventory data is hard-coded to nine items.
- The Stats screen is informational only (no interactive drill-down).
- Household Members management is a link target only.

## Files

- `index.html` - Hi-Fi prototype (Milestone 5 deliverable).
- `vercel.json` - Static deployment config.
- `lo-fi-wireframe/index.html` - Milestone 4 low-fi prototype, kept for reference
  and visual comparison.

## External dependencies

- Lucide icons loaded from `unpkg.com/lucide@latest` via CDN (no local install).

## Contact

- rpm04447@uga.edu
- kp39596@uga.edu
- mah08371@uga.edu
- dbf65068@uga.edu
