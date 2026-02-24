# Todo List for Optimized Diamond 30 Packaging

## Phase 1: Identify Exclusions
- [ ] Identify all large zip files (`*.zip`).
- [ ] Identify all temporary files (`zi*`).
- [ ] Identify `node_modules`, `.env`, `__pycache__`, `.pytest_cache`.

## Phase 2: Create Optimized Archive
- [ ] Create `Global_System_v26_Diamond_30_Full_Optimized.zip` including ALL project directories (`roles`, `infrastructure`, `knowledge`, `memory-bank`, etc.).
- [ ] Exclude all identified large and temporary files.
- [ ] Ensure no critical project files are excluded.

## Phase 3: Verification
- [ ] Verify that `roles`, `infrastructure`, `knowledge`, `memory-bank` are PRESENT in the zip.
- [ ] Verify that large zip files and temp files are ABSENT.
- [ ] Check final archive size (should be much smaller than 700MB).

## Phase 4: Delivery
- [ ] Deliver the optimized zip file to the user.
