# Smart-Cane-Project 
The Project, multimodal that combines computer vision, language processing, and speech recognition to enable users to interact with an AI assistant. The assistant can answer questions, provide location-based information, and generate speech based on the user's input.
**The smart cane project aims to help blind individuals navigate their surroundings independently using advanced technology. The cane integrates sensors, GPS, a camera, and AI to provide real-time obstacle detection and navigation assistance.**

![Smart Cane](https://github.com/Yasmincs2/Smart-Cane-/blob/main/smartCane.png?raw=true)


# -Gitting started- 
 •Library installation .
 
 • **Automatically start a program on Raspberry Pi**
run the command in the terminal 

( _python3 <script file path>_)
( _sudo crontab -e_)
Write down at the bottom of the file ( _@reboot <Your command> &_)
The {@reboot} signifies when it powers on run run this command 
The {&} means keep running all the jobs don’t stop there and only run that command 
Then (Ctrl + S) —> save , (Ctrl + X)—> exit


# 1. Hardware Setup:

 •We connected the Raspberry Pi5 to a portable power source and installed necessary libraries like OpenCV, TensorFlow, and GPSD.

 •We attached ultrasonic sensors, including distance sensors, to the cane and connected them to the GPIO pins on the Raspberry Pi using female-to-female wires as shown in the diagram.

 •We integrated a GPS module into the cane and connected it via UART or USB to the Raspberry Pi.

 •We mounted a camera on the cane and connected it to the camera interface on the Raspberry Pi. 

 •A portable battery powers the entire system.

 # 2.	Software Development:

 •We installed run environment  on the Raspberry Pi and the required libraries.
 
•We developed scripts to collect sensor data and implemented an obstacle alert algorithm.
 
•We developed scripts to process GPS data and implemented geofencing to alert users when they enter or exit predefined safe zones.
 
•We trained and implemented the YOLO model for real-time obstacle detection.

•We implement a pre-trained model for visual questioners answer .
 
•We integrated Google Speech-to-Text for voice commands to enable easy user interaction with GPt-3 API.

# 3. Integration and Testing:

•We integrated the sensors, GPS, camera, and AI models and tested the cane in various environments.
 
•We conducted field tests with users to evaluate performance and gather feedback.

•We achieved 80% on testing yolov8 accuracy.
 
•Based on user feedback, we made adjustments to the design and functionality.
 
# 4. Deployment:

•We finalized the hardware and software setup and provided training sessions for users to familiarize them with the smart cane’s features.
 
•We deployed the smart cane to a broader user base, monitored performance, and made necessary updates.

# 5. Conclusion:
The smart cane project significantly advances assistive technology, providing visually impaired users with real-time obstacle detection and navigation support. Successful integration of sensors, GPS, a camera, and AI, alongside user-friendly voice interaction, ensures safe and efficient movement. Continuous feedback and updates will further enhance its functionality, promoting greater inclusivity and accessibility. This project not only meets current needs but also sets the stage for future innovations in assistive technology.


 
