$result = az group list
$result_as_json = $result | ConvertFrom-Json
# How to import a resource
terraform import azurerm_resource_group.test $result_as_json[0].id