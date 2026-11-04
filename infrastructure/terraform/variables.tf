variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "admin_username" {
  type    = string
  default = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Path to your SSH public key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "ssh_source_cidr" {
  description = "Your public IP in CIDR format, for example 203.0.113.10/32"
  type        = string
}

variable "vm_size" {
  type    = string
  default = "Standard_D2nlds_v6"
}
