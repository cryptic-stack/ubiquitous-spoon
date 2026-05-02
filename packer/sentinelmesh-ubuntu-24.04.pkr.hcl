packer {
  required_plugins {
    qemu = {
      version = ">= 1.1.0"
      source  = "github.com/hashicorp/qemu"
    }
  }
}

variable "ubuntu_iso_path" {
  type        = string
  description = "Path to the Ubuntu Server 24.04 LTS ISO."
}

variable "ubuntu_iso_checksum" {
  type        = string
  description = "Checksum for the Ubuntu Server ISO."
  default     = "none"
}

source "qemu" "sentinelmesh" {
  iso_url           = var.ubuntu_iso_path
  iso_checksum      = var.ubuntu_iso_checksum
  output_directory  = "build/packer/sentinelmesh-ubuntu-24.04"
  shutdown_command  = "echo 'packer' | sudo -S shutdown -P now"
  disk_size         = "40960M"
  memory            = 4096
  cpus              = 2
  headless          = true
  format            = "qcow2"
  ssh_username      = "sentinel"
  ssh_password      = "sentinel"
  ssh_timeout       = "30m"
}

build {
  name = "sentinelmesh-ubuntu-24.04"
  sources = [
    "source.qemu.sentinelmesh"
  ]
}

