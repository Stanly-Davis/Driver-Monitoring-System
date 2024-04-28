# Driver Monitoring System

This project detects drowsiness and yawn of truck drivers through camera. The image of sleepy driver (closed eye) is saved and kept as a reference to show it to the truck owner. It also detects for alcohol/smoke. If an accident takes place, alert and GPS coordinates are sent as SMS to concerned authority/owner.

This project is just an additional feature to the already existing drowsiness detection system.



## Motivation


In the existing system, truck driver is truck/car/bus driver is alerted immediately whenever he is drowsy.

Many methods like using IR sensor, Night vision camera, optimized algorithms are used to detect if driver is closing the eye.

If the driver is alerted whenever he closes his eye, he might get a bit cautious and alert, but there is chance that he will feel drowsy again and again. Hence the alarm will ring again and again. This happens mostly with truck drivers who drive for long distance. But if we capture the photos of the driver when he is sleeping and then if it is shown to the truck/vehicle owner. The owner can clearly understand from the photos that driver was drowsy and still kept driving the truck. The owner has proof and he can warn the driver to avoid it. The photos can also be taken if smoke is detected in the cabin (This implies driver was smoking)

By placing this system in all the trucks, the owner can find out good drivers and bad drivers (drowsy driver)

Hence, drowsy drivers can be replaced with good drivers or drowsy drivers can be assigned short distance.

This method will make sure only the best drivers will be given long, dangerous and accident-prone route. Thus, the probability of accident decreases.

This project/method is just an additional feature to the already existing drowsiness detection system. 


## Components

1. Raspberry Pi 3B+
2. Raspberry Pi camera module
3. Sim 800A (GSM Module to send SMS)
4. Arduino UNO Rev 3
5. MQ2 Sensor (smoke/Alcohol Detection)
6. SW-18010P (Collision Detection)
7. NEO-6M (GPS Module)
8. Buzzer


## Circuit

![Circuit](https://github.com/Stanly-Davis/Driver-Monitoring-System/blob/main/Images/Circuit.png)

## Model

![Model](https://github.com/Stanly-Davis/Driver-Monitoring-System/blob/main/Images/DrowsyDetect.png)

![Model](https://github.com/Stanly-Davis/Driver-Monitoring-System/blob/main/Images/Arduino_MQ2_SW_GPS_GSM.png)

## Code


Drowsiness detection and Gmail alert is done through Raspberry pi.

Alcohol/smoke detection, accident detection and SMS alert is done by Arduino


### Setting up Raspberry Pi 

        Model: Raspberry Pi 3B+ 
        Operating System: Raspberry Pi OS (32 bit)
        Debian Version: 11 (bullseye)
        Kernel: Linux 5.15.84-v7+
        RAM: 1GB

Library files required:

        dlib
        cv2
        scipy
        imutils
        numpy
        argparse
        time
        reportlab
        smtplib
        email
        imghdr

Installing cv2(OpenCV) and dlib will be challenging if you have low RAM memory. 

Since I used Raspberry Pi 3B+ which is an old model which had only 1GB RAM, installation of cv2 and dlib was crashing or unsuccessful. 

If you are using Raspberry Pi 4 or above version with higher RAM memory, then the installation of these 2 libraries is easy. 

### Virtual environment:

Creating a virtual environment and installing all the modules/Libraries to this environment will be a very organized approach. But I have not made use of virtual environment since it was a one-time project and I dint use Raspberry pi 3 after that.

If you plan to use different versions of Modules/Libraries for different project, virtual environment is a must.


### Library installation

1. cv2(OpenCV installation)

        $ sudo apt update
        $ sudo apt upgrade
        $ sudo apt install python3-opencv

This process took 15-20 mins. It might vary in other systems.
Verify if the library is installed.

If not installed, you can follow the below tutorial

https://raspberrytips.com/install-opencv-on-raspberry-pi/



2. dlib installation

If your Raspberry Pi has good processor and above 4GB RAM, you can follow below steps

        $ sudo apt-get install build-essential cmake
        $ sudo apt-get install libgtk-3-dev
        $ sudo apt-get install libboost-all-dev

Using Pip to install – make sure Pip module is already installed. If not install pip module

        $ pip install numpy
        $ pip install scipy
        $ pip install scikit-image
Installing dlib

        $ sudo pip install dlib

Dlib will be installed.


If your Raspberry Pi has 1 GB RAM and is slow, dlib installation might fail.
There are few methods to work around this:

1.	Increase swap file size
Some space of SD card/USB drive/Flash memory/ROM will be used as RAM. This increases size of RAM.

2.	Changing Boot options
The graphical interface of the OS can be changed to Command line interface 

3.	Updating memory Split
Reduce the memory allocated to onboard GPU.

After following these steps, Raspberry should be restarted 

All these 3 steps are clearly explained in the below tutorial of py_image_search website.

Please refer the below link.

https://pyimagesearch.com/2017/05/01/install-dlib-raspberry-pi/


After performing the 3 steps, you can go ahead with the same commands

        $ sudo apt-get install build-essential cmake
        $ sudo apt-get install libgtk-3-dev
        $ sudo apt-get install libboost-all-dev

        $ pip install numpy
        $ pip install scipy
        $ pip install scikit-image
        $ sudo pip install dlib

dlib will be installed.


After the installation of dlib, verify if the library is properly installed.

Then the remaining library file can be installed using pip command

        imutils
        argparse
        time
        reportlab
        smtplib
        email
        imghdr


Once all this is done, open Thonny editor or any other coding editor and then run the code.


### Setting up Arduino Uno

1. GSM module
   
Sim800A is easy to use. It works well when we insert a 4G Airtel Sim. 3G sim dint work with this model.

Library file needed: SoftwareSerial.h

2. GPS module
   

NEO-6M has low accuracy. It works good only at open place like terrace or ground. Many approaches can be taken to increase the accuracy of the GPS module.

Library file needed: TinyGPS++.h

3. Library files needed for Arduino:

        SoftwareSerial.h
        TinyGPS++.h


Once this libraries are installed, the final code can be flashed to Arduino



## Future Scope

In this project, only photo of drowsy drivers is sent as mail to the truck owner.

For fleet management, if a separate online portal is made for each driver, and the Photos of drowsy driver, smoking of driver and many more data can be stored. 

Data analysis can be performed on these data. Predictions can be made.

Drivers can be ranked accordingly.
