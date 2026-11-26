---
description: "Requirements and installation of Tephra, the eBPF runtime security sensor for Kubernetes, with Helm."
title: Getting started
weight: 1
---

## Requirements

- x86-64 nodes with Linux **5.15 or newer**, BTF (`/sys/kernel/btf/vmlinux`) and cgroup v2.
- For enforcement and blind mode: **BPF LSM active**, that is `bpf` listed in `/sys/kernel/security/lsm`.
  Without it the agent says so in its log and only detects.
- Kubernetes and Helm 3.8 or newer (for charts from an OCI registry).

## Install

{{< callout type="info" >}}
v0.1.0-rc.1 is a release candidate, for testing on clusters you can throw away.
[Tell us what you find.](https://github.com/tephrasec/tephra/issues/new/choose)
{{< /callout >}}

```sh
helm install tephra oci://ghcr.io/tephrasec/charts/tephra --version 0.1.0-rc.1 \
  -n tephra --create-namespace
```

The chart names both images by digest, and the images are signed. To check a signature with
[cosign](https://github.com/sigstore/cosign):

```sh
cosign verify ghcr.io/tephrasec/tephrad@sha256:0281226b8dc21abf7e98f5c1da50ee9e58451e086b4a0f9c20dce60bb54304df \
  --certificate-identity-regexp 'https://github.com/tephrasec/tephra/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
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
