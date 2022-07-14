# Ensuring Quality Releases - Udacity Cloud DevOps using Microsoft Azure Project 3

# Overview
This project demonstrates automated testing in Azure with end to end (E2E), unit testing and monitoring.

# Architecture Diagramm


# Instructions

* Setup the cloud shell
  - Open the cloud shell from Azure Portal
  - Select "Bash" as input
  - Configure advanced options
  - Use new fileshare and new storage accounts if you have not created them already.
  - Run the following commands:
    - `ssh-keygen -t rsa`
    - `cat /home/odl_user/.ssh/id_rsa.pub`
    - Copy the output of the `cat` command. It should start with "rsa"
  - Go to [github.com/settings/keys](github.com/settings/keys)
  - Save the keys to `priv_key.rsa` and `pub_key.rsa`
  - Add the new SSH Key

* Clone the repo into the cloud shell
  * Use the SSH clone, like `git clone git@github.com:maxpaschke/udacity-devops-third.git`

* Run setup.ps1 to create the following
  * Terraform config
  * VM for the pipeline runner

* Setup the Azure Devops organisation
  - Login to Azure on the Azure Portal
  - Go to https://aex.dev.azure.com/
  - Enter your details and continue
  - Create new organisation
  - Goto Organization Settings >> Policies 
    - Enable public projects
  - Create a new project
    - Name the project `udacity-azure-devops`
  - Setup the service connection in the Project settings >> Service connection
    - `Create service connection`
    - Select `Azure resource manager` and then `Service Principal (manual)`
    - Enter the details from the Udacity cloud lab
    - Set `Allow access to all pipelines to true`
    - Get the subscription name from the azure portal
    - Name the service connection `AzureUdacity`

* Create the agent pool in Azure Devops
  * Goto Project Settings >> Agent Pools
  * Press `Add Pool`
    * Select `Self-hosted`
    * Name: `myAgentPool`
    * Enable `Grant access permission to all pipelines`

* Setup terraform
  - Replace the values below in terraform/main.tf with the output from `Create_storage_account.ps1` above
  - Run the import script `import_resource_group.ps1` in the terraform folder
  - Modify the tags of the existing resource group resource to match the resourcegroup in `input.tf`
  - Run `terraform apply`

* Create a new pipeline and connect it
  - Goto `Pipelines` in the Azure Devops project
  - Select `Create`
    - In the Connect Wizard Select `Github`
    - Choose your repository
    - Select existing yaml file
      - Select `azure-pipelines.yaml`
      - Adjust the webapp name to your new name

- Create a Personal Access Token (PAT)
    - Goto [Dev.azure.com](https://dev.azure.com/)
    - Select `Personal Access Tokens` from the user settings menu
    - Click `Create new Token`
      - Name it `PAT_udacity`
      - Give it `Full access`
      - Create it
      - Save the Token

* Add the pipeline agent to the VM
  *  Connect to the VM via Azure cloud shell
    - `ssh devopsagent@$VMIP$`, use your specific IP for the VM here.
  * Add the agent:
  ``` bash
        # Download the agent
        curl -O https://vstsagentpackage.azureedge.net/agent/2.204.0/vsts-agent-linux-x64-2.204.0.tar.gz
        # Create the agent
        mkdir myagent && cd myagent
        tar zxvf ../vsts-agent-linux-x64-2.204.0.tar.gz
        # Configure the agent
        ./config.sh --unattended --url https://dev.azure.com/odluser200841/ --auth pat --token ag2xd2ulzrk27d77nc5ploam5c5ybbiexofyv72m3ghht2pipsoa
        # Finish the setup
        sudo ./svc.sh install
        sudo ./svc.sh start
  ```