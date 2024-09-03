# triggerdm
triggerdm is a driver for Magic Control Technology Corp. (MCT) USB display IC series in ChromeOS Developer Mode. It is executed in user space and developed based on [EVDI](https://github.com/DisplayLink/evdi) , [libusb](https://libusb.info/) and [turbojpeg](https://github.com/libjpeg-turbo/libjpeg-turbo). Before you build the driver, follow the steps in this [link](https://solarianprogrammer.com/2017/09/13/chrome-os-native-development/) to install the necessary development tools. 

### Build & Installation
1. cd $(your install path)/triggerdm
2. make
3. cp triggerdm /usr/local/sbin
4. sudo /usr/local/sbin/triggerdm &
5. leave virtual terminal mode and plug in usb display adapter with MCT chipset
