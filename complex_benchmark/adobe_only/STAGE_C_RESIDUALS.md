# Stage C residuals (fix during full-spec writing)

The reconciled ledger (`PORTFOLIO_LEDGER_v2.json`, verify verdict MINOR) is solid: 30/15/35/20,
all 5 Photo signature ops represented (none >~10), duplicate clusters collapsed. Five small items to
resolve when full specs are written:

1. **AO-17 mis-absorption** — AO-17 (Ostra dark-mode menu) is correctly owned by PHOTO-09 but is also
   listed in LAYOUT-01 (Kantyna) `absorbs`. Remove it from LAYOUT-01.
2. **Orphaned AO-06** (firearms-optics Shopify product cleanup) — not absorbed anywhere. Home it in a
   Photo white-bg product-isolation engagement (candidate: PHOTO-12 Kilnmore marketplace, or a product row).
3. **Orphaned AO-11** (sterling ruby pendant product photo + listing) — home it in a jewelry Photo row
   (candidate: PHOTO-13 enclosed-aperture jewelry isolation, or PHOTO-08).
4. **Brand collision "Anvil & Oak"** — LAYOUT-16 (strength-studio launch) vs locked MOTION-15 (Anvil & Oak
   movement library). Either make them one client's two engagements (add a cross-family note) or rename one.
5. **Brand collision "Apexguard"** — PHOTO-25 (performance parts/detailing) vs LAYOUT-17 (auto film);
   AO-90 double-absorbed. Reconcile as one client's two engagements or rename + split the AO-90 absorb.
6. **Text bug** — LAYOUT-13 `element_reuse` cites "a single Marisol photo engagement (in the Photo slice)"
   which no longer exists (Marisol is Layout-only now). Fix the wording.

Double-absorption of an AO-id across a Photo engagement and a Layout engagement is ACCEPTABLE where the
same client's assets legitimately feed both (e.g. a photo cohesion job + a data-sheet job); only flag it
when unreconciled.
