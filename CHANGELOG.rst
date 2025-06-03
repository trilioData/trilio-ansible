====================================
trilio.trilio_kubernetes Release Notes
====================================

.. contents:: Topics
v1.4.1
======

Minor Changes
-------------
- Minor linting issues

v1.4.0
======

Major Changes
-------------
- Added external auth support for use with Ansible Automation Platform Credentials
- Added support for batched Backups
- Added support for Continuous Restore restores (trilio_kubernetes_restore_type: cr)
- Other bug fixes

v1.3.0
======

Minor Changes
-------------
- Added support for Operator Backups
- Added support for multiple namespace Backups


v1.2.1
======

Minor Bugfixes
--------------
- Fixes for shell task change notification
- Fixes for retries on target and backupplan creation
- Fixes for ansible CLI and Password based auth
- Other syntax and lint fixes

v1.2.0
======

Minor Changes
-------------
- Added support for Continuous Restore restores
- Added additional options to support all S3 vendors

v1.1.3
======

Minor Changes
-------------
- Added support for OpenShift Bearer Credential type in Ansible Automation Platform


v1.1.2
======

Minor Changes
-------------
- Added trilio_kubernetes_operator_namespace variable, defaults to trilio-system
- Renamed example playbook to trilio-utility.yaml

Bugfixes
--------

- User/password authentication fixes for various tasks, namely missing host for check tasks.

v1.1.1
======

Minor Changes
-------------
- Added trilio_kubernetes_cli boolean as a switch to run kubectl/oc commands for polling or not. Useful, currently, for running in Ansible Automation Platform.

Bugfixes
--------

- User/password authentication inadvertenly required kubeconfig environment. This is no longer required.

v1.1.0
======

Major Changes
-------------

- Renamed tasks from tvk_task to trilio_kubernetes_task. Playbooks will need to be updated accordingly.

v1.0.0
======
Initial Release