'''
Shri Prabha Shivram
Software Carpentry Final Project = "Patient and Provider System"
'''
#Importing all the required modules
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import pymongo
from tkinter import messagebox
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import wave
import librosa
from gridfs import GridFS
from bson import ObjectId
from pymongo import MongoClient
import os
import librosa.display

#Initilizing connection to MongoDB 
client = pymongo.MongoClient("mongodb+srv://sshivra1:Spsleo05@cluster0.cxduuuj.mongodb.net/")
db = client["mydatabase"]
collection = db["patients"]
print(client.server_info())

class LoginGUI:
    '''
    A GUI for user login.

    Parameters:
    master (Tk): the root window for the GUI.

    Attributes:
    master (Tk): the root window for the GUI.
    label_username (Label): a label for the username field.
    label_password (Label): a label for the password field.
    entry_username (Entry): an entry field for the username.
    entry_password (Entry): an entry field for the password.
    button_login (Button): a button for submitting the login credentials.

    Methods:
    __init__(self, master): initializes the GUI window and its elements.
    login(self): validates the login credentials and opens the PatientForm window if correct.
    '''
    def __init__(self, master):
        '''
        Initializes the LoginGUI window and its elements.

        Parameters:
        master (Tk): the root window for the GUI.

        Returns:None
        '''
        self.master = master
        master.title("Login")

        self.label_username = tk.Label(master, text="Username:")
        self.label_password = tk.Label(master, text="Password:")

        self.entry_username = tk.Entry(master)
        self.entry_password = tk.Entry(master, show="*")

        self.label_username.grid(row=0, column=0, sticky=tk.W)
        self.entry_username.grid(row=0, column=1)
        self.label_password.grid(row=1, column=0, sticky=tk.W)
        self.entry_password.grid(row=1, column=1)

        self.button_login = tk.Button(master, text="Login", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2)

    def login(self):
        '''
        Checks if the login credentials are correct. If the information is incorrect, shows that the username and password is incorrect.
        If the password is correct, then it will move to the PatientForm class to get the patient data

        Returns:  None
        '''
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "SoftwareProject" and password == "asdf12345":
            self.master.destroy()
            root = tk.Tk()
            patient_type = UserType(root)
            
        else:
            messagebox.showerror("Error", "Incorrect username or password.")

class UserType:
    '''
    GUI for user to select the form
    Parameters:
    master (Tk): the root window for the GUI.

    Attributes:
    master (Tk): the root window for the GUI.
    button_newuser (Button): a button for that opens an empty form that new user can fill.
    button_existuser (Button): a button for opening existing form that displays clinician feedback.

    Methods:
    __init__(self, master): initializes the GUI window and its elements.
    New_Patient_Form(self): Connects to the new patient form 
    Exist_Patient_Form(self): Connects to the existing patient form 
    '''
    def __init__(self, master):
        '''
        Initializes the UserType window and its elements. The window consists of two button that will take the user to the 
        respected forms (new patient form or existing patient form)

        Parameters:
        master (Tk): the root window for the GUI.

        Returns:None
        '''
        self.master = master
        master.title("User Type")
        self.button_newuser = tk.Button(master, text="New User", command = self.New_Patient_Form)
        self.button_newuser.grid(row=0, column=0, columnspan=2)
        
        self.button_existuser = tk.Button(master, text="Existing User", command = self.Exist_Patient_Form)
        self.button_existuser.grid(row=1, column=0, columnspan=2)
    
    def New_Patient_Form(self):
        '''
        Connects to the New Patient Form class 

        Returns: None
        '''
        root = tk.Tk()
        patient_form = NewPatientForm(root)

        # Destroy the UserType window
        self.master.destroy()
    
    def Exist_Patient_Form(self):
        '''
        Connects to the Existing Patient Form class 

        Returns: None
        '''
        root = tk.Tk()
        existing_patient_form = ExistingPatientForm(master=root)

        # Destroy the UserType window
        self.master.destroy()
        
    

class NewPatientForm(tk.Frame):
    '''
    A class representing a form for collecting patient information, including first name, last name, 
    age, contact phone, contact email, and snoring audio file. The form can be submitted, which 
    will insert the patient information into a MongoDB database.

    Attributes:

    master: A tkinter master widget.
    number_label: A tkinter Label widget for the "Patient record number" field.
    number_entryA tkinter Entry widget for entering the patient's record number.
    fname_label: A tkinter Label widget for the "First Name" field.
    fname_entry: A tkinter Entry widget for entering the patient's first name.
    lname_label: A tkinter Label widget for the "Last Name" field.
    lname_entry: A tkinter Entry widget for entering the patient's last name.
    age_label: A tkinter Label widget for the "Age" field.
    age_entry: A tkinter Entry widget for entering the patient's age.
    ph_label: A tkinter Label widget for the "Contact Phone" field.
    ph_entry: A tkinter Entry widget for entering the patient's contact phone.
    email_label: A tkinter Label widget for the "Contact Email" field.
    email_entry: A tkinter Entry widget for entering the patient's contact email.
    audio_label: A tkinter Label widget for the "Audio file" field.
    upload_button: A tkinter Button widget for uploading an audio file.
    plot_label: A tkinter Label widget for the "Plot" field.
    plot_canvas: A tkinter Canvas widget for displaying the plot of the uploaded audio file.
    submit_button: A tkinter Button widget for submitting the form.
    
    Methods:

    init(self, master=None): Initializes the PatientForm instance.
    create_widgets(self): Creates the widgets for the form.
    upload_audio_file(self): Asks the user to select an audio file and displays the plot of the waveform in the plot_canvas.
    plot_waveform(self, file_path): Plots the waveform of the audio file specified by the file_path and displays it in the plot_canvas.
    submit_form(self): Inserts the patient information into the MongoDB database and clears the form.
    insert_patient(self): Inserts the patient information into the MongoDB database.
    '''
    def __init__(self, master=None):
        '''
        Initializes the PatientForms window and its elements.

        Parameters:
        master (Tk): the root window for the GUI.

        Returns:None
        '''
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        master.title("Patient Form")

    def create_widgets(self):
        '''
        Responsible for creating and placing all the necessary widgets in the PatientForm.
        The method creates labels and entry boxes for the user to input their personal 
        information such as their patient number, first name, last name, age, contact phone, and contact email. 
        Additionally, it creates a button for the user to upload an audio file, a label for 
        the plot, and a canvas for the plot to be displayed.

        Parameters: None

        Returns: None

        The code will take all the data and move to the next method "upload_audio_file" to upload the file. 
        '''
        # Row 0
        self.number_label = tk.Label(self, text="Patient Record Number:*")
        self.number_label.grid(row=0, column=0)
        self.number_entry = tk.Entry(self)
        self.number_entry.grid(row=0, column=1)

        # Row 1
        self.fname_label = tk.Label(self, text="First Name:*")
        self.fname_label.grid(row=1, column=0)
        self.fname_entry = tk.Entry(self)
        self.fname_entry.grid(row=1, column=1)
        
        # Row 2
        self.lname_label = tk.Label(self, text="Last Name:*")
        self.lname_label.grid(row=2, column=0)
        self.lname_entry = tk.Entry(self)
        self.lname_entry.grid(row=2, column=1)
        
        # Row 3
        self.age_label = tk.Label(self, text="Age:*")
        self.age_label.grid(row=3, column=0)
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=3, column=1)

        # Row 4
        self.ph_label = tk.Label(self, text="Contact Phone:*")
        self.ph_label.grid(row=4, column=0)
        self.ph_entry = tk.Entry(self)
        self.ph_entry.grid(row=4, column=1)

        # Row 5
        self.email_label = tk.Label(self, text="Contact Email:*")
        self.email_label.grid(row=5, column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=5, column=1)

        # Row 6
        self.audio_label = tk.Label(self, text="Audio file:*")
        self.audio_label.grid(row=6, column=0)
        self.upload_button = tk.Button(self, text="Upload", command=self.upload_audio_file)
        self.upload_button.grid(row=6, column=1)

        # Row 7
        self.plot_label = tk.Label(self, text="Plot:*")
        self.plot_label.grid(row=7, column=0)
        self.plot_canvas = tk.Canvas(self, width=400, height=300, bg="white")
        self.plot_canvas.grid(row=8, column=0, columnspan=2)
        self.canvas = None
        # Row 9
        self.back_button = tk.Button(self, text="Back", command=self.back)
        self.back_button.grid(row=9, column=0)

        #Row 9
        self.clear_button = tk.Button(self, text = "New Form", command = self.new_form)
        self.clear_button.grid(row = 9, column = 1)

        #Row 9
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=9, column=2)

        
    def back(self):
        '''
        Take the user back to the form where they can either select a new patient or an 
        existing patient. This can be used to check the status of the new patient or any 
        other existing patient on the feedback provided by the clinician. 
        
        Parameters: None

        Returns: None
        '''
        root = tk.Tk()
        Back_to_user = UserType(root)
        self.master.destroy()
        
    
    def upload_audio_file(self):
        '''
        This method takes in the snoring audio file in .wav format
        
        Parameters: None

        Returns: None

        The code will send the file to the next method for creating a plot
        '''
        file_path = filedialog.askopenfilename(filetypes=[("Waveform Audio File Format", "*.wav")])
        self.plot_waveform(file_path)
    
    def plot_waveform(self, file_path):
        '''
        This method takes the .wav file and converts it into a plot using matplotlib. 

        Parameters: None

        Returns: None

        The code will display the plot consisting of the snoring graph in the PatientForm Gui
        below the upload file button. 
        '''
        if file_path:
            signal, sr = librosa.load(file_path, sr=44100)
            duration = signal.shape[0] / sr
            time_axis = np.linspace(0, duration, signal.shape[0], endpoint=False)

            fig = plt.figure(figsize=(4,3))
            ax = fig.add_subplot(111)
            ax.plot(time_axis, signal)
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('Amplitude')
            plt.tight_layout()
            
            if self.canvas:
                self.canvas.get_tk_widget().destroy()  # Remove previous canvas if it exists
            
            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_canvas)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
            plt.close()


    def submit_form(self):
        '''
        This method submits the patient data into MongoDB database.

        Parameters: None

        Returns: None

        The code will upload all the patient data into MongoDB and the provider will be 
        able to see the data from their end. 
        '''
        number = self.number_entry.get()
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        age = self.age_entry.get()
        ph = self.ph_entry.get()
        email = self.email_entry.get()
        audio_file_path = filedialog.askopenfilename(filetypes=[("Waveform Audio File Format", "*.wav")])
        if fname and lname and age and ph and email and audio_file_path:
            # Insert data into MongoDB
            client = pymongo.MongoClient("mongodb+srv://sshivra1:Spsleo05@cluster0.cxduuuj.mongodb.net/")
            db = client.patients_db
            fs = GridFS(db)
            with open(audio_file_path, 'rb') as f:
                file_id = fs.put(f, filename=os.path.basename(audio_file_path))
 
            
            patients = db.patients
            patient = {
                "patient record number": number,
                "first name": fname,
                "last name": lname,
                "age": age,
                "phone": ph,
                "email":email,
                "audio_file": file_id,
            }
            patients.insert_one(patient)
            print("Registration data saved to MongoDB")
            
           
           
    def insert_patient(self):
        '''
        This is the last method that finally inserts all the data

        Parameters: None

        Returns: None
        '''
        number = self.number_entry.get()
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        age = self.age_entry.get()
        ph = self.ph_entry.get()
        email = self.email_entry.get()


    def new_form(self):
        '''
        This attribut erases all the information in the existing form and creates a blank one to fill new patient data
        
        Parameters: None

        Returns: None
        '''
        # Clear the form
        self.number_entry.delete(0, tk.END)
        self.fname_entry.delete(0, tk.END)
        self.lname_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.ph_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.plot_canvas.delete("all")
        self.canvas.get_tk_widget().destroy() 
        





class ProviderForm(tk.Frame):
    '''
    A class representing a form for viewing patient information, including patient record number, first name, last name, 
    age, contact phone, contact email, and snoring audio file. The form can be updated, which 
    will take the patient information from MongoDB database to display code. The physician viewing it can then provide
    two types of response. A quick response using a dropdown menu with the following options: 
    "Normal", "Need to visit sleep clinic", "Need to get sleep study". There is also a section called physician notes. 
    In the physician notes section, the physician can provide detailed notes if necessary. 

    Attributes:
    - master (Tk): the root window for the GUI.

    Methods:
    - __init__(self, master=None): initializes the ProviderForm window and its elements.
    - open_patients(self): gets the patient record number and searches from MongoDB to get the patient information 
    - connect_to_mongodb(self): Creates a connection to a new mongodb database 
    - save_to_mongodb(self): Uploads the data to the new mongodb database 
    '''
    def __init__(self, master=None):
        '''
        Initializes the PatientForms window and its elements.

        Parameters:
        master (Tk): the root window for the GUI.

        Returns:None
        '''
        super().__init__(master)
        self.master = master
        self.master.title("Provider Form")
        self.master.fullscreen = True
        # configure rows and columns to expand
        self.master.grid_rowconfigure(0, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(1, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(2, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(3, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(4, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(5, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(6, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(7, weight=1, uniform ='rows')
        self.master.grid_rowconfigure(8, weight=1)
        self.master.grid_rowconfigure(9, weight=1, uniform ='rows')
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        # create a label and entry for patient id
        tk.Label(master, text="Patient Record Number: ").grid(row=0, column=0)
        self.patient_num_entry = tk.Entry(master)
        self.patient_num_entry.grid(row=0, column=1)

        # create a button to open the patient information
        tk.Button(master, text="Open", command=self.open_patient).grid(row=0, column=2)

        # create labels to display patient information
        tk.Label(master, text="First Name: ").grid(row=1, column=0)
        self.fname_label = tk.Label(master, text="")
        self.fname_label.grid(row=1, column=1)
        
        tk.Label(master, text="Last Name: ").grid(row=2, column=0)
        self.lname_label = tk.Label(master, text="")
        self.lname_label.grid(row=2, column=1)
        
        tk.Label(master, text="Age: ").grid(row=3, column=0)
        self.age_label = tk.Label(master, text="")
        self.age_label.grid(row=3, column=1)

        tk.Label(master, text="Contact Phone: ").grid(row=4, column=0)
        self.ph_label = tk.Label(master, text="")
        self.ph_label.grid(row=4, column=1)

        tk.Label(master, text="Contact Email: ").grid(row=5, column=0)
        self.email_label = tk.Label(master, text="")
        self.email_label.grid(row=5, column=1)

        tk.Label(master, text="Audio File: ").grid(row=6, column=0)
        self.audio_label = tk.Label(master, text="")
        self.audio_label.grid(row=6, column=1)

        self.plot_label = tk.Label(self.master)
        self.plot_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        self.figure = plt.figure(figsize=(3, 2))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=3, padx=5, pady=5)

        tk.Label(master, text = "Physician quick response: ").grid(row = 9, column = 0)
        self.selected_provider = tk.StringVar()
        self.provider_dropdown = tk.OptionMenu(master, self.selected_provider, "Normal", "Need to visit sleep clinic", "Need to get sleep study")
        self.provider_dropdown.config(width=30)
        self.provider_dropdown.grid(row=9, column=1)
        self.save_button = tk.Button(master, text="Save", command=self.save_to_mongodb)
        self.save_button.grid(row=10, column=3, columnspan=1)

        # create a label and text box for physician notes
        tk.Label(master, text="Physician notes: ").grid(row=10, column=0)
        self.physician_notes_text = tk.Text(master, height=10, width=30)  # Multiline text box
        self.physician_notes_text.grid(row=10, column=1)

        # Create a label for displaying the save status
        self.save_status_label = tk.Label(master, text="")
        self.save_status_label.grid(row=11, column=3, columnspan=4)

        self.connect_to_mongodb()

    

    def open_patient(self):
            '''
            This methods displays the patient information for the specific record number choosen
            Parameters: None
            Returns: None
            '''
            client = pymongo.MongoClient("mongodb+srv://sshivra1:Spsleo05@cluster0.cxduuuj.mongodb.net/")
            db = client["patients_db"]
            collection = db["patients"]
            fs = GridFS(db)
       
            # get the patient id from the entry widget
            patient_id = self.patient_num_entry.get()

            # query the patient information from MongoDB
            patient = collection.find_one({'patient record number': patient_id}) #{'patient record number': patient_id}
          
            #update the labels with patient information
            if patient:
                self.fname_label.config(text = patient["first name"])
                self.lname_label.config(text = patient["last name"])
                self.age_label.config(text = patient["age"])
                self.ph_label.config(text = patient["phone"])
                self.email_label.config(text = patient["email"])
                audio_file_id = patient["audio_file"]
                audio_file = fs.get(ObjectId(audio_file_id))
                self.audio_label.config(text=audio_file.filename)
                
                # Load the audio file data
                audio_data, sample_rate = librosa.load(audio_file,sr=44100)
                
                # Calculate the duration of the audio data
                duration = len(audio_data) / sample_rate
                time_axis = np.linspace(0, duration, len(audio_data), endpoint=False)
                
                # Plot the audio data
                self.figure.clear()
                plt.plot(time_axis,audio_data)
                plt.xlabel('Time (seconds)')
                plt.ylabel('Amplitude')
                plt.tight_layout()
                self.canvas.draw()

            else:
                self.fname_label.config(text="")
                self.lname_label.config(text = "")
                self.age_label.config(text = "")
                self.ph_label.config(text = "")
                self.email_label.config(text = "")
                self.audio_label.config(text = "")
    
    def connect_to_mongodb(self):
        '''
            This methods connects to mongodb to upload the provider information such as 
            quick response and physician notes
            Parameters: None
            Returns: None
        '''
       
        self.client = MongoClient("mongodb+srv://sshivra1:Spsleo05@cluster0.cxduuuj.mongodb.net/")
        self.db = self.client['mydatabase']
        self.collection = self.db['provider_data']
    

    def save_to_mongodb(self):
        '''
            This methods uploads the data to mongodb to upload the patient information such as 
            name, age, provider quick response and notes. 
            Parameters: None
            Returns: None
        '''
        patient_num = self.patient_num_entry.get()
        fname = self.fname_label.cget("text")
        lname = self.lname_label.cget("text")
        age = self.age_label.cget("text")
        provider = self.selected_provider.get()
        physician_notes =  self.physician_notes_text.get("1.0", tk.END).strip()
        data = {
            'patient_num': patient_num,
            'patient_fname': fname,
            'patient_lname': lname,
            'patient_age': age,
            'provider': provider,
            'physician_notes': physician_notes
        }

        # Insert data into MongoDB
        self.collection.insert_one(data)
        print("Data saved to MongoDB!")
        # Update the save status label
        self.save_status_label.config(text="Data saved")







class ExistingPatientForm(tk.Frame):
    '''
    This form is used by the patient to view the physician feedback. When the physician provides feedback using the 
    provider form, the patient can view the feedback through this Existing user form. Patient record number needs to 
    be entered to open the patient information and feedback. 

    Attributes:
    - master (Tk): the root window for the GUI.

    Methods:
    - __init__(self, master=None): initializes the ExistingPatientForm window and its elements.
    - open_patients(self): gets the patient record number and searches from MongoDB to get the patient information inclucing
    physician feedback
    '''
    def __init__(self, master=None):
        '''
        Initializes the PatientForms window and its elements.

        Parameters:
        master (Tk): the root window for the GUI.

        Returns:None
        '''
        super().__init__(master)
        self.master = master
        self.master.title("Existing User Form")
       

        # create a label and entry for patient id
        tk.Label(master, text="Patient Record Number: ").grid(row=0, column=0)
        self.patient_num_entry = tk.Entry(master)
        self.patient_num_entry.grid(row=0, column=1)

        # create a button to open the patient information
        tk.Button(master, text="Open", command=self.open_patient).grid(row=0, column=2)

        # create labels to display patient information
        tk.Label(master, text="First Name: ").grid(row=1, column=0)
        self.fname_label = tk.Label(master, text="")
        self.fname_label.grid(row=1, column=1)
        
        tk.Label(master, text="Last Name: ").grid(row=2, column=0)
        self.lname_label = tk.Label(master, text="")
        self.lname_label.grid(row=2, column=1)
        
        tk.Label(master, text="Age: ").grid(row=3, column=0)
        self.age_label = tk.Label(master, text="")
        self.age_label.grid(row=3, column=1)

        tk.Label(master, text = "Physician quick response: ").grid(row = 6, column = 0)
        self.QuickResponse_label = tk.Label(master, text="")
        self.QuickResponse_label.grid(row=6, column=1)
       
        tk.Label(master, text = "Physician notes: ").grid(row = 7, column = 0)
        self.notes_label = tk.Label(master, text="")
        self.notes_label.grid(row=7, column=1)


    def open_patient(self):
            '''
            This methods displays the patient information for the specific record number choosen
            '''
            client = pymongo.MongoClient("mongodb+srv://sshivra1:Spsleo05@cluster0.cxduuuj.mongodb.net/")
            db = client["mydatabase"]
            collection = db["provider_data"]
        
            # get the patient id from the entry widget
            patient_id = self.patient_num_entry.get()
            print(patient_id )
            # query the patient information from MongoDB
            patient = collection.find_one({'patient_num': patient_id}) #{'patient record number': patient_id}
            #print(patient)
            #update the labels with patient information
            if patient:
                self.fname_label.config(text = patient["patient_fname"])
                self.lname_label.config(text = patient["patient_lname"])
                self.age_label.config(text = patient["patient_age"])
                self.QuickResponse_label.config(text = patient["provider"])
                self.notes_label.config(text = patient["physician_notes"])
                

            else:
                self.fname_label.config(text="")
                self.lname_label.config(text = "")
                self.age_label.config(text = "")
                self.QuickResponse_label.config(text = "")
                self.notes_label.config(text = "")
                




# root = tk.Tk()
# #Simultaneous display
# # Create the login window as a Toplevel widget
# login_window = tk.Toplevel(root)
# login = LoginGUI(login_window)

# # Create the provider form window as a Toplevel widget
# provider_window = tk.Toplevel(root)
# provider_form = ProviderForm(provider_window)
# # Start the main event loop for the main window
# root.mainloop()


#individual display for testing
root = tk.Tk()
login = LoginGUI(root)
root.attributes('-fullscreen', True)
root.mainloop()

# root2 = tk.Tk()
# login = ProviderForm(root2)
# root2.attributes('-fullscreen', True)
# root2.mainloop()




