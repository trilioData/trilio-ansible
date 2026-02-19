# Collection: trilio.trilio_kubernetes
Set of Ansible Roles and Playbooks for Trilio Cloud-Native Intelligent Recovery products

# Python version compatibility
This collection requires Python 3.7 or greater.

# Requirements
This collection requires the following Python libraries:
- jmespath
- requests-oauthlib
- kubernetes
- openshift


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

# Usage
To use this role in your Playbook:

```yaml
- name: Trilio for Kubernetes Ansible Utility
  hosts: localhost
  roles:
    - trilio.trilio_kubernetes.trilio_kubernetes
```

There are tasks created to do the following:
- **Check Prerequisites**: Prerequisites required to operate Trilio for Kubernetes
- **Create Namespaces**: (for OpenShift you optionally can set a default SCC to ensure application can run successfully)
- **Deploy Apps**: Deploy a test application
- **Create Secrets**: Create a secret (for S3 based targets)
- **Create Targets**: A target is where backups will be stored: S3 or NFS based
- **Create Backup Plans**: A backup plan describes what to backup. Selection is namespace or label based
- **Create Backups**: Create a backup from the created backup plan
- **Perform Restores**: Perform a restore to a Namespace (from backup, backup plan, location or continuous restore)
- **Perform Trilio Continuous Restores**: Perform a Trilio Continuous Restore of a namespace or apps to a another Kubernetes cluster
- **Restore Transformation**: (Beta) Perform a restore with transformation of a namespace or apps to a another Kubernetes cluster

As an example, the task can be utilized as follows:

```yaml
- name: Trilio for Kubernetes Create Target
  ansible.builtin.include_tasks: trilio_kubernetes_create_target.yaml
  tags: ['target']
  when: trilio_kubernetes_create_target | bool
```


# Secrets 
To use S3 based Trilio for Kubernetes Targets, a secret is used for the access and secret keys. This Play can create secrets from an encrypted vault with the following structure:

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
ansible-playbook -e @secrets.enc --ask-vault-pass trilio-utility.yaml
```

# Authentication
Authentication can be done using 3 methods:
* Kubeconfig (kubeconfig)
* Variable/Encrypted Override (password)
* Credentials (external)

If using username/password authentication and not using kubeconfig specified in `trilio_kubernetes-config.yaml`<br>
Then create a separate file, *auth.enc*, and encrypt with the following structure:<br>
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
ansible-playbook -e @auth.enc -e @secrets.enc --ask-vault-pass trilio-utility.yaml
```
# Example Playbook
Example playbook can be found in the playbooks directory of the collection. It includes the Playbook called `trilio-utility.yaml`, and example configuration files. You can override any values with extra configuration files, such as the content from `-e @backup-config.yaml`.


``` bash
ansible-playbook -e @secrets.enc -e @auth.enc --ask-vault-pass trilio-utility.yaml
```

## Running Specific Tasks (Tags)
You can use tags to run specific parts of the automation:

### Basic Syntax
```bash
ansible-playbook -e@auth.enc --ask-vault-password\
    playbooks/trilio-utility.yaml --tags "tag" \
    -e@configuration-overrides.yaml
```

### Available Tags

#### Core Workflow
- **`auth`**: Performs authentication to the Kubernetes/OpenShift cluster.
- **`target`**: Manages the creation and configuration of backup targets (NFS/S3).
- **`backupplan`**: Handles the creation of backup plans.
- **`backup`**: Executes the backup process.
- **`restore`**: Performs restore operations.

#### Setup & Resources
- **`check`**: Validates prerequisites and configuration.
- **`namespace`** (or **`ns`**): Creates/manages the namespace for backups/restores.
- **`secret`**: Manages secrets (e.g., for S3 access).
- **`deploy_app`**: Deploys the demo application.

#### Testing & Verification
- **`smoketest`**: Runs the full end-to-end smoke test (often combines many of the above).
- **`smoketest_cleanup`**: Cleans up resources created during the smoke test.

#### Utilities
- **`suggest`** / **`search`** / **`autoprotect`**: Used for discovering namespaces to protect or auto-configuring protection.
- **`migrate`**: Specific tag for migration workflows.
- **`delay`**: Adds a delay (likely for waiting on resources).

#### Control Flow
- **`always`**: Tasks that should always run (unless skipped).
- **`never`**: Tasks that are skipped by default unless explicitly requested.

### Configuration Overrides (extravars)
This where you set the specific variables for the tag action you want to perform. For example, if `--tags "target"` you will need to tell Ansible about the target, target type, credentials etc.

You can find a full list of them in `defaults/main.yaml`.

There are extravars (`-e`) override examples below:
- `-e@config-deploy-app.yaml`
- `-e@config-nfs-target.yaml`
- `-e@config-backupplan.yaml`

And use them on the command line such as:

```bash
ansible-playbook -e @auth-ocp-dev.enc --ask-vault-password \
    playbooks/trilio-utility.yaml --tags "auth,target" \
    -e@config-nfs-target.yaml \
    -e "trilio_kubernetes_namespace=ansible-demo3"
```
`-e` allows you to set any variable, so the above shows the namespace we want is configurable on the command line in addition to what is in the file `config-nfs-target.yaml`.

### Deploy App (YAML URL reference)
`config-deploy-app.yaml`

```yaml
---
trilio_kubernetes_distro: openshift # kubernetes | openshift
trilio_kubernetes_auth_type: password # password | kubeconfig | external
# app yaml to deploy
trilio_kubernetes_deploy_demo_app: true
trilio_kubernetes_demo_app_yaml: https://raw.githubusercontent.com/uksysadmin/trilio-ansible-unmaintained/refs/heads/main/files/demo-mysql-app.yaml
trilio_kubernetes_scc_policy_to_ns: true
trilio_kubernetes_rbac_service_account: default
trilio_kubernetes_rbac_uid_to_use: "system:openshift:scc:anyuid"
trilio_kubernetes_create_namespace: true
```

Command:
```bash
ansible-playbook -e @auth-ocp-dev.enc --ask-vault-password \
    playbooks/trilio-utility.yaml --tags "auth,namespace,deploy_app" \
    -e@config-deploy-app.yaml \
    -e "trilio_kubernetes_namespace=ansible-demo3"
```

### Configure NFS Target in a Namespace
`config-nfs-target.yaml`

```yaml
---
trilio_kubernetes_distro: openshift # kubernetes | openshift
trilio_kubernetes_auth_type: password # password | kubeconfig | external
#
# Backup Target
#
trilio_kubernetes_create_target: true
trilio_kubernetes_target_type: nfs
trilio_kubernetes_target_name: sa-lab-nfs-share1
trilio_kubernetes_nfs_export: "172.22.5.250:/export/sa-lab-nfs-share1"
trilio_kubernetes_nfs_mount_options: "rw,async"
trilio_kubernetes_enable_browsing: true
```

Command:
```bash
ansible-playbook -e @auth-ocp-dev.enc --ask-vault-password \
    playbooks/trilio-utility.yaml --tags "auth,target" \
    -e@config-nfs-target.yaml \
    -e "trilio_kubernetes_namespace=ansible-demo3"
```

### Configure Backup Plan in a Namespace
`config-nfs-backupplan.yaml`

```yaml
---
trilio_kubernetes_distro: openshift # kubernetes | openshift
trilio_kubernetes_auth_type: password # password | kubeconfig | external
# Namespace Information
#
# List of namespaces where backups will be created. Ensure in [] list or
# on seperate lines, e.g.
# trilio_kubernetes_backup_namespaces: [ mynamespace1 ]
# or
# trilio_kubernetes_backup_namespaces: [ mynamespace1, mynamespace2 ]
# or
# trilio_kubernetes_backup_namespaces:
#   - mynamespace1
#   - mynamespace2
trilio_kubernetes_backup_namespaces: ["{{ trilio_kubernetes_namespace }}"]
#
# Backup Plan Details
# Note this must be relevant to the test/demo app
#
trilio_kubernetes_create_backupplan: true
trilio_kubernetes_backupplan_override: false
trilio_kubernetes_backupplan_name: "{{ trilio_kubernetes_namespace }}-backupplan"
trilio_kubernetes_backupplan_type: ns # ns|label|operator
trilio_kubernetes_backup_match_label: "app: k8s-demo-app" # ignored for ns backup type
trilio_kubernetes_backupplan_polling_retries: 20
trilio_kubernetes_backupplan_polling_every_seconds: 30
trilio_kubernetes_target_name: "sa-lab-nfs-share1"
```

Command:
```bash
ansible-playbook -e @auth-ocp-dev.enc --ask-vault-password \
    playbooks/trilio-utility.yaml --tags "auth,backupplan" \
    -e@config-nfs-backupplan.yaml \
    -e "trilio_kubernetes_namespace=ansible-demo3"
```

### Perform a Backup
`config-backup.yaml`

```yaml
---
trilio_kubernetes_distro: openshift # kubernetes | openshift
trilio_kubernetes_auth_type: password # password | kubeconfig | external
trilio_kubernetes_backup_namespaces: ["{{ trilio_kubernetes_namespace }}"]
#
# Backup Plan Details
# Note this must be relevant to the test/demo app
#
trilio_kubernetes_backupplan_name: "{{ trilio_kubernetes_namespace }}-backupplan"
#
# Perform Backup
trilio_kubernetes_create_backup: true
trilio_kubernetes_backup_prefix: "{{ trilio_kubernetes_backupplan_name }}"
trilio_kubernetes_backup_wait: true
trilio_kubernetes_backup_polling_retries: 20
trilio_kubernetes_backup_polling_every_seconds: 10
trilio_kubernetes_backup_batch_size: 1
```

Command:
```bash
ansible-playbook -e @auth-ocp-dev.enc --ask-vault-password \
    playbooks/trilio-utility.yaml --tags "auth,backup" \
    -e@config-backup.yaml \
    -e "trilio_kubernetes_namespace=ansible-demo3"
```

### Perform a Multi-Namespace Backup with Batching
`config-multibackup.yaml`

```yaml
---
trilio_kubernetes_distro: openshift # kubernetes | openshift
trilio_kubernetes_auth_type: password # password | kubeconfig | external
# trilio_kubernetes_backup_namespaces: ["{{ trilio_kubernetes_namespace }}"]
#
# Backup Plan Details
# Note this must be relevant to the test/demo app
#
trilio_kubernetes_backupplan_name: "{{ trilio_kubernetes_namespace }}-backupplan"
#
# Backup Target
#
# Currently assumes AWS S3
# IMPORTANT: See templates/target.yaml.j2 to modify for other targets
# TODO: Specify NFS or S3
trilio_kubernetes_create_target: true
trilio_kubernetes_target_type: nfs
trilio_kubernetes_target_name: sa-lab-nfs-share1
trilio_kubernetes_nfs_export: "172.22.5.250:/export/sa-lab-nfs-share1"
trilio_kubernetes_nfs_mount_options: "rw,async"
trilio_kubernetes_enable_browsing: true
#
# Perform Backup
trilio_kubernetes_create_backup: true
trilio_kubernetes_backup_prefix: "{{ trilio_kubernetes_backupplan_name }}"
trilio_kubernetes_backup_wait: true
trilio_kubernetes_backup_polling_retries: 20
trilio_kubernetes_backup_polling_every_seconds: 10
trilio_kubernetes_backup_batch_size: 5
```

Command:
```bash
ansible-playbook -e @auth-ocp-dev.enc --ask-vault-password \
    playbooks/trilio-utility.yaml \
    --tags "auth,target,backupplan,backup" \
    -e@config-multibackup.yaml \
    -e "trilio_kubernetes_backup_namespaces=['ansible-demo1','ansible-demo2','ansible-demo3']" \
    -e "trilio_kubernetes_backup_type=Incremental trilio_kubernetes_backup_batch_size=2"
```
## Trilio Continuous Restore
An example Ansible Configuration Override to perform a Continuous Restore. In this example, you authenticate to the _restore cluster_ only but specify the original backup plan and target from the source cluster:

``` yaml
---
trilio_kubernetes_distro: openshift
trilio_kubernetes_auth_type: external

# Backup Plan Details
trilio_kubernetes_backupplan_name: "rh-summit-demo"
trilio_kubernetes_namespace: "demonstration"
trilio_kubernetes_target_name: "trilio-demo-event-target"
# Perform Restore
trilio_kubernetes_restore_type: cr
trilio_kubernetes_create_restore: true
trilio_kubernetes_restore_namespace: demonstration
trilio_kubernetes_restore_polling_retries: 10
trilio_kubernetes_restore_polling_every_seconds: 60
trilio_kubernetes_restore_data_only: false
# Currently only for CR restores
trilio_kubernetes_restore_delete_pvc_before_restore: false

# Continuous Restore
trilio_kubernetes_cr_backupplan: "{{ trilio_kubernetes_backupplan_name }}"
trilio_kubernetes_event_target: "{{ trilio_kubernetes_target_name }}"
```
<br>

## Ansible Automation Platform/Galaxy Tower
When Authenticating using Ansible Automation Platform's Credentials, specify ``trilio_kubernetes_auth_type: external``.
Then create a Credential of type ``OpenShift or Kubernetes API Bearer Token``. Then in the Template, select the _Credential_ created.

# Restore Examples
Trilio Ansible Role provides the ability to perform different restores:
* Restore specific backup name
* Restore last backup from a backup plan
* Restore from a location UUID
* Restore from Continuous Restore (e.g Disaster Recovery scenario)

These are configured in the variable ``trilio_kubernetes_restore_type: cr # backup | backupplan | location | cr | snapshot``

