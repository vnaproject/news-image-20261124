// news-image-20261124 — "The World Today", a one-page front page summing up
// Tuesday 24 November 2026. The image is drawn at build time by render.py
// (system fonts + original vector shapes only) and shipped here as entry.png.
// This program just copies it to the output directory, deterministically,
// with no network access. Node 22, standard library only.
//
// Local test:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
