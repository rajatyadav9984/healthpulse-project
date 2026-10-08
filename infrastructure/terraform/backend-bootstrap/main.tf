terraform {
  required_version = ">= 1.15.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "= 5.7.0"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id                 = var.subscription_id
  resource_provider_registrations = "core"
}

# =========================================================
# VARIABLES
# =========================================================

variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

# =========================================================
# RESOURCE GROUP
# =========================================================

resource "azurerm_resource_group" "healthpulse" {
  name     = "rg-healthpulse-dev"
  location = var.location

  tags = {
    project     = "HealthPulse"
    environment = "dev"
    managed_by  = "Terraform"
  }
}

# =========================================================
# STORAGE ACCOUNT FOR TERRAFORM REMOTE STATE
# =========================================================

resource "azurerm_storage_account" "tfstate" {
  name                     = "sthealthpulsetfstate2610"
  resource_group_name      = azurerm_resource_group.healthpulse.name
  location                 = azurerm_resource_group.healthpulse.location

  account_tier             = "Standard"
  account_replication_type = "LRS"

  min_tls_version = "TLS1_2"

  tags = {
    project     = "HealthPulse"
    environment = "dev"
    purpose     = "Terraform Remote State"
    managed_by  = "Terraform"
  }
}

# =========================================================
# STORAGE CONTAINER
# =========================================================

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"
}
