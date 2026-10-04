output "resource_group_name" {
  description = "HealthPulse Resource Group"
  value       = azurerm_resource_group.healthpulse.name
}

output "vnet_name" {
  description = "HealthPulse VNet"
  value       = azurerm_virtual_network.healthpulse.name
}

output "subnet_name" {
  description = "HealthPulse Subnet"
  value       = azurerm_subnet.healthpulse.name
}

output "vm_name" {
  description = "HealthPulse VM"
  value       = azurerm_linux_virtual_machine.healthpulse.name
}

output "vm_private_ip" {
  description = "Private IP of HealthPulse VM"
  value       = azurerm_network_interface.healthpulse.private_ip_address
}

output "vm_public_ip" {
  description = "Public IP of HealthPulse VM"
  value       = azurerm_public_ip.healthpulse.ip_address
}
