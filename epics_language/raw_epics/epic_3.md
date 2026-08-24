# TITLE: Registry Improvements / Supply Chain Security
# STATE: opened
# PARENT: 220
# LABELS: P::2,complexity::medium,subproduct::registry

## Epic Description

The Supply Chain epic focuses on securing the software supply chain for the OpenShift service by implementing signing mechanisms for Helm charts, images, and Git commits. This ensures that the components deployed across countries are verified and trustworthy. The epic also includes setting up an immutable log database and PKI infrastructure to track the integrity of the software components and enable secure deployment processes.

## Importance of the Epic

This epic is essential for maintaining the integrity and security of the software supply chain. By implementing image, Helm chart, and Git commit signing, we can ensure that only verified and trusted components are used in the OpenShift deployments. The use of immutable logs and PKI infrastructure enhances security by providing a transparent and auditable record of all changes and deployments.

## Functional Requirements

* Implement signing mechanisms for Helm charts, images, and Git commits based on the sigstore project.  
* Set up an immutable log database to track software changes and deployments.  
* Establish PKI infrastructure for secure signing and verification processes.

## Non-Functional Requirements

* Security: Ensure the signing process and immutable logs are secure and tamper-proof.  
* Scalability: The signing and logging system must scale as the service grows.  
* Maintainability: The signing and PKI infrastructure should be easy to update and manage.  
* Compliance: Ensure compliance with industry standards and security regulations.  
* Usability: The signing and logging processes should be straightforward for developers and operators.

## Roadmap Summary
Secure the DCS supply chain via image/chart signing, PKI, and immutable logs to ensure verified, trustworthy deployments across all regions.