# Preparing the Source VHD Image

See [Capture a Linux virtual machine running on Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-linux-capture-image) for more info.

1. Get a VM setup the way you want it. 
1. ***MAKE SURE THAT THERE IS NOTHING IN THE USER'S "/home" FOLDER THAT NEEDS TO BE PERSISTED.  THE USER'S FOLDER WILL BE WIPED OUT DURING GENERALIZATION!!!!!!***

1. While ssh'd into the VM, run.  This will get the machine ready for imaging and wipe out the user data, etc.:

    ```bash
    sudo /usr/sbin/waagent -force -deprovision+user && export HISTSIZE=0 && sync
    ```

    you should see output similar to:

    ```bash
    WARNING! The waagent service will be stopped.
    WARNING! Cached DHCP leases will be deleted.
    WARNING! root password will be disabled. You will not be able to login as root.
    WARNING! /etc/resolvconf/resolv.conf.d/tail and /etc/resolvconf/resolv.conf.d/original will be deleted.
    WARNING! dliuser account and entire home directory will be deleted.
    ```

1. Disconnect from ssh


1. Back on your workstation, run:

    ```bash
    azure vm deallocate -g <name>group -n <name>vm
    ```

1. Followed by

    ```bash
    azure vm generalize -g <name>group -n <name>vm
    ```

1. And finally (where `<name>vximage` is some name you want to use as a prefix to the image file created, for example `dli2010v3image`, and `<name>vxtemplate.json` is the name you want to use for the output template, for example `dli0201v3template`, although you don't really need the template:

    ```bash
    azure vm capture -g <name>group -n <name>vm -p <name>vximage -t <name>vxtemplate.json
    ```

1. Once the capture is complete, Use the Azure Storage Explorer, and connect to the container where the source VM's vhd was.  You should now see a new container off the root of the same storage account as the source VHD:

    ```bash
    <storageaccount>/system/Microsoft.Compute/Images/vhds
    ```

1. And then in there, is the vhd with the image in it.  It should have a file name that starts with the image name prefix you specified above (`<name>vximage`) and some longer funky name after that.  For example:

    ```bash
    dli0201v3image-osDisk.fe5e2322-a6c8-45e1-9160-10d731d6fd42.vhd
    ```

1. Use storage explorer (or whatever) to copy that image vhd to the storage account and container where you want to host the source image for attendees to copy. 

1. Get a new Shared Access Signature (storage explorer is a handy way to to do that) for the blob, and update the docs with the new SAS value.  


