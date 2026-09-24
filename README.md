# visibility-complete-monitor

This standalone repository implements and checks proof-carrying minimum-cost monitor placements for one explicitly bounded class of owned synthetic export-policy graphs. It accompanies an internal research manuscript; it is not a BGP implementation or deployment recommendation.

## Scope

An input is a finite directed acyclic physical graph with one source--target obligation, a persistent restriction bit, edge actions `keep`, `restrict`, or `either`, boundary edges disabled while restricted, and positive-cost `export` monitor components. A component observes a realization only at its unrestricted vertex state. Tolerating `failures = f` arbitrary selected-component losses is equivalent to requiring at least `k = f + 1` selected observations on every realization.

The policy semantics compiles to a state-unique two-terminal `k`-hurdle graph. Production returns exactly one certificate status:

* `optimal`: selected components, an exact integer coverage potential, and an integer flow/overflow lower bound equal to the placement cost;
* `infeasible`: a realizable source--sink path containing fewer than `k` monitor components even when all are selected; or
* `vacuous`: a checker-recomputed declaration that no policy realization reaches the target.

The checker reconstructs the compiled graph using separately written transition logic and validates exact integers. Its acceptance path uses only the Python standard library, does not import SciPy or NetworkX, and does not trust the producer's LP, rounding, or circulation trace. JSON booleans are not accepted as integers; unknown identifiers, negative values, extra fields, noncanonical ordering, and sparse objects longer than their reconstructed universes are rejected.

The artifact contains no AS numbers, prefixes, announcements, devices, private data, live services, attack routes, or evasion workflow. A certificate is conditional on the supplied finite model and does not establish model completeness for a deployed network.

## Requirements

* Python 3 for checking, tests, bounded exhaustive validation, differential validation, comparison, and audit.
* SciPy and NetworkX only for certificate production and the two diagnostic baselines (`requirements-producer.txt`).

The campaign launcher uses one worker, a 3 GiB address-space cap, and a 2700-second CPU cap.

## Clean reproduction

Run from the repository root; each named output directory must be absent or empty:

```bash
python3 test.py
python3 exhaustive.py --out replay-exhaustive
python3 fuzz.py --out replay-fuzz
python3 run.py pilot --out replay-pilot
python3 run.py reproduce --out replay
python3 run.py compare --observed replay
python3 analyze.py --results replay --out replay-derived
python3 audit.py --campaign replay --derived replay-derived \
  --fuzz replay-fuzz --exhaustive replay-exhaustive
python3 -S run.py check \
  --model inputs/example-model.json \
  --certificate inputs/example-certificate.json
```

`compare` requires equality of all 120 certificate objects, every non-timing semantic case field, the aggregate summary, and all 20 control outcomes. `audit` rechecks retained and replayed certificates, compares the deterministic derived tree, compares all 13,720 bounded-exhaustive rows and all 200 fixed-seed differential cases, and validates the claim, external-resource, and 58-entry reference-audit ledgers. Producer/checker milliseconds, wall/CPU time, and peak RSS are descriptive and intentionally excluded from deterministic equality.

## Retained evidence

* 120-model deterministic campaign: 96 optimal, 12 infeasible, and 12 vacuous certificates.
* 44 campaign cases with direct-semantics / compiled-path / brute-force oracle agreement.
* 20 malformed or out-of-class controls, all rejected.
* 20 contract tests, including a complete three-vertex universe check, strict type and sparse-bound checks, and a checker-only `python3 -S` subprocess.
* A complete 13,720-model three-vertex universe: all forward-edge absence/policy choices, one-or-zero monitors per vertex, both initial restriction states, and every legal failure budget; compiler, path semantics, and brute-force classification agree on every case.
* 200 fixed-seed differential small models: 192 generated and 8 targeted; compiler, path semantics, brute-force optimum/status, and certificate acceptance agree on every case.

These finite checks are implementation evidence. They are not a proof of the general theorem, a representative Internet sample, or a portable performance claim.

## Repository map

* `run.py`: pilot, full production, checking, comparison, and command routing.
* `exhaustive.py`, `src/exhaustive_cases.py`: complete declared three-vertex universe.
* `fuzz.py`, `src/fuzz_cases.py`: fixed-seed generated and targeted differential cases.
* `audit.py`: standard-library artifact/result/reference audit.
* `test.py`, `tests/`: contract and exact-oracle tests.
* `src/model.py`: strict bounded model parser and DAG/horizon checks.
* `src/producer_compile.py`: producer-side policy compiler.
* `src/checker_compile.py`: separately written checker-side compiler.
* `src/solver.py`: attributed hurdle LP/threshold construction, integer dual extraction, and baselines.
* `src/checker.py`: exact certificate checker.
* `src/oracle.py`: direct physical-semantics path enumerator and brute-force placement oracle.
* `src/controls.py`: malformed-certificate and out-of-class controls.
* `inputs/suite.json`: all 120 retained models.
* `results/campaign/`: certificates, primary rows, controls, summary, and resource observations.
* `results/exhaustive/`: retained 13,720-case bounded-complete rows and summary.
* `results/fuzz/`: retained 200-case differential rows and summary.
* `results/derived/`: deterministic manuscript tables and plot inputs.
* `results/pilot/`: repaired discriminating pilot.
* `docs/reference-audit.csv`: canonical source record for each of the 58 cited works.
* `claim_evidence_ledger.csv`: claim-to-proof/check/result map.
* `external_resources.csv`: external scholarly, standards, dependency, and workflow records; no external executable or paper bytes are bundled.

## License

See `LICENSE`. Publisher template files and scholarly papers are not part of this standalone repository.
