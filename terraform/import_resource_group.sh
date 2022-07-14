#!/bin/bash
resourcegroupId=$(az group list | python -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")
echo $resourcegroupId
terraform import azurerm_resource_group.test $resourcegroupId