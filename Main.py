from tkinter import *  #para magka roon ng GUI
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

window = Tk() # para mag karoon ng window

#this is where the class of algorithm is created
from FIFO import FIFO
from SJF import SJF
from NPP import NPP
from PP import PP
from SRTF import SRTF
from RR import RR


#para may choice kung anong algorithm ang gagamitin
def create_combobox(window):
    # Define options for the combo box
    title = tk.Label(window, font=('Helvetica', 20), anchor="center", width=85, bg="skyblue", text="Calculate your Chosen Algorithm")
    title.grid(row=1, column=5, columnspan=4, sticky="ew")

    options = ["First in First out", "Shortest Job First", "Non-Preemtive Priority", "Preemtive Priority", "Shortest Remaining Time First", "Round Robin"]

    # Create a combo box
    combo = ttk.Combobox(window, values=options, width=50, height=40,  font=('Helvetica', 20))
    
    # Set the default option (optional)
    combo.current(0)
    
    # Pack the combo box into the window
    combo.grid(row=3, column = 5)
    
    return combo


def show_alert(message): #ano to practice lang pamalit sa print para kita sa windows
    messagebox.showinfo("Selection Alert", message)


def clear_window(window):
    # tatanggalin yung mga widget na nasa loob pa kase lilinisin yung interface
    for widget in window.winfo_children():
        widget.destroy()


def MainFunc():
    option = combo.get()
    if (option == "First in First out" ):
        clear_window(window)
        #tatawagin na yung fifo
        fifo = FIFO(window)
    elif (option == "Shortest Job First"):
        clear_window(window)
        sjf = SJF(window)
    elif(option == "Non-Preemtive Priority"):
        clear_window(window)
        npp = NPP(window)
    elif(option == "Preemtive Priority"):
        clear_window(window)
        pp = PP(window)
    elif(option == "Shortest Remaining Time First"):
        clear_window(window)
        srtf = SRTF(window)
    elif(option == "Round Robin"):
        clear_window(window)
        rr = RR(window)
    else:
        show_alert("Choose a Valid Algorithm")

#this is the main loop dito nagsisimula yung mismong code
if __name__ == "__main__":
    
    combo = create_combobox(window) #calls the combobox function

    #pag pinindot yung button tsaka magrurun yung main function na calculation
    btn = Button(window , text="Select", command=MainFunc, width=30, font=('Helvetica', 14), anchor="center", bg="#F7E59D", fg="black")
    btn.grid(row=3, column = 6, sticky="ew")

    #ito yung mismong design ng windows


    #specifications of window
    window.geometry("1920x1024")
    window.title("CPU SCHEDULING")
    window.configure(bg="#D2F4F5")
    
    window.mainloop() #para magplace ng window sa screen 