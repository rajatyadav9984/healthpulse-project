terraform {
  required_version = ">= 1.15.0"

  backend "azurerm" {
    resource_group_name  = "rg-healthpulse-tfstate"
    storage_account_name = "sthealthpulsetfstate2610"
    container_name       = "tfstate"
    key                  = "healthpulse.tfstate"
  }

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

# -------------------------
# Resource Group
# -------------------------

resource "azurerm_resource_group" "healthpulse" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    project     = "HealthPulse"
    environment = var.environment
    managed_by  = "Terraform"
  }
}

# -------------------------
# Virtual Network
# -------------------------

resource "azurerm_virtual_network" "healthpulse" {
  name                = var.vnet_name
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name
  address_space       = [var.vnet_address_space]

  tags = {
    project = "HealthPulse"
  }
}

# -------------------------
# Subnet
# -------------------------

resource "azurerm_subnet" "healthpulse" {
  name                 = var.subnet_name
  resource_group_name  = azurerm_resource_group.healthpulse.name
  virtual_network_name = azurerm_virtual_network.healthpulse.name
  address_prefixes     = [var.subnet_address_prefix]
}

# -------------------------
# Network Security Group
# -------------------------

resource "azurerm_network_security_group" "healthpulse" {
  name                = var.nsg_name
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name

  # SSH Rule
  security_rule {
    name                       = "Allow-SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.ssh_source_address
    destination_address_prefix = "*"
  }

  # HTTP Rule
  security_rule {
    name                       = "Allow-HTTP"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    project = "HealthPulse"
  }
}

# -------------------------
# Public IP
# -------------------------

resource "azurerm_public_ip" "healthpulse" {
  name                = var.public_ip_name
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = {
    project = "HealthPulse"
  }
}

# -------------------------
# Network Interface
# -------------------------

resource "azurerm_network_interface" "healthpulse" {
  name                = var.nic_name
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.healthpulse.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.healthpulse.id
  }

  tags = {
    project = "HealthPulse"
  }
}

# -------------------------
# NSG -> NIC Association
# -------------------------

resource "azurerm_network_interface_security_group_association" "healthpulse" {
  network_interface_id      = azurerm_network_interface.healthpulse.id
  network_security_group_id = azurerm_network_security_group.healthpulse.id
}

# -------------------------
# Linux Virtual Machine
# -------------------------

resource "azurerm_linux_virtual_machine" "healthpulse" {
  name                = var.vm_name
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name
  size                = var.vm_size
  admin_username      = var.admin_username

  disable_password_authentication = true

  network_interface_ids = [
    azurerm_network_interface.healthpulse.id
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }

  os_disk {
    name                 = "${var.vm_name}-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }

  tags = {
    project     = "HealthPulse"
    environment = var.environment
    managed_by  = "Terraform"
  }
}
