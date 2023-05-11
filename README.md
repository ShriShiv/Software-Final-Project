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
gridfs (GridFS)
bson (ObjectId)
os

The windows will be displayed in GUI. 

### Instructions Manual

#### Patient Side

1. Run the main code and the login GUI will pop up 
<img width="269" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/103fc076-041e-414f-a119-c5e48def705f">
2. Login using a specific userID and Password (SoftwareProject and asdf12345)
3. If the login is incorrect, there will be a popup that states "Incorrect username or password" 
<img width="530" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/92313e1d-990c-4092-885b-216344208df7">
4. Try again to add the correct username and password
5. Once entered, the user type GUI opens up. This allows you to select if it is an existing user or a new user 
<img width="164" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/84437c93-4fa1-42c8-a137-8e8295da1fbc">
6. To enter new user information, please select new user
7. Once entered, patient GUI opens up 
<img width="456" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/d2d137c5-9d1a-46c6-bdcc-3bbec195c708">
8. Here, patient details such as first name, last name, age, medical record number, phone, email, and snoring audio can be added
9. Snoring audio will open the folders in the desktop and allow to select the correct file 
<img width="812" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/1e8b8ea1-e1ef-4cb0-be0e-7a337856efb7">
10. The snoring audio should be in .wav form 
11. Once the file is selected, the paitent GUI will automatically generate a plot that displays the snoring graph which is useful for the provider
<img width="452" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/dd903d4a-7d98-4648-a457-786d276a3674">
12. After adding all the data, the user can hit submit and the data will be taken to the server 
13. There are also two other bottons on the bottom of the form. They are "new form" and "back". "new form" erases the existing form so new patient information can be included. "back" takes the user back to the User Type GUI where a new patient or exisitng patient can be selected.
14. To view physician feedback of an existing patient, select existing patient in the User Type GUI. This will open a form
<img width="215" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/bed3f59d-f1d9-497b-8592-557f5b74f5fe">
15. Enter patient record number and select open. This will open patient information and the physician feedback. 
<img width="486" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/8fb77065-9ccc-4ee9-8d6d-ca7f7fd59d8d">


#### Provider Side

1. Provider will be able to view the Provider GUI 
2. In that, provider selects the patient medical record number and that specific patient information is visible
<img width="432" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/453edf3e-a389-4889-a303-b9e2ad5c83bd">
3. The provider can view the patient data and graph and click the next steps through the dropdown
4. Once done, they can upload changes for the specific patient 
<img width="401" alt="image" src="https://github.com/ShriShiv/Software-Final-Project/assets/16839045/408e8f5c-d5d8-4ad3-8db2-e120ed373865">


All the forms are made using classes



