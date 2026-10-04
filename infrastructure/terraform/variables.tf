variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  sensitive   = true
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "resource_group_name" {
  description = "Resource Group name"
  type        = string
  default     = "rg-healthpulse-dev"
}

variable "vnet_name" {
  description = "Virtual Network name"
  type        = string
  default     = "vnet-healthpulse-dev"
}

variable "vnet_address_space" {
  description = "VNet CIDR"
  type        = string
  default     = "10.10.0.0/16"
}

variable "subnet_name" {
  description = "Subnet name"
  type        = string
  default     = "snet-healthpulse-vm"
}

variable "subnet_address_prefix" {
  description = "Subnet CIDR"
  type        = string
  default     = "10.10.1.0/24"
}

variable "nsg_name" {
  description = "Network Security Group name"
  type        = string
  default     = "nsg-healthpulse-dev"
}

variable "public_ip_name" {
  description = "Public IP name"
  type        = string
  default     = "pip-healthpulse-dev"
}

variable "nic_name" {
  description = "Network Interface name"
  type        = string
  default     = "nic-healthpulse-dev"
}

variable "vm_name" {
  description = "Linux VM name"
  type        = string
  default     = "vm-healthpulse-dev"
}

variable "vm_size" {
  description = "Azure VM size"
  type        = string
  default     = "Standard_D2nlds_v6"
}

variable "admin_username" {
  description = "Linux VM admin username"
  type        = string
  default     = "healthpulseadmin"
}

variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
  sensitive   = true
}

variable "ssh_source_address" {
  description = "Allowed source address for SSH"
  type        = string
  default     = "*"
}
