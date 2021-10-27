# BertheletteProject

![BertheletteMarkI](https://raw.githubusercontent.com/lucblender/BertheletteProject/master/Ressources/Berthelette%20concept_whitebg.png)

## Description

Berthelette Mark I is a strong 6DOF robot arm made with normal nema 17 stepper motor from your casual 3d printer and 3d printed part. Everything is 3D printed except the screws and a 3 ball bearing.


<img src="https://raw.githubusercontent.com/lucblender/BertheletteProject/master/Ressources/BertheletteID.png" height="500">

The brain of Berthelette is a Raspberry Pi 4. This Raspberry drive 4 stepper motor driver and up to 3 servo motors for the different claws. A little custom PCB helps bringing GPIOs up the claw helps Berthelette to be modular and claws to be changed easily. The whole arm is remote controlled with blender. The arm is re-modeled and rigged with inverse kinematic. A sequence of movements can be made in blender and then reproduced by the arm!

Each stepper motor is coupled to a gearbox made of two coupled planetary gear system. The reduction factor goes from 1:49 to 1:63 for the strongest motor. The arm successfully lift up a 1.5kg drill.

Berthelette as been made as part of the helixbyte project. More to see on the [helixbyte Instagram](https://www.instagram.com/helixbyte/).

## Status of this git 

Done:

- Published Controller code
- Published Blender plugin code
- Added reference of components used in the autoclamp system

To do:

- Publish blender file
- Publish 3D files to build Berthelette Mark I 
- Publish Gerber of PCBs

## Index

- The Controller code (Raspberry Pi) is under the [Raspberry Controller](https://github.com/lucblender/BertheletteProject/tree/master/Raspberry%20Controller) folder.
- The Blender pluggin code is under the [Blender Plugin](https://github.com/lucblender/BertheletteProject/tree/master/Blender%20Plugin) folder.


## Requirement

### Controller side (Raspberry Pi)

The arm use raspberry pi GPIO to control the motor driver and servo motor. To do so the RPi.GPIO lib is used. And the arm expose a simple Flask server for remote control with blender.

```pip3 install Flask```

```pip3 install RPi.GPIO```

### Material

#### General

Berthelette has been tested with a Raspberry Pi 4 4GB. It has not been tested with less powerfull model.

The motor driver are the VMA333 because that's what I had in stock. They are not the best at all. Any stepper motor driver with Enable, Step and Dir signal will work. The A4988 have been tested too and are proved to work with the code.

#### Auto clamp system

| Description                            | Reseller   | Reference                                                                                                     | Qty |
|----------------------------------------|------------|---------------------------------------------------------------------------------------------------------------|-----|
| 5V Solenoids                           | AliExpress | [Aliexpress Link](https://www.aliexpress.com/item/4000807560712.html?spm=a2g0s.9042311.0.0.3aec4c4djkiW06)    | 4   |
| Magnetic Connectors Male  6 pins       | AliExpress | [Aliexpress Link](https://www.aliexpress.com/item/1005002669709542.html?spm=a2g0s.9042311.0.0.3aec4c4djkiW06) | 1   |
| Magnetic Connectors Female 6 pins      | AliExpress | [Aliexpress Link](https://www.aliexpress.com/item/1005002669709542.html?spm=a2g0s.9042311.0.0.3aec4c4djkiW06) |     |
| Solenoid Driver PCB                    | PCBWay     | TODO ADD GERBER                                                                                               | 1   |
| Slip Ring PCB                          | PCBWay     | TODO ADD GERBER                                                                                               | 1   |
| Spring connectors  (For slip ring pcb) | AliExpress | [Aliexpress Link](https://www.aliexpress.com/item/4000282372452.html?spm=a2g0s.9042311.0.0.3aec4c4djkiW06)    | 4   |

## License

All files included in this repository are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/) 

![license_picture](https://licensebuttons.net/l/by-sa/3.0/88x31.png)
