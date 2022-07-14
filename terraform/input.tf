# Azure GUIDS
variable "subscription_id" {}
variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}

# Resource Group/Location
variable "location" {}
variable "resource_group" {}
variable "application_type" {}

# Network
variable virtual_network_name {}
variable address_prefix_test {}
variable address_space {}

# VM
variable "vm_username" {
  description = "Username for the vm"
}

variable "vm_name" {
  description = "vm name postfix"
}
variable "public_key_file" {}

variable "storage_account_name" {}
variable "backend_container_name" {}
variable "access_key" {}


# Resource Group
resource "azurerm_resource_group" "test" {
    name = var.resource_group
    location = var.location
    tags     = {
          "DeploymentId" = var.deployment_id
          "LaunchId"     = var.launch_id
          "LaunchType"   = "ON_DEMAND_LAB"
          "TemplateId"   = var.template_id
          "TenantId"     = "none"
        }
}
