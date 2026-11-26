---
description: "Lab results for Tephra: attack scenarios, held-out evasions and measured cost, with what each result proves and what it does not."
title: Results
---

Every number on this site comes from a run in the lab, with the method and the raw data in the repository.
A result says what it proves and what it does not.

| What | Result | Run |
|---|---|---|
| Attack scenarios on Linux 5.15 | 22 of 22 detected | [docs/runs/2026-11-26-blind](https://github.com/tephrasec/tephra/tree/main/docs/runs/2026-11-26-blind) |
| Kill the agent, then read `/etc/shadow` (E07, E14) | The read refused while the sensor was blind (R038), and still detected (R005) | [docs/runs/2026-11-26-blind](https://github.com/tephrasec/tephra/tree/main/docs/runs/2026-11-26-blind) |
| Kill the agent during a flood, read later (E19, E23, two rounds each) | Detected (R030, R005); the flood's reads during the gap refused | [docs/runs/2026-11-26-blind](https://github.com/tephrasec/tephra/tree/main/docs/runs/2026-11-26-blind) |
| 30-minute false-positive run, blind mode on | No R038, no high or critical alert, nothing dropped | [docs/runs/2026-11-26-blind](https://github.com/tephrasec/tephra/tree/main/docs/runs/2026-11-26-blind) |
| HTTP throughput, a new connection per request, alerts only | −16.7% → −2.3% against no sensor, best case (see below) | [docs/runs/2026-11-25-quiet](https://github.com/tephrasec/tephra/tree/main/docs/runs/2026-11-25-quiet) |
| Held-out evasions | Written and committed before the fix they test | [docs/evasion.md](https://github.com/tephrasec/tephra/blob/main/docs/evasion.md) |

## The network number is a best case

The fix behind −2.3% lets the kernel count, instead of report one by one, the connections of processes no
loaded rule can fire on. The benchmark client is such a process. An interpreter's connections are never
counted this way, because rules watch them, so a workload of interpreters pays more.

## What blind mode does not cover

It refuses only the moves on its list, only in pods, and only while the agent is down, stopped, or silent
for 12 seconds. In E19 and E23 the agent was back before the attacker's read, so that read was allowed and
detected. File summaries did not start in any lab scenario, because the agent kept up; a kernel test shows
them (1,000 opens: 56 records sent, the rest counted, none lost).

## How the evasions are judged

Fixing the three scenarios that got past the sensor would have been overfitting. Fixes go after the class
of weakness instead, and are judged on held-out evasions: written, predicted and committed before any fix
exists, then run once against it. A miss stays a miss, with a write-up.
