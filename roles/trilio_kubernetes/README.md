# Collection: trilio.trilio_kubernetes
Set of Ansible Roles and Playbooks for Trilio Cloud-Native Intelligent Recovery products

# Python version compatibility
This collection requires Python 3.7 or greater.

# Using this collection
You can install this collection using the ansible-galaxy tool:

```bash
ansible-galaxy collection install trilio.trilio_kubernetes
```

You can also include it in a requirements.yml file and install it via ansible-galaxy collection install -r requirements.yml using the format:

```yaml
collections:
- name: trilio.trilio_kubernetes
```

Note that if you install the collection manually, it will not be upgraded automatically when you upgrade the Ansible package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install trilio.trilio_kubernetes --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax where X.Y.Z can be any available version:

```bash
ansible-galaxy collection install trilio.trilio_kubernetes:==X.Y.Z
```
# Important Variable Name Changes
To align to required Ansible standard and naming conventions, variable prefix has been changed from *tvk_* to *trilio_kubernetes*.<br>
Tasks have also been renamed. This affects any new installations and upgrades *1.1.0* and newer.

# Usage
To use this role in your Playbook:

```yaml
- name: Trilio for Kubernetes Ansible Utility
  hosts: localhost
  vars_files: trilio_kubernetes-config.yaml
  roles:
    - trilio.trilio_kubernetes.trilio_kubernetes
```

There are tasks created to do the following
- Check prerequisites required to operator Trilio for Kubernetes
- Create a namespace (for OpenShift you optionally can set a default SCC to ensure application can run sucessfully)
- Deploy a test application 
- Create a secret (for S3 based targets)
- Create a target (a target is where backups will be stored: S3 or NFS based)
- Create a backup plan (a backup plan describes what top backup. Selection is namespace or label based)
- Create a backup from the created backup plan
- Perform a restore to a Namespace
- Perform all the above steps as part of a smoketest run

As an example, the task can be utilized as follows:

```yaml
- name: Trilio for Kubernetes Create Target
  ansible.builtin.include_tasks: trilio_kubernetes_create_target.yaml
  tags: ['target']
  when: trilio_kubernetes_create_target | bool
```

# Example Playbook
Example playbook can be found in the playbooks directory of the collection. It includes the Playbook called tvk-utility.yaml, and example configuration files. trilio_kubernetes-config.yaml is always referenced. You can override any values with extra configuration files, such as the content from -e @backup-config.yaml.


``` bash
ansible-playbook -e @secrets.enc -e @auth.enc --vault-ask-pass tvk-utility.yaml
```

```bash
ansible-playbook -e @secrets.enc -e @auth.enc --vault-ask-pass tvk-utility.yaml --tags "auth"
ansible-playbook -e @secrets.enc -e @auth.enc --vault-ask-pass tvk-utility.yaml --tags "check"
ansible-playbook -e @secrets.enc -e @auth.enc --vault-ask-pass tvk-utility.yaml --tags "backup"
ansible-playbook -e @secrets.enc -e @auth.enc --vault-ask-pass tvk-utility.yaml --tags "smoketest"
```

# Configuration
Configuration is done in a default configuration file *trilio_kubernetes-config.yaml* to allow for automation.<br>
Any of the variables can be overridden and placed in an override configuration file, later specified on the <br>
command line e.g. -e @/path/to/my-config.yaml

``` yaml
# Specify environment/auth details - username/pass (in a vault specified on cli)
# Username/Pass
# Note: 'openshift' assumes kubectl and oc tools installed
trilio_kubernetes_distro: openshift # kubernetes | openshift
trilio_kubernetes_auth_type: password # password | kubeconfig
# trilio_kubernetes_auth_api: https://auth_endpoint:6443/ # auth API server if not using kubeconfig
                                             # Recommend to store in auth.enc with credentials and
                                             # encrypt and pass as -e @auth.enc
# Kubeconfig
kubeconfig: # path to kubeconfig file if kube_auth_type is 'kubeconfig'

# Always authenticate unless you have a reason to skip this
trilio_kubernetes_auth: true
# Performs a check of the license and other prequisites
trilio_kubernetes_check: true
# Uses the values in the config file to create a demo app, target, backuppplan, backup and restore.
# Set this value for first installation test
trilio_kubernetes_smoketest: true

# Search for suggested NS to backup
trilio_kubernetes_suggest: true
# Auto create NS Backup Plan 
trilio_kubernetes_autoprotect: true
# List of NS to exclude
trilio_kubernetes_autoprotect_exclude: ['openshift-storage','openshift-operators','default']

# app yaml to deploy
trilio_kubernetes_deploy_demo_app: false
trilio_kubernetes_namespace: smoketest
trilio_kubernetes_demo_app_yaml: files/demo-mysql-app.yaml

#
# Backup Target
#
# Currently assumes AWS S3
# IMPORTANT: See templates/target.yaml.j2 to modify for other targets
# TODO: Specify NFS or S3
trilio_kubernetes_create_target: true
trilio_kubernetes_target_type: S3
trilio_kubernetes_target_name: smoketest-target
trilio_kubernetes_s3_bucket_name: tvk-migration-demo1
trilio_kubernetes_secret_name: s3-access-secret

#
# Backup Plan Details
# Note this must be relevant to the test/demo app
#
trilio_kubernetes_create_backupplan: true
trilio_kubernetes_backupplan_name: smoketest-app-backupplan
trilio_kubernetes_backupplan_type: ns # ns|label
trilio_kubernetes_backup_match_label: "app: k8s-demo-app" # ignored for ns backup type

#
# Perform Backup
trilio_kubernetes_backup_prefix: "{{ trilio_kubernetes_backupplan_name }}"
trilio_kubernetes_backup_type: Full # Full | Incremental

# Perform Restore (to new ns)
trilio_kubernetes_restore_namespace: smoketest-restore

# Used for migration/DR smoketest
trilio_kubernetes_dr_restored_namespace: dr-restore
trilio_kubernetes_dr_backupplan: "{{ backupplan_name }}" # if specified, uses last known backup
trilio_kubernetes_location_id: # can specify which backup to restore to if known
```

# Secrets 
To create S3 based Trilio for Kubernetes Targets, a secret is used. This Play can create secrets from an encrypted vault with the following structure:

``` yaml
secrets:
  - name: s3-access-secret
    type: generic
    data:
      - key: accessKey
        value: YOURACCESSKEY
      - key: secretKey
        value: YOURSECRETKEY
```
Create this in a file called *secrets.enc* then encrypt with<br>
``` bash
ansible-vault encrypt secrets.enc
```
You would then specify this on the command line with<br>
``` bash
ansible-playbook -e @secrets.enc --vault-ask-pass tvk-utility.yaml
```

# Authentication
If using username/password authentication and not using kubeconfig specified in trilio_kubernetes-config.yaml<br>
Then create a seperate file, *auth.enc*, and encrypt with the following structure:<br>
``` yaml
trilio_kubernetes_auth_api: https://auth_endpoint_url:6443
trilio_kubernetes_username: username
trilio_kubernetes_password: password
```
Encrypt this file with the following:
``` bash
ansible-vault encrypt auth.enc
```
You would then specify this on the command line with<br>
``` bash
ansible-playbook -e @auth.enc -e @secrets.enc --vault-ask-pass tvk-utility.yaml
```
<br>
