sudo apt update -y
sudo apt upgrade -y
sudo apt install open-vm-tools-desktop -y
sudo apt install traceroute -y
sudo apt install wireshark -y
sudo dpkg-reconfigure wireshark-common
sudo usermod -a -G wireshark $USER
newgrp wireshark
