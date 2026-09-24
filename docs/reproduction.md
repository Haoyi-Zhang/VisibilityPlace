# Reproduction and repair record

## Resource guard and retained campaign

The campaign uses one Python process and one worker under a 3 GiB address-space limit and a 2700-second CPU limit. It uses no GPU, model API, external compute, live network, device, private input, or attack traffic.

The deterministic suite contains 120 owned synthetic models: 36 Tiny, 48 Layered, 12 Fan, 12 Infeasible, and 12 Vacuous. Maximum declared dimensions are 500 physical vertices, 2,000 permitted physical edges (1,428 observed), 32 permitted monitor components (31 observed), and horizon 16 (14 observed). Retained outcomes are 96 optimal, 12 infeasible, and 12 vacuous. The maximum compiled graph has 2,033 vertices and 4,017 edges; the largest certificate is 16,711 bytes.

Direct physical semantics, independently compiled paths, and brute-force placement agree on 44 retained cases. All 120 certificates are accepted. All 20 malformed or out-of-class controls are rejected. Twenty contract tests pass.

The retained campaign measured about 7.51 CPU seconds, 7.51 wall seconds, and 410,016 KiB peak process RSS in its recorded environment. These values are descriptive only; exact proof objects, not speed, support correctness claims.

## Complete bounded three-vertex universe

`exhaustive.py` enumerates every model in a declared finite universe rather than sampling it. Vertices are fixed as `0,1,2`, with source `0` and target `2`. Each of the three forward edge slots is absent or has one of six boundary/action combinations; each vertex has zero or one export monitor with fixed positive cost; the initial restriction bit takes both values; and the failure budget ranges from zero through the monitor count. The universe therefore has

```text
7^3 * 2 * sum_{M subseteq {0,1,2}} (|M|+1) = 13,720
```

models. Every model validates; producer and checker compilers agree edge-for-edge; direct physical observations equal compiled-path observations; and complete subset enumeration returns a status and optimum. The retained distribution is 1,640 optimal, 8,500 infeasible, and 3,580 vacuous. This is a complete check only for the stated three-vertex universe, not for all bounded inputs or the general theorem.

## Fixed-seed differential campaign

`fuzz.py` runs 192 generated small DAGs and eight targeted semantic edge cases under seed `20260918`. The targeted cases cover zero monitors, initial restriction with boundary suppression, source and target monitors, co-located components, `either` actions, first target arrival, restriction suppression, and high failure budgets. For every one of the 200 cases it requires:

1. edge-for-edge equality of producer and checker compiled graphs;
2. equality of direct physical realizations and compiled path observations;
3. equality of brute-force status/cost and producer output; and
4. acceptance of the emitted certificate by the independent checker.

The retained run has 25 optimal, 104 infeasible, and 71 vacuous cases and reaches 16 realizations in one model. Runtime fields are retained as observations but excluded from replay equality. This campaign is auxiliary implementation evidence, not a general proof or workload sample.

## Clean commands

Every output directory named below must be absent or empty:

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
python3 -S run.py check --model inputs/example-model.json \
                        --certificate inputs/example-certificate.json
```

`compare` excludes `producer_ms` and `checker_ms` but requires equality of all other case fields, the summary, all 20 control rows, and every certificate object. The analyzer omits timings from deterministic manuscript data. `audit` rechecks every certificate; compares retained and replayed semantic objects, derived files, bounded-exhaustive rows, and differential rows; verifies required claim-ledger fields and source URLs; and requires exactly 58 unique cited rows in `docs/reference-audit.csv`.

The final `python3 -S` command disables site packages. Its success demonstrates that the documented checker acceptance path does not need the producer's SciPy or NetworkX dependencies. It does not show that every future Python implementation or platform is supported.

## Repairs retained in the record

1. **Pilot subset.** The first seven-case pilot solved its scientific cases but its summary function referenced four control identifiers omitted from the subset. The repaired subset includes `T000`, `T001`, `I000`, `V000`, `L012`, `L037`, and `F007`, exercises all statuses and maximum scale, and rejects all controls. The 120-case campaign was unaffected.
2. **Deterministic derived data.** A legacy `scaling.csv` mixed deterministic graph/certificate fields with run-local timings. The analyzer now excludes timings from manuscript data. No model, certificate, status, cost, baseline result, or plotted certificate-size point changed.
3. **Checker dependency path.** `run.py` formerly imported the producer module before dispatch, contradicting the documented standard-library checker route. Producer imports are now lazy, and the checker command is tested under `python3 -S`.
4. **Strict JSON integers and sparse bounds.** Python booleans could previously compare equal to `0` or `1` in a few certificate fields. The checker now requires exact integer types and rejects negative overflow, unknown edge identifiers, and sparse/path lists longer than the reconstructed graph permits.
5. **Label-cut boundary citation.** An earlier manuscript sentence incorrectly conjoined two restrictions proved separately in Zhang and Fu: maximum source--sink path length two, and maximum label frequency two. The paper, proof notes, source ledger, and related-work matrix now state the separate results and note that their length-two/frequency-three refinement is not a length-two/frequency-two hardness theorem.

The first four are implementation/workflow repairs; the fifth is a scientific-claim correction. None changes the frozen positive theorem or retained numerical results.

## Interpretation

A successful replay regenerates the same finite certificate objects and deterministic analysis data and validates them in the tested environment. It is not bit-level identity of third-party solver internals, proof-assistant verification, independent peer review, evidence about deployed routing, or a guarantee against all software defects.
