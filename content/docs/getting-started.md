---
title: Getting started
weight: 1
---

## Requirements

- x86-64 nodes with Linux **5.15 or newer**, BTF (`/sys/kernel/btf/vmlinux`) and cgroup v2.
- For enforcement and blind mode: **BPF LSM active**, that is `bpf` listed in `/sys/kernel/security/lsm`.
  Without it the agent says so in its log and only detects.
- Kubernetes and Helm 3.

## Install

{{< callout type="info" >}}
v0.2.0 publishes the chart as an OCI package on GHCR. Until then, install from a clone of the repository.
{{< /callout >}}

```sh
git clone https://github.com/tephrasec/tephra
cd tephra
helm install tephra deploy/helm/tephra -n tephra --create-namespace
```

The chart installs the agent as a DaemonSet, a collector, Loki and Grafana dashboards. Detection and
[blind mode](../blind-mode/) are on. [Enforcement](../enforcement/) stays off until you turn it on.

## Check it works

```sh
kubectl -n tephra get pods
kubectl -n tephra logs ds/tephra-agent | grep -E 'blind mode|enforcement|configuration loaded'
```

Each agent logs the rules it loaded, whether blind mode is in force, and why not if it is not.

## Remove it

`helm uninstall tephra -n tephra` raises no alert and leaves no programs or pins in the kernel: the agent
recognises a stop by Kubernetes. See [when the agent is stopped](../tamper/).
