#!/bin/bash
resourcegroupId=$(cat terraform_resource_group.txt)
terraform import 'azurerm_resource_group.test' "$resourcegroupId"