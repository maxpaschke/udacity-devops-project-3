$RESOURCE_GROUP_NAME = 'Azuredevops'
$STORAGE_ACCOUNT_NAME = "tfstate$(Get-Random)"
$CONTAINER_NAME = 'tfstate'
$CREATE_STORAGE = $true

Write-Host "Enter client_id"
$client_id = Read-Host
Write-host "Enter client_secret"
$client_secret = Read-Host

# Connect to the az account
# Connect-AzAccount
# az login

# Get the existing resource group
$resourceGroup = Get-AzResourceGroup -Name $RESOURCE_GROUP_NAME
$resourceGroup.ResourceId | Out-File -FilePath terraform/terraform_resource_group.txt -Encoding ascii
$location = $resourceGroup.Location
$subscription = Get-AzSubscription
$tenantId = $subscription.TenantId

# Create storage account
if ($CREATE_STORAGE) {
    $storageAccount = New-AzStorageAccount -ResourceGroupName $RESOURCE_GROUP_NAME -Name $STORAGE_ACCOUNT_NAME -SkuName Standard_LRS -Location $location -AllowBlobPublicAccess $true
    # Create blob container
    New-AzStorageContainer -Name $CONTAINER_NAME -Context $storageAccount.context -Permission blob
    $ACCOUNT_KEY = (Get-AzStorageAccountKey -ResourceGroupName $RESOURCE_GROUP_NAME -Name $storageaccount.StorageAccountName)[0].value
    $env:ARM_ACCESS_KEY = $ACCOUNT_KEY
}

# Adjust the terraform file
$targetTerraformfile = "./terraform/terraform.tfvars"
Copy-Item -Path "./terraform/terraform.tfvars_example" -Destination $targetTerraformfile

function setVariable($parameter) {
    $file = $parameter[2]
    $regex = '(^' + $parameter[0] + '.*=.*)"(.*)"'
    $replaceregex = '$1"' + $parameter[1] + '"'
    (Get-Content $file) -replace $regex, $replaceregex | Set-Content $file
}

setVariable("subscription_id", $subscription.Id, $targetTerraformfile)
setVariable("client_id", $client_id, $targetTerraformfile)
setVariable("client_secret", $client_secret, $targetTerraformfile)
setVariable("tenant_id", $tenantId, $targetTerraformfile)

setVariable("location", $location, $targetTerraformfile)
setVariable("resource_group", $resourceGroup.ResourceGroupName, $targetTerraformfile)
setVariable("deployment_id", $resourceGroup.Tags.DeploymentId, $targetTerraformfile)
setVariable("launch_id", $resourceGroup.Tags.LaunchId, $targetTerraformfile)
setVariable("template_id", $resourceGroup.Tags.TemplateId, $targetTerraformfile)

if ($CREATE_STORAGE) {
    $targetConf = "./terraform/terraform_backend.conf"
    Copy-Item -Path "./terraform/terraform_backend.conf_example" -Destination $targetConf

    setVariable("storage_account_name", $storageaccount.StorageAccountName, $targetConf)
    setVariable("container_name", $CONTAINER_NAME, $targetConf)
    setVariable("access_key", $ACCOUNT_KEY, $targetConf)
}




# Generate the key
# ssh-keygen -f terraform/id_rsa -N '""'

# Create the runner vm
# az vm create --resource-group $RESOURCE_GROUP_NAME --name "RunnerVM" --image "Canonical:UbuntuServer:18.04-LTS:latest" --admin-username "vmadmin" --ssh-key-values terraform/id_rsa.pub

# get the public ip
$publicIp = Get-AzPublicIpAddress -Name "RunnerVMPublicIp"

Write-Host "Connect to the vm with"
Write-Host('ssh vmadmin@' + $publicIp.IpAddress)