#!/usr/bin/env bash
set -euo pipefail

if ! command -v ansible-playbook >/dev/null 2>&1; then
  echo "ansible-playbook is not installed; skipping Ansible syntax check."
  exit 0
fi

ANSIBLE_CONFIG=ansible/ansible.cfg ansible-playbook -i ansible/inventory.ini --syntax-check ansible/site.yml

echo "Ansible syntax check passed."
