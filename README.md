# Software Final Project

## Patient Monitoring Client Server System

The purpose of this project is to develop a patient monitoring client server system for patients with sleep disorders like sleep apnea. This system enables patients to upload their information and snoring files, which will then be stored on a server (MongoDb is used for storing the data). The provider can access the patient data and provide suggestions based on the data.

The system allows the following functionalities:

- Patients can upload their data to the server.
- The data is stored on the server and can be accessed by the provider.
- The provider can view the data and provide suggestions to the patient.
- This project aims to improve patient care for people with sleep disorders, making it easier for both patients and providers to access and manage data related to patient health.

### Packages needed
tkinter
matplotlib
pymongo
numpy 
wave
librosa

The windows will be displayed in GUI. 

### Instructions Manual

#### Patient Side

1. Run the main code and the login GUI will pop up
2. Login using a specific userID and Password (SoftwareProject and asdf12345)
3. If the login is incorrect, there will be a popup that states "Incorrect username or password" 
4. Try again to add the correct username and password
5. Once entered, patient GUI opens up
6. Here, patient details such as first name, last name, age, medical record number, phone, email, and snoring audio can be added
7. Snoring audio will open the folders in the desktop and allow to select the correct file
8. The snoring audio should be in .wav form 
9. Once the file is selected, the paitent GUI will automatically generate a plot that displays the snoring graph which is useful for the provider
10. After adding all the data, the user can hit submit and the data will be taken to the server 


#### Provider Side

1. Provider will be able to view the Provider GUI 
2. In that, provider selects the patient medical record number and that specific patient information is visible
3. The provider can view the patient data and graph and click the next steps through the dropdown
4. Once done, they can upload changes for the specific patient 






