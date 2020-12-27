# AutoCarryRobot

## Usage

A demo based on "zhiyuansu" robot platform. The functions include using mobile app to control robot combat and implement robot automatic transportation in a given area.

## Code structure

### Auto Move
- `Auto_Move_Final.py`: main function
- `color_detector.py`: contains code for color detector(red, green or yellow)
- `face_detector.py`: face detector based on baidu API
- `Movement.py`: control robot movement
- `robotpi_Cmd.py` `Server.py` `robotpi_serOp.py`: communication with stm32
- `WaveModule.py`: use ultrasonic module

### APP Control Module

- easy control
