---
description: "Blind mode: while the Tephra agent is killed, frozen or flooded, the kernel refuses the attacker moves that usually come next."
title: Blind mode
weight: 2
---

The first thing an attacker who reaches a node does is blind the sensor: kill it, freeze it, or flood it
until it falls behind. Blind mode makes the kernel refuse the moves that usually come next for as long as
the sensor is blind. It is **on by default**.

## When the sensor counts as blind

- The agent's **heartbeat** is older than `stale_after` (12 s by default). The agent writes it once a second
  from its main loop, so an agent that runs but no longer handles events stops it too.
- At once, when the agent is sent **SIGKILL or a stop signal** (SIGSTOP, SIGTSTP, SIGTTIN, SIGTTOU) by any
  process but itself, or when its **last thread exits**.

The next agent's first heartbeat ends it. A stop by Kubernetes (a rollout, an upgrade, an uninstall)
switches blind mode off before the agent exits, so planned stops refuse nothing.

## What is refused

In every pod on the node, labelled or not, except pods in `enforcement.protectNamespaces` (`kube-system`
by default). The node's own processes and the container runtime are never refused.

| Action | Why it is on the list |
|---|---|
| Reading `/etc/shadow` | Credential access |
| Writing `/etc/ld.so.preload` | Hijacking every program on the system |
| Writing any `authorized_keys` | SSH persistence |
| Writing `release_agent` or `/proc/sys/kernel/core_pattern` | Container escape |
| Running a deleted or in-memory binary | Fileless payloads |
| `ptrace` attach | Injecting into other processes |
| Loading a kernel module | Rootkits |
| `mount` | Escaping the container's filesystem |

Each refusal is written to a ring buffer reserved for attacks on the agent, and raises **R038** (critical)
when an agent is back. A pod that repeats one refusal in a loop is reported once a second and counted in
between, so it cannot fill that buffer.

## Configuration

```yaml
agent:
  blind:
    mode: "on"        # on, dry_run (report, refuse nothing) or off
    staleAfter: 12s
```

`dry_run` is the way to check a cluster first: R038 then reports what would have been refused. Blind mode
needs BPF LSM and `agent.tamper.keepRecording` (on by default).

## The way out

If no agent can run on a node, blind mode stays in force there. From a shell on the node, with the
`tephrad` binary:

```sh
tephrad enforce off
```

turns enforcement and blind mode off through the pinned maps until the next agent starts.
