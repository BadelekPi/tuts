Add user to virtualbox group:
sudo gpasswd -a badelekpi vboxusers

[Enterprise Linux] Mandatory access system control SELinux
sudo setsebool -P use_virtualbox 1

# Install necessary modules for Secure Boot enabled system:
sudo apt install virtualbox-ext-pack
sudo apt install virtualbox-dkms
sudo apt install linux-headers-generic

# Disable Secure Boot to use Virtual Box !

# Install additional guest tools - for smoother performance
sudo dnf update -y
sudo reboot now
sudo dnf group install -y "Development tools"
sudo dnf install -y elfutils-libelf-devel   # develop means source code package

# Saving snapshots
right ctrl + T

################################################################################
                                    Network
################################################################################
# Internal network
VMs can communicate with eatch other but not with the host

# Host-Only Adapter
VMs can communicate with eatch other and also with the host
This makes it easy to secure copy files into the VMS

File -> Tools -> Host only adapter -> Create

On specified VM manager: settings -> Adapter2 -> Host-only Adapter

Every host is separated, so this have the same ip on enp0s3 

# Network Address Translation
Can communicate with a physical host on the network and the internet
This is not the same thing as a bridge because it doesn't let the physical host on the network access to VMs

