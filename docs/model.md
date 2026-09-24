# Frozen model and certificate interface

## 1. Input object

A model is a JSON object with exactly these fields:

| Field | Meaning | Bound |
|---|---|---|
| `case`, `family` | neutral alphanumeric identifiers | at most 32 characters |
| `nodes` | physical vertices numbered `0..nodes-1` | 1--500 |
| `edges` | `[u,v,boundary,action]` | at most 2,000; no parallel pair |
| `monitors` | `[vertex,"export",positive_cost]` | at most 32 |
| `obligation` | `[source,target,initial_restriction]` | distinct endpoints; bit in `{0,1}` |
| `horizon` | declared upper bound on physical DAG path length | 0--16 |
| `failures` | number of arbitrary selected-component losses tolerated | 0--number of monitors |

The physical graph must be acyclic, and its longest path must not exceed `horizon`. Costs are positive JSON integers; booleans are rejected even though Python treats them as integer subclasses. The certified class rejects local hooks, repeated physical edges, cycles, undeclared fields, and noncanonical identifiers.

## 2. Policy transition semantics

A route state is `(v,r)`, where `v` is a physical vertex and `r` is a persistent restriction bit.

* A boundary edge is disabled when `r=1`.
* `keep` preserves `r`.
* `restrict` sets `r=1`.
* `either` permits both `0` and `1` from an unrestricted state, and only `1` from a restricted state.
* An export monitor at vertex `v` observes exactly when the state is `(v,0)`.
* A realization stops at its first arrival at the declared target.

The one-bit transition system is an owned abstraction. It is not a complete implementation of BGP decision processes, communities, route selection, convergence, or inter-AS economics.

## 3. Robust visibility obligation

Let `M(P)` be the set of monitor components observed on realization `P`, and let `S` be the selected placement. For a component-failure budget `f`, the safety-only obligation is

```
for every realization P and every F subset of S with |F| <= f:
    (S \ F) intersects M(P).
```

This is equivalent to `|S intersect M(P)| >= f+1` for every realization. The checker reports an empty realization family as `vacuous`; it never merges that status with an ordinary nonempty optimum.

## 4. Policy-to-hurdle compiler

For each physical state `(v,r)`, the compiler creates an entry and exit vertex. At `(v,0)`, all export components hosted at `v` are serialized as distinct monitor edges; at `(v,1)`, the state has only an ordinary bypass. Ordinary transition edges implement the policy relation. A super-source enters the initial state, and each target state exits to a super-sink. Transitions leaving the physical target are suppressed.

Each monitor component labels exactly one compiled edge. For `n` physical vertices, `a` physical edges, and `m` components, the compiled graph has

* exactly `4n + m + 2` vertices, and
* at most `2n + m + 3a + 3` edges.

A physical topological order induces a compiled topological order. There is a bijection between policy realizations and compiled source--sink paths, preserving the observed component set.

## 5. Certificate schemas

All certificates include `schema`, `case`, `status`, and `k=failures+1`. Extra fields are rejected. Every declared integer must have exact JSON-integer type rather than boolean type. Sparse lists must be no longer than the reconstructed vertex, edge, or monitor universe; entries must have known identifiers and canonical order.

### Optimal

An optimal certificate contains:

* sorted unique selected component identifiers and their exact cost;
* an integer potential `h` in `[0,k]` on every compiled vertex, with `h(source)=0` and `h(target)=k`;
* nonnegative integer source--sink flow entries `y` and their value `F`;
* nonnegative integer overflow entries `z_m` for monitor edges; and
* the equality `cost = kF - sum(z_m)`.

For every ordinary edge `(u,v)`, the checker requires `h(v)-h(u) <= 0`. For monitor edge `m`, it requires `h(v)-h(u) <= 1` when selected and `<=0` otherwise. The flow must conserve exactly. The dual capacity condition is `y_m-z_m <= c_m`. Flow and overflow values are nonnegative exact integers. Unknown edge identifiers, negative overflow, duplicate entries, and sparse vectors larger than the corresponding reconstructed universe are rejected before arithmetic checks.

### Infeasible

The certificate gives a contiguous source--sink path and its exact monitor-edge count. Its length cannot exceed the reconstructed DAG vertex count. If the count is less than `k`, then even selecting every component cannot satisfy the obligation.

### Vacuous

The certificate carries zero cost. The checker independently reconstructs the graph and recomputes that the sink is unreachable.

## 6. Excluded models

The exact certificate theorem does not cover:

* one physical component represented by multiple compiled edges;
* multiple independent source--target obligations optimized jointly;
* cyclic route-state semantics or unbounded convergence;
* monitor-site common-cause failures;
* probabilistic availability, traffic volume, or detection latency;
* live routing data or completeness of a discovered topology.

Repeated component labels already contain general minimum label `s-t` cut at `k=1`; known hardness holds under separate short-path and low-frequency restrictions, not the unsupported simultaneous `(2,2)` restriction. Joint obligations lead to hurdle multicut/covering structure. These exclusions are complexity boundaries, not parser conveniences.
