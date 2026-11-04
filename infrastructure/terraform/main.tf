resource "azurerm_resource_group" "healthpulse" {
  name     = "rg-healthpulse-vm-demo"
  location = var.location
}

resource "azurerm_virtual_network" "healthpulse" {
  name                = "vnet-healthpulse-vm-demo"
  address_space       = ["10.20.0.0/16"]
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name
}

resource "azurerm_subnet" "healthpulse" {
  name                 = "snet-healthpulse-vm"
  resource_group_name  = azurerm_resource_group.healthpulse.name
  virtual_network_name = azurerm_virtual_network.healthpulse.name
  address_prefixes     = ["10.20.1.0/24"]
}

resource "azurerm_network_security_group" "healthpulse" {
  name                = "nsg-healthpulse-vm-demo"
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name

  security_rule {
    name                       = "Allow-SSH-From-My-IP"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.ssh_source_cidr
    destination_address_prefix = "*"
  }

  # Demo access for the HealthPulse Flask app
  security_rule {
    name                       = "Allow-HealthPulse-5000"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_public_ip" "healthpulse" {
  name                = "pip-healthpulse-vm-demo"
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_network_interface" "healthpulse" {
  name                = "nic-healthpulse-vm-demo"
  location            = azurerm_resource_group.healthpulse.location
  resource_group_name = azurerm_resource_group.healthpulse.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.healthpulse.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.healthpulse.id
  }
}

resource "azurerm_network_interface_security_group_association" "healthpulse" {
  network_interface_id      = azurerm_network_interface.healthpulse.id
  network_security_group_id = azurerm_network_security_group.healthpulse.id
}

resource "azurerm_linux_virtual_machine" "healthpulse" {
  name                = "vm-healthpulse-app-demo"
  resource_group_name = azurerm_resource_group.healthpulse.name
  location            = azurerm_resource_group.healthpulse.location
  size                = var.vm_size

  admin_username                  = var.admin_username
  disable_password_authentication = true

  network_interface_ids = [
    azurerm_network_interface.healthpulse.id
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(pathexpand(var.ssh_public_key_path))
  }

  os_disk {
    name                 = "osdisk-healthpulse-vm-demo"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }
}
