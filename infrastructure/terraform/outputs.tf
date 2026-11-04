output "resource_group_name" {
  value = azurerm_resource_group.healthpulse.name
}

output "vm_name" {
  value = azurerm_linux_virtual_machine.healthpulse.name
}

output "vm_public_ip" {
  value = azurerm_public_ip.healthpulse.ip_address
}

output "ssh_command" {
  value = "ssh ${var.admin_username}@${azurerm_public_ip.healthpulse.ip_address}"
}
