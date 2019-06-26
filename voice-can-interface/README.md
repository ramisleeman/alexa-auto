(UNDER CONSTRUCTION)

# alexa-can-interface



## Introduction
This sample demo, illustrates a simple example of voice to [CAN](https://www.sae.org/standards/content/j2411_200002/) and CAN to voice implemention using Alexa and a Raspberry Pi 3. The demo can be imppelmneted with around $100.

Specifically, the demo presented here illustrates the use of Alexa along with a Raspberry Pi 3 that are used to read the OBD (On Board Diagnostic) of a vehicle.

<br />
![alt text](Resources/HL.png)
<br />


## Parts needed
1. **OBD-II Male Connector.** Buy here: [Amazon Link](https://www.amazon.com/gp/product/B07F1887MB/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)

   NOTE: Some buyers complained that the color mapping doesn't match the PIN Assignment, make sure to double check before connecting the cables

   

2. **Raspberry Pi 3.** Buy here: [Amazon Link](https://www.amazon.com/Raspberry-Pi-MS-004-00000024-Model-Board/dp/B01LPLPBS8/)

   NOTE: Check out Raspberry Pi 4 that was just recently released: [Link](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)

   

3. **PiCAN2 Duo CAN-Bus Board for Raspberry Pi 2/3 With SMPS** Buy here: [Link](https://copperhilltech.com/pican2-duo-can-bus-board-for-raspberry-pi-2-3-with-smps/)

   NOTE: A cheaper CAN to Raspberry Pi is available ([Link](https://copperhilltech.com/pican2-duo-can-bus-board-for-raspberry-pi-2-3/)), but you'll need to power the Pi from an external source which is not ideal for this demo as the goal is to power the system from the vehicle's OBD port.

   
## OBD-II Introduction

[SAE J1962](https://www.sae.org/standards/content/j1962_201207/) defines the OBD-II standard that specifies the functional requirements for the vehicle connector. Such as connector location/access, connector design, connector contact allocation, etc. For this demo we will be reading PID (Parameter IDs) codes that defines the communication between the vehicles' OBD system and the test equipment. [SAE J1979](https://www.sae.org/standards/content/j1979_201702/) is the SAE standard that defines this communication protocol.

The Raspberry Pi setup in this demo is the *test equipment*. It's role is to read the PIDs and report back through voice the status of these PID as well as the status of the DTCs (Diagnostic Trouble Code).





