---
title: Documentation
weight: 1
---

Tephra is a runtime threat-detection sensor for Kubernetes nodes. eBPF programs observe process, file,
network and privilege activity in the kernel; a Go agent, `tephrad`, attributes each event to a pod and
evaluates detection rules; alerts land in Grafana through Loki.

Three ideas shape it:

- **Detect from the kernel.** Programs, files and pods are recognised by identity, not only by name or path.
- **Refuse in the kernel.** Rules can block what they detect with BPF LSM, per pod, and refusals outlive the agent.
- **Hardened by default.** An attacker on a node blinds the sensor first. Tephra records the attempt, keeps
  recording while the agent is gone, and refuses the moves that come next.

{{< cards >}}
  {{< card link="getting-started" title="Getting started" subtitle="Requirements and install" >}}
  {{< card link="blind-mode" title="Blind mode" subtitle="What is refused while the sensor is blind" >}}
  {{< card link="enforcement" title="Enforcement" subtitle="Blocking rules, per pod" >}}
  {{< card link="tamper" title="When the agent is stopped" subtitle="Planned stops, kills and what is recorded" >}}
{{< /cards >}}
