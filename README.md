# OpenFilter Experiment: License Plate OCR Pipeline

This repository is dedicated to experimenting with the OpenFilter framework to build, test, and evolve an OCR pipeline for license plate recognition.

## Purpose

The main goal of this experiment is to explore the capabilities and limitations of OpenFilter when applied to real-world scenarios involving license plate detection and recognition.

## Experiment Phases

### Phase 1: Baseline Pipeline
- Reorganize project structure and simplify codebase
- Remove outdated comments and unused files
- Standardize pipeline entrypoint to `script.py`
- Recreate a minimal OCR pipeline using `VideoIn`, `OCRFilter`, and `Webvis`
- Ensure test coverage and CI setup (via GitHub Actions)

### Phase 2: Error Analysis
- Identify limitations in current detection.
- Log incorrect or noisy OCR outputs.
- Investigate frame regions where OCR failed.

### Phase 3: Hypothesis
- The OCR pipeline fails without prior plate segmentation.
- Hypothesize that a preprocessing filter could isolate regions of interest and improve results.

### Phase 4: Experimental Improvement
- (Optional) Introduce or simulate preprocessing filter for plate detection.
- Compare OCR results with and without preprocessing.
- Evaluate output quality, frame accuracy, and noise reduction.

### Phase 5: Documentation & Reflection
- Summarize findings, code decisions, and error handling.
- Reflect on the hypothesis and what could be productized or researched further.

