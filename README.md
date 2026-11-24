# The World Today — Tuesday, 24 November 2026

A one-page newspaper front page summing up the world's news of
Tuesday 24 November 2026, drawn programmatically (`render.py`, Python/PIL):
every letter is rendered from a system font and every picture is original
vector art built from shapes. No photographs, no copied artwork, no
image-generator output. `main.ts` (Node 22, stdlib only) copies the rendered
`entry.png` to `/output/entry.png` deterministically, with no network.

## The stories

**Lead — TECH: NVIDIA BRINGS BACK HUANG AFTER TRUMP INTERVENTION**
Nvidia's board unanimously reinstates Jensen Huang as chief executive,
11 days after he quit over revelations of affairs — including one with a
woman US officials suspect of spying for China. President Trump says he
pressed the board personally and sent Vice-President JD Vance as his
emissary. Shares soar by a third; the Nasdaq jumps 6.5%.
Sources: Reuters, BBC, CNN, WSJ (24 Nov).

**THE GULF — Iran steps up Gulf strikes, sues for $290bn**
Tehran hits US bases and civilian sites in the Gulf after a lull, as a US
naval blockade and sanctions squeeze the country. Iran calls the blockade
"military aggression".
Sources: Al Jazeera, France 24, Spyglass (24 Nov).

**KOREA — Russian jets enter Seoul's defence zone**
Multiple Russian warplanes enter South Korea's air defence zone without
notice; Seoul issues an emergency alert for Ulleung Island. Moscow also
warns Finland and Estonia.
Sources: Yonhap, The Straits Times (24 Nov).

**LIBYA — Ukraine says it sank a Russian warship**
Kyiv claims seven sea drones sank the corvette Merkury off Benghazi and
hit a cargo ship. Russia vows a response.
Sources: France 24, Al Jazeera, BBC (24 Nov).

**EUROPE — EU targets Russian sport in 22nd package**
The European Commission proposes banning Russian teams from EU events and
curbing crypto channels. In Spain, final polls put the right on course to
oust Sánchez on 29 November.
Sources: Al Jazeera, Bloomberg (24 Nov).

**ALSO TODAY**
- Business: CrowdStrike agrees to buy Zscaler in a $44bn deal.
- Law/AI: Virginia and Oregon sue SpaceX over Grok AI sexual imagery.
- Health: England launches the largest AI breast-screening trial, for
  700,000 women.

## Design

Masthead "THE WORLD TODAY" with the dateline "TUESDAY, 24 NOVEMBER 2026"
front and centre, so the judge can tell at a glance which day the page sums
up. The Nvidia comeback leads — the day's most consequential story — with
a vector illustration of an AI chip under a rising market arrow. Four more
stories fill a two-by-two grid, each with its own small vector icon (tanker,
jet, warship, ballot box), and a bottom strip carries three short briefs
from three more fields, so the page spans tech, war, diplomacy, business,
law and health across the US, the Gulf, Korea, Libya and Europe.

## Verification

- `python3 render.py` twice: byte-identical `entry.png` (same sha256).
- `entry.png`: 1024x1024 PNG, under 1 MiB.
- `main.ts` copies it to `/output/entry.png`; run twice, same bytes.
- Kit check: `node ../news-image-20261124-kit/cli/makefun.mjs check` —
  5 passed (competition_open, snapshot, license_osi MIT, entrypoint node22,
  repo_created_after_open drand round 34227943), 1 failed
  (transcripts_present — the coordinator bundles the session transcripts
  after the build session ends), 15 skipped, 3 checked at submission.
