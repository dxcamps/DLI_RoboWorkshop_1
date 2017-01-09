# Deep Learning Institute Robot Workshop Pre-Requiste Lab

In this lab, we'll walk workshop attendees through the required pre-requisite steps.  At the completion of this lab, attendees should have a properly prepared Virtual Machine running in Azure that has the NVidia GPUs, and lab assets needed for successful completion of the workshop.

<a name="prereqs"></a>

## Pre-Requisites

To complete this lab, you will need to have the following items:

1. An active azure subscription that you are willing to use for the lab.  ***BE AWARE** the lab has you create N-Series VMs in Azure.  These VMs are special because they include NVidia GPU support and provide an extremely powerful environment for deep learning projects.  However, they are expensive when compared to other less capable VMs.  It is recommended that you use a trial subscription, or a subscription provided to you at a live event for the lab steps.  This will help to ensure that you are not billed for excessive VM utilization.
1. Nodejs v6.9.4 or later. You can download the current version of Nodejs from [https://nodejs.org/en/download/](https://nodejs.org/en/download/)

___

<a name="tasks"></a>

## Tasks

In this lab, you will complete the following tasks:

1. [Creating your Azure Subscription](#task1)
1. [Installing the Azure Command-Line Interface (Azure CLI)](#task2)
1. [Logging into your Azure Subscription via the Azure-CLI](#task3)
1. [Creating an Azure Storage Account, and Container](#task4)
1. [Copying the Virtual Hard Disk (VHD) for the Virtual Machine](#task5)
1. [Creating the Virtual Machine using the VHD](#task6)
1. [Configuring your Virtual Machine Firewall](#task7)
1. [Connecting to your Virtual Machine using SSH](#task8)

___

<a name="task1"></a>

## Creating your Azure Subscription


1. Create your azure Subscription

___

<a name="task2"></a>

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

<a name="task3"></a>

## Logging into your Azure Subscription via the Azure-CLI



___

<a name="task4"></a>

## Creating an Azure Storage Account, and Container

___

<a name="task5"></a>

## Copying the Virtual Hard Disk (VHD) for the Virtual Machine

___

<a name="task6"></a>

## Creating the Virtual Machine using the VHD

___

<a name="task7"></a>

## Configuring your Virtual Machine Firewall

___

<a name="task8"></a>

## Connecting to your Virtual Machine using SSH




