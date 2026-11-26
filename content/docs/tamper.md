---
title: When the agent is stopped
weight: 4
---

Anything done through Kubernetes raises no alert: `kubectl rollout restart`, `helm upgrade`, deleting an
agent pod, draining a node, `helm uninstall`. The agent recognises these stops because the kernel shows the
container runtime sent the signal.

Any other stop leaves a record:

| What happens | What Tephra does |
|---|---|
| A signal to the agent from anything else | **R030**, critical, with the sender and its pod |
| An attach to the agent, or a write to its memory | **R033**, critical |
| The agent killed, crashed or frozen | Detection stays pinned and recording; the next agent reads what happened in between |
| A node goes quiet | The collector reports the gap as **R031** |
| Actions while the sensor is blind | Refused by [blind mode](../blind-mode/), reported as **R038** |

Records of attacks on the agent go to a ring buffer of their own, so a flood of other events cannot push
them out; if even that buffer is full, the kernel counts the loss and the agent still raises the alert.

Someone with root on the node, or a cluster administrator, can still stop Tephra; no sensor can prevent its
own administrator. What they cannot do is stop it without a trace.
