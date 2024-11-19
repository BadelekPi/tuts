KVM - feature of the Linux Kernel act as a type 1 hypervisor to run virtual machines
allows to use the host's processor directly instead of relying on emulation
MAC OS: Hypervisor Framework
Windows: HyperV
KVM with QEMU
KVM is available on AMD, Intel systems whose support virtualization (AMD-V / VT-x)

-.-.-.-.-.-.-

check whether the vitualization is avaiable:
ls /dev/kvm
or
lsmod | grep kvm

install qemu:
apt list qemu*
sudo apt install qemu-kvm

-.-.-.-.-.-.-

Create QCOW image
qemu-img create -f qcow2 disk1.qcow2 1G

Create guest
qemu-system-x86_64 -enable-kvm -cpu host -smp 4 -m 4G -k en-us -vnc :0 -usbdevice tablet -drive file=disk1.qcow2,if=virtio -cdrom ubuntu-22.04.1-desktop-amd64.iso -boot d

After installation, execute above command without -cdrom and -boot flags

-.-.-.-.-.-.-

To see what CPU and what VM it is, execute:
lscpu / hostnamectl commands
lspci - show emulated PCI devices
lsusb - show what devices you have
lsmem - how many memory

-.-.-.-.-.-.-

Start a guest with the QEMU Monitor available for control and troubleshooting
To above command which executes guest, add flag:
-monitor stdio

Update the path to the backing image:
qemu-img rebase -b /newpath/backing.qcow2 overlay.qcow2

View disk image information
qemu-img info diskimage.qcow2

Resized disk images
qemu-img resize +50G disk.qcow2

-.-.-.-.-.-.-

Qemu-nbd utility attaches a disk image to host as a network block device
Check if nbd kernel module is loaded
sudo modprobe nbd

sudo qemu-nbd --connect=/dev/nbd0 /home/path_to_disk_image.qcow2

See block device:
lsblk -f /dev/nbd*

mount disk partition
sudo mkdir /mnt/mydisk
Then it is possible to work with this partition the same way as it be a normal disk
Unmount this disk
sudo umount /mnt/mydisk
Detach disk image from the device, created for it
sudo qemu-nbd -d /dev/nbd0

-.-.-.-.-.-.-

Control graphics output with the -display and -vga options
-vga determines what video adapter is used
- without any options defining the display or the video adapter, the guest on the Linux host will start up a GTK/GNOME ToolKit window, and a standard VGA adapter
While create a guest, it is -display flag:
-vnc :0  # shortcut for -display vnc=:0
- none  # attaches no display to the guest
- curses  # present a guest a text-based console display
- vnc  # present a guest's display through VNC server
- sdl # simple DirectMedia Layer (local graphical window)
- gtk # GNOME ToolKit (default option) 
    gtk and sdl can include ,gl=on # OpenGL support

Flag -vga # Video Graphics Adapter, parameters:
    std # Standard VGA
    virtio # Use paravirtualization for better performance
    
Best performance propably:
qemu-system-x86_64 -enable-kvm -cpu host -smp 4 -m 4G -k en-us -usbdevice tablet -drive file=disk1.qcow2 -display sdl -vga virtio -monitor stdio


-.-.-.-.-.-.-

Share files between host and guest
qemu-system-x86_64 -enable-kvm -cpu host -smp 4 -m 4G -k en-us -usbdevice tablet -drive file=disk1.qcow2 -display sdl -vga virtio -monitor stdio -virtfs local,path=/home/badelekpi/Documents/tuts/qemu-kvm/shared,mount_tag=shared,security_model=mapped

Then in guest create a local mount point for shared resource
sudo mount -t 9p -o trans=virtio shared /home/badelekpi/shared -o version=9p2000.L

-.-.-.-.-.-.-

Using a Host's Hardware in a Guest
qemu-system-x86_64 -enable-kvm -cpu host -smp 4 -m 4G -k en-us -usbdevice tablet -drive file=disk1.qcow2 -display sdl -vga virtio -device qemu-xhci,id=xhci -device usb-host,bus=xhci.0,vendorid=0x046d,productid=0x0843

Execute lsusb command:
lsusb

Attach a device by its vendor and product IDs to the guest
-device usb-host,bus=xhci.0,vendorid=0x046d,productid=0x0843

Attach a host USB port (and whatever is plugged into it) to the guest
-device usb-host,bus=xhci.0,hostbus=1,hostport=5

(use superuser priviliges to run the command)

-.-.-.-.-.-.-

Networking

By default: The host creates the private NAT network for the guest and handles routing to its network and beyond. When you create another guest, another NAT network will be create. Without additional configuration, our two guests wont be able to communicate with each other.

-netdev option
Sets up the network back end, assign and ID so the device can associate with it

-device option
Add a network device to the guest, set its model, associate it with a netdev ID

qemu-system-x86_64 \
-enable-kvm -cpu host -smp 4 -m 4G \
-k en-us -usbdevice tablet \
-drive file=disk1.qcow2 -display sdl -vga virtio \
-netdev user,ipv6=off,id=net0 \
-device rtl8139,netdev=net0

For info about supported devices:
qemu-system-x86_64 -device help


-nic option
Is newer and combines elements from -netdev and -device into one option
for example: -nic user,model=virtio-net-pci


Port forwarding in User Mode
# The general pattern
-nic user,hostfwd=protocol:hostaddr:hostport-guestaddr:guessport

qemu-system-x86_64 \
-enable-kvm -cpu host -smp 4 -m 4G \
-k en-us -usbdevice tablet \
-drive file=disk1.qcow2 -display sdl -vga virtio \
-nic user,hostfwd=::2222-:22,hostfwd=::8080-:80

On guest install
sudo apt update
sudo apt install openssh-server apache2

ssh badelekpi@localhost -oPort=2222


# Disable network connectivity on guest
-nic none


# Network bridges
Allows two devices or networks to communicate each other
In Linux is possible to create virtual bridge on host
Guest network adapters are represented as TAPs on the host

# Private Bridges Network
- guests can connect to each other with manual addresses
- provide DHCP and other services
- can set up routing on the host to create a NAT network

# Public Bridged Network
- add a host Ethernet adapter to the bridge
- guest behave as though they were members of the host's network

# Set up a bridge on the host - firstly
Bridge device is completely separate from QEMU

sudo ip link add br0 type bridge
sudo ip link set br0 up

# Bridges Network: Bridge Helper

configure to execute without sudo:
sudo chmod u+s /usr/lib/qemu/qemu-bridge-helper

create configuration file
sudo mkdir /etc/qemu/
sudo vim /etc/qemu/bridge.conf

inside file:
    allow br0

# Private Bridged Networking

qemu-system-x86_64 \
-enable-kvm -cpu host -smp 4 -m 4G \
-k en-us -usbdevice tablet \
-drive file=disk1.qcow2 -display sdl -vga virtio \
-netdev bridge,br=br0,id=net1 \
-device virtio-net,netdev=net1

# Mac Address Conflicts
QEMU assigns each guests the same MAC address

Use unique MAC address:
-nic bridge,br=br0,mac=52:54:00:12:34:57,model=virtio-net-pci

# Bridged Networking: Host Only - network architecture
Add the address to the bridge called br0

sudo ip addr add 10.10.10.1/24 dev br0

- the host participates in the private network
- does not allow guest to access its network or the internet

# Provide a DHCP server only on the bridge interface
sudo dnsmasq --interface=br0 --bind-interfaces --dhcp-range=10.10.10.2,10.10.10.100

# Create NAT network - network architecture

- on the host, tell to forward packets, by setting the kernel parameter for ipv4 forwardingsudo sysctl -w net.ipv4.ip_forward=1

- accept and forward traffic from the bridge
sudo iptables -A FORWARD -i br0 -j ACCEPT

- configure NAT from the bridge's address out to the rest of the host's network and to the world
sudo iptables -t nat -I POSTROUTING -s 10.10.10.1/24 -j MASQUERADE

# Create Public Virtual Bridge - network architecture
this allows guests to participate in the host's network as though they were any other member of that network

sudo ip link add br0 type bridge
sudo ip link set br0 up
sudo ip link set eno1 master br0

qemu-system-x86_64 \
-enable-kvm -cpu host -smp 4 -m 4G \
-k en-us -usbdevice tablet \
-drive file=disk1.qcow2 -display sdl -vga virtio \
-netdev bridge,br=br0,id=net1 \
-device virtio-net,netdev=net1

-.-.-.-.-.-.-

# Libvirt

sudo apt install libvirt-daemon-system libvirt-clients

- stores a configuration files in /etc/libvirt/qemu
- managing NAT, storeges, handle communicaton QEMU

# Virt-Manager
sudo apt install virt-manager


