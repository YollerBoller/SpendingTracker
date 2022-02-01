from tkinter import *
from ManageJson import *
from Warnings import *
import uuid
from datetime import date


class APP:

    def on_start(self):
        self.load_all_profiles()
        self.main_frame_on_start()
        return

    files = []
    dict_files = []
    profile_names = []

    def load_all_profiles(self):
        self.files.clear()
        self.dict_files.clear()
        self.profile_names.clear()

        self.files = get_profiles()

        for x in self.files:
            if "_reserve" not in x:
                self.dict_files.append(decode_json(x))

        for y in self.dict_files:
            self.profile_names.append(y["Profile"])
        return

    def dump_frames(self):
        self.main_frame.grid_forget()
        self.add_profile_frame.grid_forget()
        self.edit_profile_frame.grid_forget()
        return

    def load_main_frame(self, event=None):
        self.dump_frames()
        self.main_frame_on_start()
        self.main_frame_refresh()
        self.main_frame.grid(row=0, column=0, sticky=NW)
        root.geometry("450x290")
        return

    def load_add_profile_frame(self, event=None):
        self.dump_frames()
        self.add_profile_frame_refresh()
        self.add_profile_frame.grid(row=0, column=0, sticky=NW)
        root.geometry("360x180")
        return

    def load_edit_profile_frame(self, event=None):
        self.dump_frames()
        self.edit_profile_frame_on_start()
        self.edit_profile_frame_refresh()
        self.edit_profile_frame.grid(row=0, column=0, sticky=NW)
        root.geometry("300x340")
        return

    ###################################################################
    #   Main Frame Methods

    selected_profile_name = None
    selected_profile = None
    rolling_total = 0
    current_mark = 0

    selected_account_name = None
    selected_account = None
    selected_account_current_mark = None
    new_entry_amount = None
    new_entry_name = None

    selected_profile_accounts = []

    def main_frame_on_start(self):
        counter = 0
        self.profile_listbox.delete(0, END)
        for i in self.profile_names:
            self.profile_listbox.insert(counter, i)
            counter += 1
        return

    def main_frame_refresh(self):
        self.rolling_total_entry.configure(state="normal")
        self.current_mark_entry.configure(state="normal")
        self.main_name_entry.configure(state="normal")
        self.main_current_mark_entry.configure(state="normal")
        self.main_new_entry.configure(state="normal")
        self.main_new_entry_name_entry.configure(state="normal")

        self.account_listbox.delete(0, END)
        self.rolling_total_entry.delete(0, END)
        self.current_mark_entry.delete(0, END)
        self.main_name_entry.delete(0, END)
        self.main_current_mark_entry.delete(0, END)
        self.main_new_entry.delete(0, END)
        self.main_new_entry_name_entry.delete(0, END)

        if self.selected_profile_name is not None:
            counter = 0
            for i in self.selected_profile_accounts:
                self.account_listbox.insert(counter, i)
                counter += 1

        if self.selected_profile is not None:
            self.rolling_total_entry.insert(0, self.selected_profile["Rolling Total"])
            self.current_mark_entry.insert(0, self.selected_profile["Current Mark"])

        self.rolling_total_entry.configure(state="disabled")
        self.current_mark_entry.configure(state="disabled")
        self.main_name_entry.configure(state="disabled")
        self.main_current_mark_entry.configure(state="disabled")
        self.main_new_entry.configure(state="disabled")
        self.main_new_entry_name_entry.configure(state="disabled")
        return

    def select_profile(self, event=None):
        self.selected_profile_name = self.profile_listbox.get(self.profile_listbox.curselection())
        self.get_account_names()
        self.account_listbox.delete(0, END)
        self.main_frame_refresh()
        return

    def select_account(self, event=None):
        self.selected_account_name = self.account_listbox.get(self.account_listbox.curselection())
        self.selected_account = self.selected_profile["Accounts"][self.selected_account_name]
        self.selected_account_current_mark = self.selected_account["Current Mark"]

        self.main_name_entry.configure(state="normal")
        self.main_current_mark_entry.configure(state="normal")
        self.main_name_entry.delete(0, END)
        self.main_current_mark_entry.delete(0, END)

        self.main_name_entry.insert(0, self.selected_account_name)
        self.main_name_entry.configure(state="disabled")
        self.main_current_mark_entry.insert(0, self.selected_account_current_mark)
        self.main_current_mark_entry.configure(state="disabled")
        self.main_new_entry.configure(state="normal")
        self.main_new_entry_name_entry.configure(state="normal")
        return

    def add_entry(self, event=None):
        if self.selected_account_name is None:
            print("add_entry() -> No account selected")
            self.main_new_entry.delete(0, END)
            return
        else:
            self.new_entry_amount = float(self.main_new_entry.get())
            self.new_entry_name = self.main_new_entry_name_entry.get()
            if self.new_entry_amount is None:
                print("add_entry() -> Must enter a value.")
                return
            elif self.new_entry_amount == 0:
                print("add_entry() -> Must enter a value greater than 0.")
                return
            else:
                if self.new_entry_amount >= 500:
                    # Display prompt
                    invalid_entry_amount_msg()
                    return
                elif self.new_entry_amount >= 300:
                    # Display prompt
                    result = prompt_high_entry(self.new_entry_amount)
                    if result == "no":
                        self.main_frame_refresh()
                        return
                # create uuid
                new_id = str(uuid.uuid4())
                creation_date = date.today().strftime("%m/%d/%y")
                entry_data = {"Account": self.selected_account_name,
                              "Entry Name": self.new_entry_name,
                              "Amount": self.new_entry_amount,
                              "Date": creation_date}
                self.selected_profile["Accounts"][self.selected_account_name]["Entries"][new_id] = entry_data
                entry_data = {"Account": self.selected_account_name,
                              "Entry Name": self.new_entry_name,
                              "Amount": self.new_entry_amount,
                              "Date": creation_date}
                self.selected_profile["Entries"][new_id] = entry_data
                self.selected_profile["Rolling Total"] = float(self.selected_profile["Rolling Total"]) + self.new_entry_amount
                self.selected_profile["Current Mark"] = float(self.selected_profile["Current Mark"]) + \
                                                        self.new_entry_amount / \
                                                        self.selected_profile["Accounts"].keys().__len__()
                self.selected_profile["Accounts"][self.selected_account_name]["Current Mark"] += self.new_entry_amount
                self.selected_profile["Accounts"][self.selected_account_name]["Total Entries"] = \
                    self.selected_profile["Accounts"][self.selected_account_name]["Total Entries"] + 1
                save_json(self.selected_profile_name, self.selected_profile)
                self.selected_account_name = None
                self.selected_account = None
                self.new_entry_amount = None
                self.selected_account_current_mark = None
                self.main_frame_refresh()
                return

    def get_account_names(self):
        for i in self.dict_files:
            if i["Profile"] == self.selected_profile_name:
                print("Profile found")
                self.selected_profile = i
                self.selected_profile_accounts = self.selected_profile["Accounts"].keys()
        return

    def undo_add_entry(self, event=None):

        return

    ###################################################################
    #   Add Profile Frame Methods

    profile_name = ""
    new_account = ""
    selected_account = ""
    accounts = []
    create_new_profile = False

    def add_profile_frame_refresh(self):
        counter = 0
        self.add_account_listbox.delete(0, END)
        for i in self.accounts:
            self.add_account_listbox.insert(counter, i)
            counter += 1
        return

    def add_profile(self, event=None):
        self.profile_name = self.add_profile_entry.get()
        self.accounts.clear()
        if self.profile_name.__len__() > 0:
            self.create_new_profile = True
            print(f"add_profile({self.profile_name}) -> New profile set.")
        else:
            self.create_new_profile = False
            print(f"add_profile({self.profile_name}) -> Must enter a valid profile name!")
        self.add_profile_entry.delete(0, END)
        self.add_profile_frame_refresh()
        return

    def add_account(self, event=None):
        if self.create_new_profile:
            self.new_account = self.add_account_name_entry.get()
            if self.new_account.__len__() > 0:
                if self.accounts.__contains__(self.new_account):
                    # Display warning
                    print(f"add_account({self.new_account}) -> Profile already contains account by same name.")
                    return
                else:
                    self.accounts.append(self.new_account)
                    self.add_account_name_entry.delete(0, END)
                    print(f"add_account({self.new_account}) -> New account added.")
            else:
                print(f"add_account() -> Must enter a valid account name.")
        else:
            print(f"add_account() -> No valid profile set.")
        self.add_profile_frame_refresh()
        return

    def undo_add_account(self, event=None):
        if self.new_account.__len__() > 0:
            if self.accounts.__contains__(self.new_account):
                self.accounts.remove(self.new_account)
                print(f"undo_add_account({self.new_account}) -> Account removed successfully.")
                return
        else:
            print(f"undo_add_account({self.new_account}) -> Account not removed.")
        self.add_profile_frame_refresh()
        return

    def delete_add_account(self, event=None):
        self.select_delete_account()
        if self.selected_account.__len__() > 0:
            if self.accounts.__contains__(self.selected_account):
                self.accounts.remove(self.selected_account)
                print(f"delete_add_account({self.selected_account}) -> Account deleted successfully.")
        else:
            print(f"delete_add_account({self.selected_account}) -> Account not deleted.")
        self.add_profile_frame_refresh()
        return

    def select_delete_account(self, event=None):
        self.selected_account = self.add_account_listbox.get(self.add_account_listbox.curselection())
        return

    def create_profile(self, event=None):
        if self.create_new_profile:
            if self.accounts.__len__() > 0:
                print(f"create_profile({self.profile_name, self.accounts}) -> Creating account.")
                create_profile_json(self.profile_name, self.accounts)
        self.create_new_profile = False
        self.accounts.clear()
        self.load_all_profiles()
        self.add_profile_frame_refresh()
        return

    def add_delete_profile(self, event=None):
        print(f"add_delete_profile({self.profile_name}) -> Profile creation cancelled.")
        self.profile_name = ""
        self.accounts.clear()
        self.create_new_profile = False
        self.selected_account = ""
        self.new_account = ""
        self.add_profile_frame_refresh()
        return

    ###################################################################
    #   Edit Profile Frame Methods

    edit_select_profile = None
    edit_select_profile_name = ""

    edit_select_profile_accounts = []

    edit_select_account = None
    edit_select_account_name = ""

    def edit_profile_frame_on_start(self):
        counter = 0
        self.edit_profile_listbox.delete(0, END)
        for i in self.profile_names:
            self.edit_profile_listbox.insert(counter, i)
            counter += 1
        return

    def edit_profile_frame_refresh(self):
        self.edit_account_listbox.delete(0, END)
        if self.edit_select_profile_name is not None:
            counter = 0
            for i in self.edit_select_profile_accounts:
                self.edit_account_listbox.insert(counter, i)
                counter += 1

        self.edit_entry_name_entry.configure(state="normal")
        self.edit_entry_amount_entry.configure(state="normal")

        self.edit_entry_name_entry.delete(0, END)
        self.edit_entry_amount_entry.delete(0, END)

        self.edit_entry_name_entry.configure(state="disabled")
        self.edit_entry_amount_entry.configure(state="disabled")
        self.fill_entries()
        return

    def edit_select_profile(self, event=None):
        self.edit_select_profile_name = self.edit_profile_listbox.get(self.edit_profile_listbox.curselection())
        self.edit_select_account_name = ""
        for i in self.dict_files:
            if i["Profile"] == self.edit_select_profile_name:
                print("Profile found")
                self.edit_select_profile = i
                self.edit_select_profile_accounts = self.edit_select_profile["Accounts"].keys()
        self.fill_entries()
        self.edit_profile_frame_refresh()
        return

    def edit_select_account(self, event=None):
        self.edit_select_account_name = self.edit_account_listbox.get(self.edit_account_listbox.curselection())
        self.edit_select_account = self.edit_select_profile["Accounts"][self.edit_select_account_name]
        self.fill_entries()
        return

    # TODO make sure iterating through new entry system works

    def fill_entries(self):
        if self.edit_select_profile_name.__len__() > 0 and self.edit_select_account_name.__len__() == 0:
            self.view_entries_listbox.delete(0, END)
            entries = self.edit_select_profile["Entries"]
            counter = 0
            entry_ids = self.edit_select_profile["Entries"].keys()
            for i in entry_ids:
                account = self.edit_select_profile["Entries"][i]["Account"]
                amount = self.edit_select_profile["Entries"][i]["Amount"]
                entry_date = self.edit_select_profile["Entries"][i]["Date"]
                line = f"{account} | {amount} | {entry_date}                    {i}"
                self.view_entries_listbox.insert(counter, line)
                counter += 1
            return
        elif self.edit_select_account_name.__len__() > 0:
            self.view_entries_listbox.delete(0, END)
            entry_ids = self.edit_select_account["Entries"].keys()
            counter = 0
            for i in entry_ids:
                account = self.edit_select_account["Entries"][i]["Account"]
                amount = self.edit_select_account["Entries"][i]["Amount"]
                entry_date = self.edit_select_account["Entries"][i]["Date"]
                line = f"{account} | {amount} | {entry_date}                    {i}"
                self.view_entries_listbox.insert(counter, line)
                counter += 1
            return
        else:
            self.view_entries_listbox.delete(0, END)
            return

    selected_entry = ""
    selected_entry_id = ""
    selected_entry_account_name = ""

    def select_entry(self, event=None):
        self.selected_entry = self.view_entries_listbox.get(self.view_entries_listbox.curselection())
        self.selected_entry = self.selected_entry.replace("|", "")
        entry = self.selected_entry.split()
        entry_id = entry[3]
        name = entry[0]
        amount = entry[1]
        self.selected_entry_id = entry_id
        self.selected_entry_account_name = name
        self.edit_entry_name_entry.configure(state="normal")
        self.edit_entry_name_entry.insert(0, name)
        self.edit_entry_name_entry.configure(state="disabled")
        self.edit_entry_amount_entry.configure(state="normal")
        self.edit_entry_amount_entry.insert(0, amount)
        return

    def save_entry(self, event=None):
        edit_date = date.today().strftime("%m/%d/%y")
        new_amount = float(self.edit_entry_amount_entry.get())

        self.edit_select_profile["Entries"][self.selected_entry_id]["Edit Date"] = edit_date
        original_amount = float(self.edit_select_profile["Entries"][self.selected_entry_id]["Amount"])
        self.edit_select_profile["Entries"][self.selected_entry_id]["Amount"] = new_amount
        self.edit_select_profile["Entries"][self.selected_entry_id]["Original Amount"] = original_amount
        self.edit_select_profile["Rolling Total"] = \
            float(self.edit_select_profile["Rolling Total"] - (original_amount - new_amount))
        num_accounts = self.edit_select_profile["Accounts"].keys().__len__()
        self.edit_select_profile["Current Mark"] = \
            float(self.edit_select_profile["Current Mark"] - ((original_amount - new_amount) / num_accounts))

        self.edit_select_profile["Accounts"][self.selected_entry_account_name]["Entries"][self.selected_entry_id]["Edit Date"] = edit_date
        self.edit_select_profile["Accounts"][self.selected_entry_account_name]["Entries"][self.selected_entry_id]["Amount"] = new_amount
        self.edit_select_profile["Accounts"][self.selected_entry_account_name]["Entries"][self.selected_entry_id]["Original Amount"] = original_amount
        self.edit_select_profile["Accounts"][self.selected_entry_account_name]["Current Mark"] -= float(original_amount - new_amount)
        save_json(self.edit_select_profile_name, self.edit_select_profile)
        self.edit_profile_frame_refresh()
        return

    # TODO Set entry dictionary key as the UUID then use del UUID or pop(UUID)

    def delete_entry(self, event=None):
        # Get entry amount that is being deleted
        entry_amount = float(self.edit_select_profile["Entries"][self.selected_entry_id]["Amount"])
        # Reflect changes to json of amount being removed
        self.edit_select_profile["Rolling Total"] = self.edit_select_profile["Rolling Total"] - entry_amount
        self.edit_select_profile["Current Mark"] = self.edit_select_profile["Current Mark"] - \
                                                    (entry_amount / (self.edit_select_profile["Accounts"].keys().__len__()))
        self.edit_select_profile["Accounts"][self.selected_entry_account_name ]["Current Mark"] -= entry_amount
        # Delete both instances of the entry
        # self.edit_select_profile["Entries"].pop(self.selected_entry_id)
        # self.edit_select_profile["Accounts"][self.edit_select_account_name]["Entries"].pop(self.selected_entry_id)
        del self.edit_select_profile["Entries"][self.selected_entry_id]
        del self.edit_select_profile["Accounts"][self.selected_entry_account_name]["Entries"][self.selected_entry_id]
        # Save changes
        save_json(self.edit_select_profile_name, self.edit_select_profile)
        self.edit_profile_frame_refresh()
        return

    ###################################################################
    #   Init

    def __init__(self, master):

        root.geometry("450x290")
        root.title("MarkTracker")
        root.resizable(width=False, height=False)

        ###################################################################
        #   Main Frame

        self.main_frame = Frame(master)
        self.main_frame.grid(row=0, column=0, sticky=NW)

        ###################################################################
        #   Left Panel

        self.main_left_panel = Frame(self.main_frame)
        self.main_left_panel.grid(row=0, column=0, sticky=NW, padx=10)

        self.profile_listbox_label = Label(self.main_left_panel, text="Profiles")
        self.profile_listbox_label.grid(row=0, column=0, sticky=W, padx=10, pady=0)

        self.profile_listbox = Listbox(self.main_left_panel, height=5, selectmode=SINGLE)
        self.profile_listbox.grid(row=1, column=0, padx=10, pady=0)

        self.profile_select_button = Button(self.main_left_panel, text="Select Profile")
        self.profile_select_button.bind("<Button-1>", self.select_profile)
        self.profile_select_button.grid(row=2, column=0, sticky=E, padx=10, pady=2)

        self.account_listbox_label = Label(self.main_left_panel, text="Accounts")
        self.account_listbox_label.grid(row=3, column=0, sticky=W, padx=10, pady=0)

        self.account_listbox = Listbox(self.main_left_panel, height=5, selectmode=SINGLE)
        self.account_listbox.bind('<Button-1>', self.selected_account)
        self.account_listbox.grid(row=4, column=0, padx=10, pady=0)

        self.account_select_button = Button(self.main_left_panel, text="Select Account")
        self.account_select_button.bind("<Button-1>", self.select_account)
        self.account_select_button.grid(row=5, column=0, sticky=E, padx=10, pady=2)

        ###################################################################
        #   Right Panel

        self.main_right_panel = Frame(self.main_frame)
        self.main_right_panel.grid(row=0, column=1, sticky=NE, padx=10)

        ###################################################################
        #   Right Top Panel

        self.main_right_top_panel = Frame(self.main_right_panel)
        self.main_right_top_panel.grid(row=0, column=0, sticky=N, pady=65)

        self.rolling_total_label = Label(self.main_right_top_panel, text="Rolling Total")
        self.rolling_total_label.grid(row=0, column=0, sticky=NW, pady=0)

        self.rolling_total_entry = Entry(self.main_right_top_panel, width=20)
        self.rolling_total_entry.configure(state="disabled")
        self.rolling_total_entry.grid(row=1, column=0, sticky=W, pady=0)

        self.current_mark_label = Label(self.main_right_top_panel, text="Current Mark")
        self.current_mark_label.grid(row=0, column=1, sticky=W, padx=10, pady=0)

        self.current_mark_entry = Entry(self.main_right_top_panel, width=20)
        self.current_mark_entry.configure(state="disabled")
        self.current_mark_entry.grid(row=1, column=1, sticky=W, padx=10, pady=0)

        ###################################################################
        #   Right Bottom Panel

        self.main_right_bottom_panel = Frame(self.main_right_panel)
        self.main_right_bottom_panel.grid(row=1, column=0, sticky=N, pady=0)

        self.main_name_label = Label(self.main_right_bottom_panel, text="Name")
        self.main_name_label.grid(row=0, column=0, sticky=W, pady=0)

        self.main_name_entry = Entry(self.main_right_bottom_panel, width=20)
        self.main_name_entry.configure(state="disabled")
        self.main_name_entry.grid(row=1, column=0, sticky=W, pady=0)

        self.main_current_mark_label = Label(self.main_right_bottom_panel, text="Current Mark")
        self.main_current_mark_label.grid(row=0, column=1, sticky=W, padx=5, pady=0)

        self.main_current_mark_entry = Entry(self.main_right_bottom_panel, width=20)
        self.main_current_mark_entry.configure(state="disabled")
        self.main_current_mark_entry.grid(row=1, column=1, sticky=W, padx=5, pady=0)

        self.main_new_entry_name_label = Label(self.main_right_bottom_panel, text="Entry Name")
        self.main_new_entry_name_label.grid(row=2, column=0, sticky=W, padx=0, pady=0)

        self.main_new_entry_amount_label = Label(self.main_right_bottom_panel, text="Amount")
        self.main_new_entry_amount_label.grid(row=2, column=1, sticky=W, padx=0, pady=0)

        self.main_new_entry_name_entry = Entry(self.main_right_bottom_panel, width=20)
        self.main_new_entry_name_entry.configure(state="disabled")
        self.main_new_entry_name_entry.grid(row=3, column=0, sticky=W, padx=0, pady=0)

        self.main_new_entry = Entry(self.main_right_bottom_panel, width=20)
        self.main_new_entry.configure(state="disabled")
        self.main_new_entry.grid(row=3, column=1, sticky=W, padx=5, pady=0)

        self.main_new_entry_button = Button(self.main_right_bottom_panel, text="Add")
        self.main_new_entry_button.bind("<Button-1>", self.add_entry)
        self.main_new_entry_button.grid(row=4, column=1, sticky=E, padx=5, pady=5)

        self.main_new_entry_undo_button = Button(self.main_right_bottom_panel, text="Undo")
        # self.main_new_entry_undo_button.bind("<Button-1>", self.undo_entry)


        ###################################################################
        #   Add Profile Frame

        self.add_profile_frame = Frame(master)

        self.add_profile_name_label = Label(self.add_profile_frame, text="New Profile Name")
        self.add_profile_name_label.grid(row=0, column=0, padx=1, pady=5)

        self.add_profile_entry = Entry(self.add_profile_frame, width=20)
        self.add_profile_entry.grid(row=1, column=0, padx=1, pady=5)

        self.add_profile_button = Button(self.add_profile_frame, text="Add")
        self.add_profile_button.bind("<Button-1>", self.add_profile)
        self.add_profile_button.grid(row=1, column=1, padx=1, pady=1)

        self.add_account_name_label = Label(self.add_profile_frame, text="New Account Name")
        self.add_account_name_label.grid(row=0, column=2, padx=5, pady=5)

        self.add_account_name_entry = Entry(self.add_profile_frame, width=20)
        self.add_account_name_entry.grid(row=1, column=2, padx=5, pady=5)

        self.add_account_button = Button(self.add_profile_frame, text="Add")
        self.add_account_button.bind("<Button-1>", self.add_account)
        self.add_account_button.grid(row=1, column=3, padx=5, pady=5)

        self.add_account_undo_button = Button(self.add_profile_frame, text="Undo")
        self.add_account_undo_button.bind("<Button-1>", self.undo_add_account)

        self.add_account_listbox = Listbox(self.add_profile_frame, height=4, selectmode=SINGLE)
        self.add_account_listbox.grid(row=2, column=0, padx=5, pady=5)

        self.add_account_delete_button = Button(self.add_profile_frame, text="Delete")
        self.add_account_delete_button.bind("<Button-1>", self.delete_add_account)
        self.add_account_delete_button.grid(row=3, column=0, sticky=E, padx=5, pady=5)

        self.create_profile_button = Button(self.add_profile_frame, text="Create")
        self.create_profile_button.bind("<Button-1>", self.create_profile)
        self.create_profile_button.grid(row=3, column=2, sticky=E, padx=5, pady=5)

        self.add_profile_delete_button = Button(self.add_profile_frame, text="Delete")
        self.add_profile_delete_button.bind("<Button-1>", self.add_delete_profile)
        self.add_profile_delete_button.grid(row=3, column=3, padx=5, pady=5)

        ###################################################################
        #   Edit Profile Frame

        self.edit_profile_frame = Frame(master)

        ###################################################################
        #   Edit Profile Top Frame

        self.edit_profile_top_frame = Frame(self.edit_profile_frame)
        self.edit_profile_top_frame.grid(row=0, column=0, sticky=NW, padx=1, pady=5)

        ###################################################################
        #   Edit Profile Top Left Frame

        self.edit_profile_left_frame = Frame(self.edit_profile_top_frame)
        self.edit_profile_left_frame.grid(row=0, column=0, padx=1, pady=1)

        self.edit_profile_listbox_label = Label(self.edit_profile_left_frame, text="Profiles")
        self.edit_profile_listbox_label.grid(row=0, column=0, sticky=W, padx=5, pady=1)

        self.edit_profile_listbox = Listbox(self.edit_profile_left_frame, height=4, selectmode=SINGLE)
        self.edit_profile_listbox.grid(row=1, column=0, padx=5, pady=2)

        self.edit_profile_select_button = Button(self.edit_profile_left_frame, text="Select Profile")
        self.edit_profile_select_button.bind("<Button-1>", self.edit_select_profile)
        self.edit_profile_select_button.grid(row=2, column=0, sticky=E, padx=5, pady=1)

        self.edit_account_listbox_label = Label(self.edit_profile_left_frame, text="Accounts")
        self.edit_account_listbox_label.grid(row=3, column=0, sticky=W, padx=5, pady=1)

        self.edit_account_listbox = Listbox(self.edit_profile_left_frame, height=4, selectmode=SINGLE)
        self.edit_account_listbox.grid(row=4, column=0, padx=5, pady=2)

        self.edit_account_select_button = Button(self.edit_profile_left_frame, text="Select Account")
        self.edit_account_select_button.bind("<Button-1>", self.edit_select_account)
        self.edit_account_select_button.grid(row=5, column=0, sticky=E, padx=5, pady=1)

        ###################################################################
        #   Edit Profile Top Right Frame

        self.edit_profile_right_frame = Frame(self.edit_profile_top_frame)
        self.edit_profile_right_frame.grid(row=0, column=1, sticky=E, padx=20, pady=0)

        self.view_entries_label = Label(self.edit_profile_right_frame, text="Entries")
        self.view_entries_label.grid(row=0, column=0, sticky=W, padx=0, pady=0)

        self.entries_scrollbar = Scrollbar(self.edit_profile_right_frame, orient=VERTICAL)

        self.view_entries_listbox = Listbox(self.edit_profile_right_frame, height=11, selectmode=SINGLE,
                                            yscrollcommand=self.entries_scrollbar.set)

        self.entries_scrollbar.config(command=self.view_entries_listbox.yview)
        self.entries_scrollbar.grid(row=1, column=1, sticky=W)

        self.view_entries_listbox.grid(row=1, column=0, sticky=E, padx=1, pady=0)

        self.select_entry_button = Button(self.edit_profile_right_frame, text="Select")
        self.select_entry_button.bind("<Button-1>", self.select_entry)
        self.select_entry_button.grid(row=2, column=0, sticky=SE, padx=1, pady=5)

        ###################################################################

        #   Edit Entry Frame

        self.edit_entry_frame = Frame(self.edit_profile_frame)
        self.edit_entry_frame.grid(row=1, column=0, sticky=SW, padx=1, pady=1)

        self.edit_entry_name_label = Label(self.edit_entry_frame, text="Name")
        self.edit_entry_name_label.grid(row=0, column=0, sticky=W, padx=1, pady=1)

        self.edit_entry_name_entry = Entry(self.edit_entry_frame, width=20)
        self.edit_entry_name_entry.configure(state="disabled")
        self.edit_entry_name_entry.grid(row=1, column=0, padx=1, pady=1)

        self.edit_entry_amount_label = Label(self.edit_entry_frame, text="Amount")
        self.edit_entry_amount_label.grid(row=0, column=1, sticky=W, padx=1, pady=1)

        self.edit_entry_amount_entry = Entry(self.edit_entry_frame, width=20)
        self.edit_entry_amount_entry.configure(state="disabled")
        self.edit_entry_amount_entry.grid(row=1, column=1, padx=1, pady=1)

        self.edit_entry_save_button = Button(self.edit_entry_frame, text="Save")
        self.edit_entry_save_button.bind("<Button-1>", self.save_entry)
        self.edit_entry_save_button.grid(row=1, column=2, sticky=E, padx=1, pady=1)

        self.edit_entry_delete_button = Button(self.edit_entry_frame, text="Delete")
        self.edit_entry_delete_button.bind("<Button-1>", self.delete_entry)
        self.edit_entry_delete_button.grid(row=2, column=2, sticky=E, padx=1, pady=1)

        ###################################################################
        #   Menu Bar

        self.the_menu = Menu(master)
        self.file_menu = Menu(self.the_menu, tearoff=0)

        self.file_menu.add_command(label="Add Profile", command=self.load_add_profile_frame)
        self.file_menu.add_command(label="Edit Profile", command=self.load_edit_profile_frame)
        self.file_menu.add_command(label="Save", command=None)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Return to Home", command=self.load_main_frame)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit Application", command=quit_app)

        # View menu
        self.view_menu = Menu(self.the_menu, tearoff=0)

        self.the_menu.add_cascade(label="File", menu=self.file_menu)

        root.config(menu=self.the_menu)

        self.on_start()
        return


def quit_app():
    root.quit()


if __name__ == '__main__':
    root = Tk()
    app = APP(root)
    root.mainloop()
