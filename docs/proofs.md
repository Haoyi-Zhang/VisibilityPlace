# Proof record

This document states the mathematical arguments implemented by the artifact. It is conventional mathematical text, not a proof-assistant development.

## Lemma 1: failures become a counting threshold

For a fixed realization with observed set `O`, a selected set `S` retains an observer after every failure set `F subseteq S` with `|F|<=f` if and only if `|S intersect O|>=f+1`.

If the intersection has at most `f` elements, fail exactly those selected observed components. Conversely, deleting at most `f` elements from a set of at least `f+1` leaves one. Applying the statement to every realization proves the robust obligation.

## Lemma 2: compiler path correspondence

Every physical realization determines a unique compiled path: enter the corresponding initial state; traverse its serialized export-monitor chain; choose the ordinary compiled transition matching each physical edge and state update; and exit through the first target state. Conversely, every compiled source--sink path alternates between complete state gadgets and legal transition edges, so projecting the transition origins yields a legal physical realization. The constructions are inverse, and the monitor edges traversed in an unrestricted state are exactly the observed components.

No target-outgoing transition is compiled, which enforces first arrival. Because the physical graph is acyclic, projection also proves that the compiled graph is acyclic.

## Theorem 1: exact reduction to two-terminal k-hurdle

Let `k=f+1`, and let `e_m` be the unique compiled edge for component `m`. A placement `S` is robustly visibility-complete exactly when every compiled source--sink path contains at least `k` edges from `{e_m : m in S}`.

This follows immediately from Lemmas 1 and 2. The optimization objective is preserved because each component and its unique edge have the same positive cost. The resulting combinatorial optimization is the established two-terminal k-hurdle problem; the hurdle algorithm itself is not claimed as new.

## Theorem 2: status trichotomy

Exactly one case applies.

1. If no compiled source--sink path exists, the safety-only universal obligation is vacuous.
2. Otherwise, assign length one to every monitor edge and zero to ordinary edges. If a shortest source--sink path has length less than `k`, selecting all components still leaves this path below the threshold, so the model is infeasible. The path is a certificate.
3. If the all-monitor shortest length is at least `k`, selecting all components is feasible, and the positive-cost finite problem has an optimum.

The checker recomputes the relevant reachability or validates the path locally.

## Lemma 3: compact LP and threshold integrality

For each component edge, use `0<=x_m<=1`; use a potential `d_v` with `d_s=0`, `0<=d_v<=k`, and `d_t>=k`. Require

* `d_v-d_u<=x_m` on monitor edge `m`, and
* `d_v-d_u<=0` on every ordinary edge.

Along any source--sink path these inequalities telescope to `sum x_m>=k`, so the LP is a relaxation of the integer placement problem. Conversely, shortest `x`-distance from the source is a feasible potential whenever every path has length at least `k`.

Let `d_v` be shortest distance capped at `k`. Choose `alpha` in `(0,1)` and select every monitor edge whose interval `(d_u,d_v]` crosses one of `alpha,1+alpha,...,k-1+alpha`. Ordinary edges cannot increase `d`. On every source--sink path, the first crossing of each threshold is therefore a selected monitor edge; because `x_m<=1`, one edge cannot account for two thresholds. The placement is feasible.

For uniformly random `alpha`, the probability that edge `m` is selected is `d_v-d_u` when positive, at most `x_m`. Hence expected cost is at most the LP value. Since every integral feasible cost is at least the LP value, some threshold placement has exactly optimum cost. Enumerating intervals between fractional breakpoints deterministically finds one. This is the standard two-terminal k-hurdle rounding argument.

## Theorem 3: local optimality certificate

Let `S` be the supplied placement. Its submitted potential `h^S` proves primal feasibility. Separately, suppose the certificate contains:

* a nonnegative integer source--sink flow `y` of value `F`; and
* nonnegative overflow values `z_m` satisfying `y_m-z_m<=c_m`.

To prove a lower bound, fix any feasible placement `X`, not necessarily `S`. By the coverage-potential construction, `X` has its own integer potential `h^X`, with `h^X_s=0`, `h^X_t=k`, and the local inequalities for the indicator `X_m`. Then

```
sum_m c_m X_m
 >= sum_m (y_m-z_m) X_m
 >= sum_e y_e (h^X_v-h^X_u) - sum_m z_m
 = kF - sum_m z_m.
```

The first inequality uses `y_m-z_m<=c_m` and `X_m` in `{0,1}`. For a monitor edge, `h^X_v-h^X_u<=X_m`; for an ordinary edge, `h^X_v-h^X_u<=0`; all flow values are nonnegative. Flow conservation telescopes the edge sum to `F(h^X_t-h^X_s)=kF`. Thus the dual value is a lower bound for **every** feasible placement. If it equals the exact cost of the supplied placement `S`, and `h^S` passes the separate primal check, then `S` is optimal.

The distinction between `h^S` and `h^X` is essential: the checker receives only `h^S`, while the proof uses existence of a canonical potential for each hypothetical feasible competitor. The checker verifies exact integer equalities and inequalities and does not need the producer's LP values, threshold, or min-cost-circulation objective.

## Lemma 4: existence of an integer dual witness

The standard dual is the k-maximum-flow formulation. Build a min-cost circulation by giving monitor edge `m` a zero-cost base capacity `c_m` and an overflow branch of unit cost, giving ordinary edges sufficiently large zero-cost capacity, and adding a sink-to-source return edge of cost `-k`. A circulation carrying flow value `F` has cost `sum z_m-kF`; minimizing it maximizes the lower bound in Theorem 3. Integral capacities imply an integral optimum.

A capacity of `C+1`, where `C=sum c_m`, is sufficient for unrestricted branches and the return edge. Remove the return edge and decompose an integral circulation into `F` integral source--sink path units plus directed cycles; zero-cost cycles can be discarded. Across all monitor base branches there are only `C` units of capacity. If `F>C`, some path unit uses no base monitor branch. In a feasible hurdle instance every source--sink path contains at least `k` monitor edges, so that unit uses at least `k` overflow branches. Removing the path unit together with one unit on the return edge removes overflow cost at least `k` and return reward exactly `k`; the circulation objective cannot increase. Repeating gives an optimum with `F<=C`. Therefore no unrestricted branch needs more than `C` units and a uniform capacity `C+1` is nonbinding. Strong LP duality and hurdle integrality yield an integer witness matching the primal optimum.

## Proposition 1: state-unique occurrence is essential

If one monitor component may label several compiled edges, the `k=1` placement problem contains minimum label `s-t` cut: choose a minimum-cardinality set of labels whose edges meet every source--sink path (unit costs suffice for the reduction). Zhang and Fu prove NP-hardness under two **separate** restrictions: maximum path length two, and maximum label frequency two. Their length-two bounded-frequency refinement uses frequency three; they do not prove hardness with both bounds equal to two, and they give a polynomial algorithm for a disjoint-path/frequency-two subcase. Thus unique compiled occurrence is a substantive general tractability boundary, but no simultaneous `(length 2, frequency 2)` hardness claim is made.

## Proposition 2: physical treewidth alone is insufficient for joint obligations

In the broader declared-obligation model, take a physical star with an unmonitorable center and one monitorable leaf for each vertex of an arbitrary graph `H`. For each edge `{u,v}` of `H`, declare the unique leaf--center--leaf path as an obligation. With one required observation and unit costs, a placement covers all obligations exactly when the corresponding vertices form a vertex cover of `H`. The physical topology has treewidth one and every obligation has length two. Therefore any claim based only on physical topology width fails when arbitrary obligation incidence is allowed.

This proposition does not contradict the single-obligation state-unique theorem: it identifies a different interface whose demand incidence carries the hard graph.

## Checker trust boundary

A successful check establishes that the supplied bounded JSON model has the declared status and, in the optimal case, that the placement cost meets a mathematically valid lower bound. It does not establish that the model accurately represents a deployed routing system. Producer and checker compilers share the strict parser and graph container, but transition construction is separately written. Tiny direct semantics and brute-force optimization provide a third implementation on 44 retained cases. A separate fixed-seed campaign differentially checks 200 additional small models, including eight targeted semantic edge cases. These are finite checks, not a general proof.

## Proposition 3: exponentially many realizations can retain a linear certificate

For every `q >= 1`, form a chain of `q` binary diamonds. Each branch vertex hosts its own unit-cost export component, and all transitions preserve the unrestricted state. The graph has `3q+1` physical vertices, `4q` physical edges, and `2q` components. A realization independently chooses one branch in every diamond, yielding `2^q` paths with pairwise distinct observed sets. The compiler remains linear by the size formulas. At `k=1`, selecting both branch components in any fixed layer has cost two and hits every path; no one-component placement can do so because its opposite branch avoids it. The emitted graph potential and flow certificate have linear representation. This is an illustration of the retained certificate language, not a lower bound for all possible certificate systems.

## Lemma 5: flow/overflow is the path-LP dual

The path relaxation has one constraint `sum_{m in P} x_m >= k` for every source--sink path and bounds `0 <= x_m <= 1`. Its dual places weight `w_P >= 0` on paths and overflow variable `z_m >= 0` on each upper bound:

```
maximize k * sum_P w_P - sum_m z_m
subject to sum_{P containing m} w_P - z_m <= c_m.
```

Aggregating `y_e = sum_{P containing e} w_P` gives a nonnegative source--sink flow of value `F=sum_P w_P`, with monitor conditions `y_m-z_m<=c_m`. Conversely, every nonnegative flow in the compiled DAG decomposes into path flows. Thus the path and flow forms have equal optimum. Strong LP duality, threshold integrality, and integral min-cost circulation imply existence of an integer lower-bound witness equal to an optimal integral placement.

## Proposition 4: certificate size and checking complexity

For compiled graph `(W,A)`, an optimal certificate stores `|W|` potentials, at most `|A|` positive flow entries, at most `|M|` positive overflow entries, and a selected list. It has `O(|W|+|A|+|M|)` entries. With producer return flow at most `C=sum c_m`, numeric values require logarithmic bits in `C+k` beyond identifiers. The checker reconstructs the graph and scans edges, sparse flow, balances, and monitor capacities once, so verification is linear in graph plus certificate representation. This does not bound LP or circulation production time.

## Proposition 5: semantic monotonicity under realization-family inclusion

For two models over the same components, costs, and hurdle, let `O(I)` be the family of observed-component sets. If `O(I1) subseteq O(I2)`, then every placement feasible for `I2` is feasible for `I1`; the feasible-set inclusion reverses, and `OPT(I1) <= OPT(I2)` whenever both optima exist. If `I1` is infeasible, a set of size below `k` in `O(I1)` also belongs to `O(I2)`, so `I2` is infeasible. This is semantic only: a changed compiled graph requires a fresh certificate because edge identifiers, potentials, and flows are model-specific.

## Reproduction claim boundary

A clean replay compares every retained certificate object and all non-timing semantic case fields. Timing and floating-point diagnostics are not trusted equality fields. Matching replay establishes regeneration and checker acceptance of the same finite proof objects in the tested environment; it is not bit-level solver reproducibility, a mechanized proof, or evidence about deployed routing.
