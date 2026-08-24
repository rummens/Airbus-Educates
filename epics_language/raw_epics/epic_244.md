# TITLE: OpenShift Virtualization & Nested Clusters
# STATE: opened
# PARENT: 220
# LABELS: P::1,complexity::high,external-support,subproduct::infrastructure

_Gopal, Vivek & RedHat_

## Epic Description

The **OpenShift Virtualization & Nested Clusters** epic focuses on the manual integration of KubeVirt into the bare-metal stack. The goal is to create a library of **Reusable VM Blueprints** (VirtualMachineInstance templates) that are pre-configured with the necessary hardware specs, ignition configs, and networking to host a nested OpenShift installation. This epic delivers the "Lego bricks" and the manual instructions needed to stand up a virtual cluster.

High Level [Drawing](https://docs.google.com/drawings/d/1JRNq5l_EgKAkTVYUSg7cbdcD5Ri3SdxiTlydwlJo9nA/edit):

![image](/uploads/8792e723bf72f9bd08210b89438cbc5b/image.png){width=858 height=560}

## Importance of the Epic

By mastering the manual deployment of nested clusters, the team gains deep visibility into the underlying resource requirements and networking constraints of OpenShift Virtualization. This approach ensures we are not "black-boxed" by automation. It allows for highly customized cluster configurations—such as specific disk layouts or custom networking via Multus—that automated tools might skip, ensuring our virtualized stack is tuned specifically for our bare-metal hardware.

## Functional Requirements

* **Operator Lifecycle:** Deploy OpenShift Virtualization and MetalLB/NMState operators to handle VM traffic and LoadBalancing.
* **Gold Images:** Create and maintain "Gold" Boot Sources (PVCs) for Red Hat Enterprise Linux CoreOS (RHCOS) to speed up VM creation.
* **Blueprint Library:** Develop YAML manifests for:
* **Control Plane VMs:** (High CPU/RAM, anti-affinity rules).
* **Worker VMs:** (Scaleable templates with specific storage mounts).
* **Networking Procedure:** Define a manual procedure for assigning static IPs or MAC addresses to VMs to ensure nested API and Ingress VIPs remain stable.
* **Storage Profiles:** Configure Trident to provide `ReadWriteMany` (RWX) capabilities for VM live migration.

## Non-Functional Requirements

* **Documentation:** Provide a step-by-step "Runbook" for manual cluster assembly (Load Balancer config -> Control Plane -> Workers).
* **Performance:** Configure **HugePages** and **CPU Pinning** in the VM manifests to reduce latency for nested workloads.
* **Stability:** Ensure that VM-based nodes can survive a restart of the physical host without losing data (Persistent Volume mapping).
* **Observability:** Configure the `kubevirt-vm-latency` and resource usage dashboards in the default OpenShift console.

---

### Proposed High-Level Procedure

1. **Prepare the Host:** Configure Bridge networking on bare-metal nodes.
2. **Define the "Flavor":** Apply the `VirtualMachine` manifests defining 4 vCPUs and 16GB RAM for control planes.
3. **Inject Identity:** Use `cloud-init` or `Ignition` inside the manifest to point the virtual node to your internal load balancer.
4. **Install:** Manually run the OpenShift installer from a "Bastion" VM within the same network.

## Roadmap Summary
Integrate KubeVirt on bare-metal with VM blueprints to enable manual deployment of nested OpenShift clusters for DCS.