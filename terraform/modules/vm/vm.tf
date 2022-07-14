resource "azurerm_network_interface" "test" {
  name                = "udacity-VM-NIC"
  location            = var.location
  resource_group_name = var.resource_group

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = var.public_ip
  }
}

resource "azurerm_linux_virtual_machine" "test" {
  name                = "${var.application_type}-${var.resource_type}-${var.name}"
  location            = var.location
  resource_group_name = var.resource_group
  size                = "Standard_B2s"
  admin_username      = var.vm_username
  network_interface_ids = [azurerm_network_interface.test.id]
  disable_password_authentication = false
  source_image_id     = var.image_id

  admin_ssh_key {
    username   = var.vm_admin_username
    public_key = file(var.public_key_file)
  }
  
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
}
