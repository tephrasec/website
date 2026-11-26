---
title: Enforcement
weight: 3
---

Rules with `action: block` can refuse what they detect, in the kernel, before it happens: running a file
with no name on disk, writing to `/etc/ld.so.preload`, `release_agent` or `core_pattern`, ptrace attach,
kernel module loads, and mounts. It needs BPF LSM.

```yaml
agent:
  enforcement:
    enabled: true     # off by default
    dryRun: true      # report what would be refused; refuse nothing
```

Only pods with the opt-in label `tephra.dev/enforce: "true"` are refused anything, never pods in
`kube-system` or the agent's namespace, never the node's own processes and never the container runtime.
Refusals are pinned in the kernel and stay in force while the agent restarts.

Start in dry-run, watch what would be refused on your workloads, then switch it on. To turn every refusal
off at once, from a node or an agent pod:

```sh
kubectl -n tephra exec <agent pod> -- /tephrad enforce off
```

[Blind mode](../blind-mode/) is separate: it applies to every pod, but only while the sensor is blind.
