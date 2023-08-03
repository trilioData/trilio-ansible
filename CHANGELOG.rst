====================================
trilio.trilio_kubernetes Release Notes
====================================

.. contents:: Topics


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