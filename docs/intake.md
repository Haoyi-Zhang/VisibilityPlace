# Scientific intake and resource record

The project was executed on 2026-09-15 in the supplied Web Pro Linux environment. Intake was performed once before the retained campaign and did not include stress tests.

## Measured execution envelope

* CPU affinity exposed logical processors 0--4; the cgroup quota was `400000/100000`, i.e., four aggregate CPU cores.
* The cgroup memory ceiling was 4,294,967,296 bytes. Memory in use at intake was approximately 338 MB.
* The host reported approximately 6.24 GB physical memory and no host swap. The project nevertheless treated the 4 GiB cgroup ceiling as authoritative.
* The writable overlay exposed approximately 33.77 GB total and 32.02 GB available.
* Platform: Linux x86-64.

The artifact applies a stricter single-process 3 GiB virtual-address-space limit and a 2700-second CPU limit before model processing. It uses one worker. No GPU, external compute, external model API, private data, live routing system, or device is used.

## Pilot and campaign observations

The repaired seven-case pilot exercised all three certificate statuses, the largest retained physical graph, and all 20 malformed or out-of-class controls. It recorded 1.23 wall seconds, 1.25 campaign CPU seconds, and 331,924 KiB peak process RSS.

The 120-case campaign recorded 7.51 wall seconds, 7.51 campaign CPU seconds, and 410,016 KiB peak process RSS. These values describe this environment only. The correctness argument does not use timing or memory measurements.

## Closure

The maximum retained physical model has 500 vertices, 1,428 edges, 31 monitor components, and horizon 14. The largest compiled graph has 2,033 vertices and 4,017 edges. All measurements are below the project ceilings. One quarter of the campaign budget was reserved for clean replay, repair, and packaging; the actual campaign used far less than the available CPU budget.
