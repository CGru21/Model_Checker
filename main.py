import tkinter as tk
from PIL import ImageTk, Image
import modifiedTransitions as MT
from tkinter import filedialog as fd
from aux_functions import read_xml


class mcGUI(object):

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modelchecker")
        self.root.config(bg="darkgrey")

        self.root.columnconfigure(index=0,weight=1)
        self.root.columnconfigure(index=1,weight=3)
        self.root.rowconfigure(index=[0,1],weight=1)

        # create top menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import", command=self.import_kts)
        filemenu.add_command(label="Save")
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=helpmenu)

        # initialize kripke transition system
        self.states = []
        self.transitions = []
        self.kts = MT.KTS_model()
        self.machine = MT.KTS(model=self.kts, show_state_attributes=True)

        # frame for atomic propositions
        self.create_ap_frame()
        self.ap_frame.grid(column=0,row=0,sticky="nsew", padx=5, pady=5)

        # frame for CTL Formulas
        self.create_ctl_frame()
        self.ctl_frame.grid(column=0,row=1,sticky="nsew", padx=5, pady=5)

        # frame for displaying the graph
        self.create_graph_frame()
        self.graph_frame.grid(column=1,row=0,rowspan=2, sticky="nsew", padx=5, pady=5)

        self.root.mainloop()

    def create_ap_frame(self):
        self.ap_frame = tk.Frame(self.root, width=400, height=200)
        self.ap_frame.grid_propagate(0)

        rows_count = list(range(3+3)) # initially 3 empty rows of the AP table are loaded

        self.ap_frame.columnconfigure(index=[0,1],weight=1)
        self.ap_frame.rowconfigure(index=rows_count,weight=2)

        ap_headline = tk.Label(self.ap_frame, text="Manage APs", borderwidth=2, relief="groove")
        ap_headline.grid(column=0,row=0,columnspan=2,sticky="nsew")

        self.editAP_button = tk.Button(master=self.ap_frame, text="Edit", command=self.editAP)
        self.editAP_button.grid(column=0,row=1,sticky="nw")

        states_table = tk.Label(self.ap_frame, text="State", borderwidth=1, relief="solid")
        states_table.grid(column=0,row=2,sticky="nsew")

        ap_table = tk.Label(self.ap_frame, text="Atomic Proposition", borderwidth=1, relief="solid")
        ap_table.grid(column=1,row=2,sticky="nsew")

        self.ap_labels = []
        self.ap_entrys = []
        self.state_labels = []
        state_count = 0

        for s in range(3): # see update_ap_frame()
            state_label = tk.Label(self.ap_frame, text="", borderwidth=1, relief="solid")
            state_label.grid(column=0,row=3+state_count,sticky="nsew")

            #ap = tk.Label(self.ap_frame, text="", borderwidth=1, relief="solid")
            #ap.grid(column=1,row=3+state_count,sticky="nsew")
            self.ap_labels.append(tk.Label(self.ap_frame, text="", borderwidth=1, relief="solid"))
            self.ap_labels[state_count].grid(column=1,row=3+state_count,sticky="nsew")

            state_count += 1

    def create_ctl_frame(self):
        self.ctl_frame = tk.Frame(self.root, width=400, height=200)
        self.ctl_frame.grid_propagate(0)

        self.ctl_frame.columnconfigure(index=[0,1],weight=1)
        self.ctl_frame.rowconfigure(index=[0,1,2,3,4],weight=2)

        ap_label = tk.Label(self.ctl_frame, text="Manage CTL-Formulas", borderwidth=2, relief="groove")
        ap_label.grid(column=0,row=0,columnspan=2,sticky="nsew")

        editCTL_button = tk.Button(master=self.ctl_frame, text="Edit")
        editCTL_button.grid(column=0,row=1,sticky="nw")

        check_button = tk.Button(master=self.ctl_frame, text="Check")
        check_button.grid(column=1,row=1,sticky="ne")

        f1 = tk.IntVar()
        ctl1 = tk.Checkbutton(master=self.ctl_frame, text="AF(loggedout)", variable=f1)
        ctl1.grid(column=0,row=2,sticky="w")

        f2 = tk.IntVar()
        ctl2 = tk.Checkbutton(master=self.ctl_frame, text="EF(loggedin)", variable=f2)
        ctl2.grid(column=0,row=3,sticky="w")

        f3 = tk.IntVar()
        ctl3 = tk.Checkbutton(master=self.ctl_frame, text="EU(loggedin,loggedout)", variable=f3)
        ctl3.grid(column=0,row=4,sticky="w")

        s1 = tk.Label(self.ctl_frame, text="[All]")
        s1.grid(column=1,row=2,sticky="w")

        s2 = tk.Label(self.ctl_frame, text="[All]")
        s2.grid(column=1,row=3,sticky="w")

        s3 = tk.Label(self.ctl_frame, text="[Produkte]")
        s3.grid(column=1,row=4,sticky="w")

    def create_graph_frame(self):
        self.graph_frame = tk.Frame(self.root, height=400, width=1000)
        self.graph_frame.grid_propagate(0)

        self.graph_frame.columnconfigure(index=[0],weight=1)
        self.graph_frame.rowconfigure(index=[0,1],weight=2)

        graph_label = tk.Label(self.graph_frame, text="Kripke Transition System", borderwidth=2, relief="groove")
        graph_label.grid(column=0,row=0,sticky="nsew")

        self.graph_display = tk.Label(self.graph_frame, text="no diagram loaded", height=22)
        self.graph_display.grid(column=0,row=1,sticky="nsew")


    def import_kts(self):
        diagramPath = fd.askopenfilename(title='Select a State Machine Diagram', initialdir='./examples', filetypes=[('XML files', '*.xml')])

        self.states, self.transitions = read_xml(diagramPath)

        self.kts = MT.KTS_model()
        self.machine = MT.KTS(model=self.kts, initial=list(self.states[0].values())[0], states=self.states, transitions=self.transitions, show_state_attributes=True)
        self.kts.get_graph().draw('kts.png', prog='dot')
        self.update_image()
        self.clear_aplabels() # clear any existing labels of the table
        self.clear_statelabels()
        self.clear_apentrys()
        self.update_ap_frame()
        
    def update_image(self):
        self.graph_image = ImageTk.PhotoImage(Image.open("kts.png"))
        self.graph_display = tk.Label(self.graph_frame, image=self.graph_image, height=350)
        self.graph_display.image = self.graph_image
        self.graph_display.grid(column=0,row=1,sticky="nsew")

    def update_ap_frame(self):
        rows_count = list(range(len(self.machine.states.items())+3))
        self.ap_frame.rowconfigure(index=rows_count,weight=2)

        state_count = 0

        for s in self.machine.states.items():
            current_name = s[0]
            self.state_labels.append(tk.Label(self.ap_frame, text=f"{current_name}", borderwidth=1, relief="solid"))
            self.state_labels[state_count].grid(column=0,row=3+state_count,sticky="nsew")
            #state_label = tk.Label(self.ap_frame, text=f"{current_name}", borderwidth=1, relief="solid")
            #state_label.grid(column=0,row=3+state_count,sticky="nsew")

            current_ap = s[1].tags
            ap_tags = ', '.join(current_ap)
            self.ap_labels.append(tk.Label(self.ap_frame, text=ap_tags, borderwidth=1, relief="solid"))
            self.ap_labels[state_count].grid(column=1,row=3+state_count,sticky="nsew")
            #ap = tk.Label(self.ap_frame, text=ap_tags, borderwidth=1, relief="solid")
            #ap.grid(column=1,row=3+state_count,sticky="nsew")

            state_count += 1

    def clear_aplabels(self):
        for i in range(len(self.ap_labels)):
            self.ap_labels[i].destroy
        
        self.ap_labels.clear()

    def clear_statelabels(self):
        for i in range(len(self.state_labels)):
            self.state_labels[i].destroy
        
        self.state_labels.clear()

    def clear_apentrys(self):
        for i in range(len(self.ap_entrys)):
            self.ap_entrys[i].destroy
        
        self.ap_entrys.clear()

    def editAP(self):
        self.editAP_button.destroy()
        self.doneAP_button = tk.Button(master=self.ap_frame, text="Done", command=self.doneAP)
        self.doneAP_button.grid(column=0,row=1,sticky="nw")

        state_count = 0

        self.clear_aplabels()

        for s in self.machine.states.items():
            #print(s[1].tags)
            ap_tags = ""

            if s[1].tags != []:
                current_ap = s[1].tags
                ap_tags = ','.join(current_ap)

            self.ap_entrys.append(tk.Entry(self.ap_frame, borderwidth=1, relief="solid"))
            self.ap_entrys[state_count].insert(10,ap_tags)
            self.ap_entrys[state_count].grid(column=1,row=3+state_count,sticky="nsew")
            #ap_entry = tk.Entry(self.ap_frame, borderwidth=1, relief="solid")
            #ap_entry.insert(10,ap_tags)
            #ap_entry.grid(column=1,row=3+state_count,sticky="nsew")

            state_count += 1


    def doneAP(self):
        self.doneAP_button.destroy()
        self.editAP_button = tk.Button(master=self.ap_frame, text="Edit", command=self.editAP)
        self.editAP_button.grid(column=0,row=1,sticky="nw")

        state_count = 0

        for s in self.states:
            current_ap = self.ap_entrys[state_count].get()
            self.ap_entrys[state_count].destroy()
            self.ap_labels.append(tk.Label(self.ap_frame, text=current_ap, borderwidth=1, relief="solid"))
            self.ap_labels[state_count].grid(column=1,row=3+state_count,sticky="nsew")

            s['tags'] = current_ap.split(",")

            state_count += 1

        self.clear_apentrys()
        self.kts = MT.KTS_model()
        self.machine = MT.KTS(model=self.kts, initial=list(self.states[0].values())[0], states=self.states, transitions=self.transitions, show_state_attributes=True)
        self.kts.get_graph().draw('kts.png', prog='dot')
        self.update_image()



if __name__ == "__main__":
    gui = mcGUI()