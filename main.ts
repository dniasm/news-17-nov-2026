// Entry for make.fun's "Sum up 17 November's world news in one image" bounty (Node 22, standard library only).
// The image is entry.png beside this file, rendered from art/front.html by tools/render.py; this program copies
// it byte for byte to /output/entry.png, so every run writes the same bytes.
//
// Locally, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true }); // a no-op on the grader's existing /output
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
