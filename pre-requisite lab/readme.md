# Deep Learning Institute Robot Workshop Pre-Requiste Lab

In this lab, we'll walk workshop attendees through the required pre-requisite steps.  At the completion of this lab, attendees should have a properly prepared Virtual Machine running in Azure that has the NVidia GPUs, and lab assets needed for successful completion of the workshop.

---

<a name="prereqs"></a>

## Pre-Requisites

To complete this lab, you will need to have the following items:

1. An active azure subscription that you are willing to use for the lab.  ***BE AWARE** the lab has you create N-Series VMs in Azure.  These VMs are special because they include NVidia GPU support and provide an extremely powerful environment for deep learning projects.  However, they are expensive when compared to other less capable VMs.  It is recommended that you use a trial subscription, or a subscription provided to you at a live event for the lab steps.  This will help to ensure that you are not billed for excessive VM utilization.

1. Nodejs v6.9.4 or later. You can download the current version of Nodejs from [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

1. Git installed.  If you don't have git on your system, you can install it from [https://git-scm.com/downloads](https://git-scm.com/downloads)

___

<a name="tasks"></a>

## Tasks

In this lab, you will complete the following tasks:

1. [Understanding the Azure Resources in this Lab](#task1)
1. [Creating your Azure Subscription](#task2)
1. [Installing the Azure Command-Line Interface (Azure CLI)](#task3)
1. [Logging into your Azure Subscription via the Azure-CLI](#task4)
1. [Creating an Azure Storage Account, and Container](#task5)
1. [Copying the Virtual Hard Disk (VHD) for the Virtual Machine](#task6)
1. [Creating the Virtual Machine using the VHD](#task7)
1. [Configuring your Virtual Machine Firewall](#task8)
1. [Connecting to your Virtual Machine using SSH](#task9)

---

<a name="task1"></a>

## Understanding the Azure Resources in this Lab

In this workshop, you will be using an Azure Virtual Machine (VM) to complete your work. The Virtual Machine will use a copy of a pre-existing Virtual Hard Disk (VHD) that we have created for your use.  The pre-existing VHD has Ubuntu 16.0.4 LTS installed, along with all of the deep learning tools, frameworks, data sets and jupyter notebooks that you will need for the lab.  The purpose of this pre-requisite lab is to walk you step-by-step through the process of configuring your Azure Subscription with the resources necessary to complete the workshop.  This section is provided to help you better understand what those resources are in an effort to help you better understand the subsequent tasks, and the workshop overall.

### Azure Resource Groups

Azure resources like storage accounts, virtual machines, etc., are organized into "Resource Groups".  You will be creating a "Resource Group" in your azure subscription, and then you will create your Azure Storage Account and Azure Virtual machine inside that resource group. 

### Azure Locations (Data Centers)

The Azure Virtual Machine used in this workshop requires the use of NVidia GPUs.  Azure offers Virtual Machine instances with access to dedicated NVidia GPU hardware in it's "N-Series" VM offering.  Currently, at the time this pre-requisite lab is being written, the only Azure Location where N-Series VMs are supported is in the "South Central US" data center.  Therefore, as we provision the resources in the following tasks, we need to make sure to use the "South Central US" location.  

### Azure Storage accounts

Azure Storage Accounts are a core Azure offering.  They support the storage of data in a variety of formats using a number of built-in services.  In this lab, we will be using Azure Storage Blob Containers to store the Virtual Hard Disk (VHD) for our Virtual Machine.  To accomplish this, we will need to first provision an Azure Storage account in our subscription, and place it in the "South Central US" location.  Azure Storage Accounts are globally accessible and as such need a globally unique name. 

___

<a name="task2"></a>

## Creating your Azure Subscription

1. Create your azure Subscription

___

<a name="task3"></a>

## Installing the Azure Command-Line Interface (Azure CLI)

The Azure-CLI is a cross platform command line interface that you can use to manage resources in your Azure Subscription from your local workstation.  The Azure-CLI is a Nodejs application and as such runs on Windows, Linux and Mac OS X. It's for that reason specifically that we have chosen it as the toolset for this lab.

1. Ensure that you have Nodejs v6.9.4 or later installed.  If you don't you can install it from [https://nodejs.org/en/download/](https://nodejs.org/en/download/).

1. From your system's command prompt or terminal window, issue the following command:

    > **Note**: You can alternatively use an installer if you are on Windows or Mac OS X.  To find out more about using an installer, view [Option 2: Use an installer](https://docs.microsoft.com/en-us/azure/xplat-cli-install#option-2-use-an-installer) on the [Install the Azure CLI](https://docs.microsoft.com/en-us/azure/xplat-cli-install) page in the Azure documentation.

    ```bash
    npm i -g azure-cli
    ```
    On OS X and Linux systems, you may need to use `sudo` before the command.

    ```bash
    sudo npm i -g azure-cli
    ```
___

<a name="task4"></a>

## Logging into your Azure Subscription via the Azure-CLI

In this steps, you'll login to your Azure subscription from your workstations command line.  There are multiple ways to login to the Azure-CLI.  You can learn about alternat login methods here: [Log in to Azure from the Azure CLI](https://docs.microsoft.com/en-us/azure/xplat-cli-connect) 

We'll be using the "**Azure login with interactive login**" method:

1.  From your system's command prompt or terminal, enter the following command to set the azure-cli into "Azure Resource Manager" mode (ARM):

    > **Note**: The first time you use the azure-cli you will likely see a prompt that starts with "`Microsoft Azure CLI would like to collect data about how users use CLI
commands and some problems they encounter...`", asking you to participate in azure-cli data collection.  You can accept or decline as you wish, it won't impact how the cli functions. 

    ```bash
    azure config mode arm
    ```

1. Next, to login to your Azure Subscription from the azure-cli, issue:

    ```bash
    azure login
    ```

1. The output should be something similar to the following:

    ```bash
    info:    Executing command login
    info:    To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the code XXXXXXXXX to authenticate.
    ```
1. As instructed, copy the `XXXXXXXXX` code from the info message, open your browser, and navigate to the [http://aka.ms/devicelogin](http://aka.ms/devicelogin) site to authenticate:

    - Paste the `XXXXXXXXX` code copied from above into the box, then click "**Continue**":

        ![Device Login Code](images/01010-DeviceLoginCode.png)

    - Then authenticate with the credentials for your Azure Subscription

        ![Azure Credentials](images/01020-AzureCredentials.png)

    - Back at the command prompt, you should get a login confirmation similar to the following:

        ```bash
        info:    Added subscription <Your Subscription Name>
        info:    Setting subscription "<Your Subscription Name>" as default
        info:    login command OK
        ```

1. If you only have a single azure subscription associated with the credentials you used above, then that subscription should be the current subscription.  However, if you have more than one subscription or if you want to just ensure the proper subscription is being used, follow these steps:

    - From the command prompt, or terminal window enter the following azure-cli command to get a list of the susbscriptions associated with your login:

        ```bash
        azure account list
        ```

    - You should get a result similar to the following:

        ```bash
        $ azure account list
        info:    Executing command account list
        data:    Name      Id                                    Current  State
        data:    --------  ------------------------------------  -------  -------
        data:    YourSub   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  true     Enabled
        info:    account list command OK
        ```

    - If more than one subscription is listed above, you need to ensure that the subscription you wish to used is set as the "Current" subscription.  To do so, use the following azure-cli command:

        ```bash
        azure account set <Your Subscription Name or Subscription Id>
        ```

    - For example, if we use the sample data above, notice the subscription name is `YourSub`.  We could then use this command to ensure that the `YourSub` subscription was the current subscription used by the azure-cli:

        ```bash
        azure account set YourSub
        ```
    - Finally, to get the details of the current subscription, you can enter the following command:

        ```bash
        azure account show
        ```

    - The `azure account show` returns results similar to:

        ```bash
        info:    Executing command account show
        data:    Name                        : YourSub
        data:    ID                          : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        data:    State                       : Enabled
        data:    Tenant ID                   : yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy
        data:    Is Default                  : true
        data:    Environment                 : AzureCloud
        data:    Has Certificate             : No
        data:    Has Access Token            : Yes
        data:    User name                   : youruser@yourdomain.com
        ```
___

<a name="task5"></a>

## Creating an Azure Storage Account, and Container

The Azure Virtual Machine that you will be using for this lab will be based on a copy of a pre-existing Virtual Hard Disk (VHD) that we have created for your use.  The pre-existing VHD has Ubuntu 16.0.4 LTS installed, along with all of the deep learning tools, frameworks, data sets and jupyter notebooks that you will need for the lab.  In this task, you will create an Azure Storage Account, and blob container that will hold your copy of the VHD.

1. First, to create your Resource Group, from your system's command prompt or terminal window, issue the following command (where `dlirwxxxgroup` is the resource group name as determined above):

    ```bash
    azure group create dlirwxxxgroup --location "SouthCentralUS"
    ```

1. The output should look something similar to:

    ```bash
    info:    Executing command group create
    + Getting resource group dlirwxxxgroup
    + Creating resource group dlirwxxxgroup
    info:    Created resource group dlirwxxxgroup
    data:    Id:                  /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/dlirwxxxgroup
    data:    Name:                dlirwxxxgroup
    data:    Location:            southcentralus
    data:    Provisioning State:  Succeeded
    data:    Tags: null
    data:
    info:    group create command OK
    ```

1. Next, create the Azure Storage Account within your new resource group, making sure again to use the South Central US location.  In the following command replace `dlirwxxxgroup` and `dlirwxxxstorage` with the resource group and storage account names determined above:

    > **Note**: This command may take thirty seconds or longer to execute

    ```bash
    azure storage account create dlirwxxxstorage --resource-group dlirwxxxgroup --location "SouthCentralUS" --kind Storage --sku-name PLRS
    ```

1. Now that you have a storage account, we need to retrieve the key needed to manage it.  Use the following command, again replacing `dlirwxxx...` with appropriate values from above:

    ```bash
    azure storage account keys list dlirwxxxstorage --resource-group dlirwxxxgroup
    ```

1. From the output, make a note of the `key1` value returned:

    ```bash
    info:    Executing command storage account keys list
    + Getting storage account keys
    data:    Name  Key                                                                                       Permissions
    data:    ----  ----------------------------------------------------------------------------------------  -----------
    data:    key1  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==  Full
    data:    key2  yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy==  Full
    info:    storage account keys list command OK
    ```

1. Next, we'll create the container to store the vhd for our virtual machine:

    ```bash
    azure storage container create \
    --account-name dlirwxxxstorage \
    --account-key xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx== \
    --container vhds
    ```

1.  The output should resemble the following:

    ```bash
    info:    Executing command storage container create
    + Creating storage container vhds
    + Getting storage container information
    data:    {
    data:        name: 'vhds',
    data:        metadata: {},
    data:        etag: '"0x8D43B5BF7376395"',
    data:        lastModified: 'Fri, 13 Jan 2017 02:29:14 GMT',
    data:        lease: { status: 'unlocked', state: 'available' },
    data:        requestId: 'ade684b0-001c-0025-7f44-6d0f07000000',
    data:        publicAccessLevel: 'Off'
    data:    }
    info:    storage container create command OK
    ```
___

<a name="task6"></a>

## Copying the Virtual Hard Disk (VHD) for the Virtual Machine

Now that we have the Azure Resource Group, Storage Account and Blob Container created, we can now copy the pre-existing VHD provided for this workshop.  To copy the original VHD, you will need the following values:

| Token | Description | Value |
| --- | --- | --- | 
| <nobr>source-sas</nobr> | The Shared Access Signature (SAS) key needed to gain access to the source URL | `sv=2015-12-11&ss=b&srt=sco&sp=rl&se=2050-01-13T02:18:26Z&st=2017-01-12T18:18:26Z&spr=https,http&sig=TGEmNmml7PXu90db5zIbA%2BUXHEOrY9XZ6dI7avV34ew%3D` |
| <nobr>source-uri</nobr> | The URL (uri) that points to the source VHD             | `https://nvidiavmstorage.blob.core.windows.net/vhds/nvidiavm20170104130104.vhd` |
| <nobr>dest-account-name</nobr> | The name of the azure storage account you created above | `dlirwxxxstorage` |
| <nobr>dest-account-key</nobr> | The primary access key (key1) for the storage account you created above | `xxx...xxx==` |
| <nobr>dest-container</nobr> | The name of the container you created above to store the copy of the VHD | `vhds` |
| <nobr>blob</nobr> | The name of the vhd blob itself.  You'll need this when monitoring the status of the copy. | `nvidiavm20170104130104.vhd` |


1. To copy the pre-existing VHD from the hosted storage account into the container you just created, use the `azure storage blob copy start` command with the values from the table above:

    > **Note**: This is ONE command.  It is shown here wrapped across multiple lines but you will need to copy and paste this command into a text editor, replace the `dest-account-key` and `dest-account-name` place holders with your actual values, then copy and paste that completed single line syntax into your command prompt or terminal:

    ```bash
    azure storage blob copy start \
        --source-uri "https://nvidiavmstorage.blob.core.windows.net/vhds/nvidiavm20170104130104.vhd" \
        --source-sas "sv=2015-12-11&ss=b&srt=sco&sp=rl&se=2050-01-13T02:18:26Z&st=2017-01-12T18:18:26Z&spr=https,http&sig=TGEmNmml7PXu90db5zIbA%2BUXHEOrY9XZ6dI7avV34ew%3D" \
        --dest-account-name "dlirwxxxstorage" \
        --dest-account-key "TfjYbT1Kj80bfslEi3Wvep4PoNEu6OooVghDTSB0295x2xdydk4k9FzB03UQPUSZvYATMBgaRKJSBncMKHbRtA==" \
        --dest-container "vhds"
    ```

1.  The command should return output similar to the following:

    ```bash
    info:    Executing command storage blob copy start
    - Start copying blob https://nvidiavmstorage.blob.core.windows.net/vhds/nvidiavm20170104130104.vhd?sv=2015-12-11&ss=b&srt=sco&sp=rl&se=2050-01-13T02:18:26+&st=2017-01-12T18:18:26Z&spr=https,http&sig=TGEmNmml7PXu90db5zIbA%2BUXHEOrY9XZ6dI7avV34ew%3D
    data:    Copy ID                               Status
    data:    ------------------------------------  -------
    data:    a8d4752a-b2e2-4510-9f55-3b11805d44ea  pending
    info:    storage blob copy start command OK

    ```
1. The copy will take up to 20 minutes or so, you can monitor the progress by repeatedly issuing the following command:

    ```bash
    azure storage blob copy show --account-name dlirwxxxstorage --account-key "TfjYbT1Kj80bfslEi3Wvep4PoNEu6OooVghDTSB0295x2xdydk4k9FzB03UQPUSZvYATMBgaRKJSBncMKHbRtA==" --container "vhds" --blob "nvidiavm20170104130104.vhd"
    ```

1. The output of the command above shows the copy status in the `Progress` and `Status` columns.  

    > **Note**: in the example shown below, the `Progress` value of `14144983040/31457280512` means that 14,144,983,040 bytes (13.17GB) of 31457280512 (29.27GB) have been transferred, or in otherwords the copy is about 45% complete.  The `Status` column shows `pending` to indicate the copy is still in progress.

    ```bash
    info:    Executing command storage blob copy show
    + Getting storage blob information
    data:    Copy ID                               Progress                 Status
    data:    ------------------------------------  -----------------------  -------
    data:    a8d4752a-b2e2-4510-9f55-3b11805d44ea  14144983040/31457280512  pending
    info:    storage blob copy show command OK
    ```

1. Contiune to monitor the status of the copy by repeating the `azure storage blob copy show...` command above until the `Status` reads `success`:

    ```bash
    info:    Executing command storage blob copy show
    + Getting storage blob information
    data:    Copy ID                               Progress                 Status
    data:    ------------------------------------  -----------------------  -------
    data:    a8d4752a-b2e2-4510-9f55-3b11805d44ea  31457280512/31457280512  success
    info:    storage blob copy show command OK
    ```
___

<a name="task7"></a>

## Creating the Virtual Machine using the VHD

azure group deployment create --name vmdeployment --resource-group dlirwxxxgroup --template-file template.json --parameters-file parameters.json

___

<a name="task8"></a>

## Configuring your Virtual Machine Firewall

___

<a name="task9"></a>

## Connecting to your Virtual Machine using SSH

