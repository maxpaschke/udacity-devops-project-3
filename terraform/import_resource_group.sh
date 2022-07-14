#!/bin/bash
resourcegroupId=$(cat terraform_resource_group.txt)
echo $resourcegroupId
terraform import 'azurerm_resource_group.test' "$resourcegroupId"