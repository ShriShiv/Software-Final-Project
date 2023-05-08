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
            patient_gui = PatientForm(root)
            
        else:
            messagebox.showerror("Error", "Incorrect username or password.")

# class UserType:
#     def __init__(self, master):
#         self.master = master
#         master.title("User Type")
#         self.button_newuser = tk.Button(master, text="New User", command = self.Patient_Form)
#         self.button_newuser.grid(row=0, column=0, columnspan=2)
        
#         self.button_existuser = tk.Button(master, text="Existing User", command = self.Patient_Form)
#         self.button_existuser.grid(row=1, column=0, columnspan=2)
#     def Patient_Form(self):
#         root = tk.Toplevel()
#         patient_form = PatientForm(root)

#         # Destroy the UserType window
#         self.master.destroy()
    

class PatientForm(tk.Frame):
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
        self.number_label = tk.Label(self, text="Patient Record Number:")
        self.number_label.grid(row=0, column=0)
        self.number_entry = tk.Entry(self)
        self.number_entry.grid(row=0, column=1)

        # Row 1
        self.fname_label = tk.Label(self, text="First Name:")
        self.fname_label.grid(row=1, column=0)
        self.fname_entry = tk.Entry(self)
        self.fname_entry.grid(row=1, column=1)
        
        # Row 2
        self.lname_label = tk.Label(self, text="Last Name:")
        self.lname_label.grid(row=2, column=0)
        self.lname_entry = tk.Entry(self)
        self.lname_entry.grid(row=2, column=1)
        
        # Row 3
        self.age_label = tk.Label(self, text="Age:")
        self.age_label.grid(row=3, column=0)
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=3, column=1)

        # Row 4
        self.ph_label = tk.Label(self, text="Contact Phone:")
        self.ph_label.grid(row=4, column=0)
        self.ph_entry = tk.Entry(self)
        self.ph_entry.grid(row=4, column=1)

        # Row 5
        self.email_label = tk.Label(self, text="Contact Email:")
        self.email_label.grid(row=5, column=0)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=5, column=1)

        # Row 6
        self.audio_label = tk.Label(self, text="Audio file:")
        self.audio_label.grid(row=6, column=0)
        self.upload_button = tk.Button(self, text="Upload", command=self.upload_audio_file)
        self.upload_button.grid(row=6, column=1)

        # Row 7
        self.plot_label = tk.Label(self, text="Plot:")
        self.plot_label.grid(row=7, column=0)
        self.plot_canvas = tk.Canvas(self, width=400, height=300, bg="white")
        self.plot_canvas.grid(row=8, column=0, columnspan=2)

        # Row 9
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=9, column=1)

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
            signal, _ = librosa.load(file_path, sr=44100)
            plt.figure(figsize=(4,3))
            plt.plot(signal)
            #plt.axis('off')
            plt.tight_layout()
            plt.savefig('plot.png')
            self.plot_image = tk.PhotoImage(file='plot.png')
            self.plot_canvas.create_image(0, 0, image=self.plot_image, anchor='nw')
            plt.close()

    def submit_form(self):
        '''
        This method submits the patient data into MongoDB database.

        Parameters: None

        Returns: None

        The code will upload all the patient data into MongoDB and the provider will be 
        able to see the data from their end. 
        '''
        number = self.number_enter.get()
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
            patients = db.patients
            patient = {
                "patient record number": number,
                "first name": fname,
                "last name": lname,
                "age": age,
                "phone": ph,
                "email":email,
                "audio_file_path": audio_file_path,
            }
            patients.insert_one(patient)
            # Clear the form
            self.number_entry.delete(0, tk.END)
            self.fname_entry.delete(0, tk.END)
            self.lname_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.ph_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.plot_canvas.delete("all")
            self.plot_image = None
            self.submit_button = tk.Button(self.master, text="Submit", command=self.insert_patient)
            self.submit_button.pack()
    def insert_patient(self):
        '''
        This is the last method that finally inserts all the data

        Parameters: None

        Returns: None
        '''
        number = self.number_entru.gets()
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        age = self.age_entry.get()
        ph = self.ph_entry.get()
        email = self.email_entry.get()
        #audio_file_path =




class ProviderForm(tk.Frame):
    '''
    A class representing a form for viewing patient information, including patient record number, first name, last name, 
    age, contact phone, contact email, and snoring audio file. The form can be updated, which 
    will take the patient information from MongoDB database to display code.

    Attributes:
    - master (Tk): the root window for the GUI.

    Methods:
    - __init__(self, master=None): initializes the ProviderForm window and its elements.
    - display_patients(self): displays all patient information in the GUI window.
    - search_patients(self): searches for patient information based on user input and displays the results in the GUI window.
    """
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

        # create a label to display the patient information
        self.info_label = tk.Label(self.master, text="")
        self.info_label.pack()

        # add a search bar to search for patients by name
        self.search_var = tk.StringVar()
        self.search_bar = tk.Entry(self.master, textvariable=self.search_var)
        self.search_bar.pack()
        self.search_button = tk.Button(self.master, text="Search", command=self.search_patients)
        self.search_button.pack()

        # display all patients by default
        self.display_patients()

    def display_patients(self):
        '''
        Displays all patient information in the GUI window.

        Parameters: None

        Returns:None
        '''
        # retrieve all patient documents from the collection
        patients = collection.find()

        # create a string to display the patient information
        info_str = "Patient Information:\n\n"
        for patient in patients:
            info_str += f"Name: {patient['name']}\nAge: {patient['age']}\nAudio File: {patient['audio_file']}\n\n"

        # display the patient information in the label
        self.info_label.config(text=info_str)

    def search_patients(self):
        '''
        Searches for patients in the database based on a search query depending on the patient record number. 

        Parameters: None

        Returns:None
        '''
        # retrieve the search query from the search bar
        search_query = self.search_var.get()

        # query the collection for patient documents that match the search query
        patients = collection.find({"name": {"$regex": search_query, "$options": "i"}})

        # create a string to display the search results
        info_str = "Search Results:\n\n"
        for patient in patients:
            info_str += f"Name: {patient['name']}\nAge: {patient['age']}\nAudio File: {patient['audio_file']}\n\n"

        # display the search results in the label
        self.info_label.config(text=info_str)




root = tk.Tk()
login = LoginGUI(root)
root.mainloop()






