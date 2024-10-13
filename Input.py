import pickle
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

def set_data(data):
    try:
        with open("Database.pkl", "wb") as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
    except pickle.PicklingError as e:
        print(str(e))

def get_data():
    try:
        with open("Database.pkl", "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        set_data({})
        return {}
    except pickle.UnpicklingError as e:
        print(str(e))
        return {}

def check_url(url):
    check = None
    if "amazon" in url:
        pattern = r'^(https?:\/\/(?:www\.)?)(amazon\.in\/)(?:[^\/]+\/)?(dp\/[A-Z0-9]{10})'
        check = re.match(pattern, url)
    elif "flipkart" in url:
        pattern = r'^(https?:\/\/(?:www\.)?)(flipkart.com\/)([-\w]+\/p\/[-\w]+(?=\?|\/|))'
        check = re.match(pattern, url)

    if check:
        url = check.group(1) + check.group(2) + check.group(3)
    else:
        url_entry.config(foreground="red")
        mb.showerror(title="Error", message="Given link is invalid. Please try again.")
        url_entry.delete(0, tk.END)
        url_entry.config(foreground=entry_txt_clr)
        url = None

    return url

def check_email(email):
    pattern = r'^[\w\-.]+@[\w\-]+\.[a-zA-z.]{2,5}$'
    check = re.match(pattern, email)
    if not check:
        email_entry.config(foreground="red")
        mb.showerror(title="Error", message="Given email ID is invalid. Please try again.")
        email_entry.delete(0, tk.END)
        email_entry.config(foreground=entry_txt_clr)
        email = None
    return email

def check_budget(budget):
    try:
        check = float(budget) > 0
        if not check:
            budget_entry.config(foreground="red")
            mb.showerror(title="Error", message="Budget should be positive. Please try again.")
            budget_entry.delete(0, tk.END)
            budget_entry.config(foreground=entry_txt_clr)
            budget = None
        return budget
    except:
        budget_entry.config(foreground="red")
        mb.showerror(title="Error", message="Budget should be a number. Please try again.")
        budget_entry.delete(0, tk.END)
        budget_entry.config(foreground=entry_txt_clr)
        return None

def toggle_radio_button():
    if rbutton_state.get() == 2:
        budget_label.grid_forget()
        budget_entry.grid_forget()
        button_frame.grid(row=4, column=0)
    else:
        budget_label.grid(row=4, column=0, padx=10, pady=10)
        budget_entry.grid(row=4, column=1, padx=5, pady=5)
        button_frame.grid(row=5, column=0)

def toggle_enter_button():
    data = get_data()

    url = url_entry.get()
    email = email_entry.get()
    budget = budget_entry.get()

    if rbutton_state.get() == 1:
        if not (url and email and budget):
            mb.showwarning(title="Warning", message="Do not leave any fields empty. Please try again.")
            return None

        if (url := check_url(url)) and (email := check_email(email)) and (budget := check_budget(budget)):
            is_ok = mb.askokcancel(title="Confirmation", message=f"Link: {url}\nEmail: {email}\nBudget: ₹{budget}\n\nDo you want to continue?")
            if is_ok:
                url_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                budget_entry.delete(0, tk.END)
                mb.showinfo(title="Info", message="Successfully stored given data.")
                data.setdefault(email, {})[url] = {-1: 0, 0: float(budget)}
                set_data(data)
    else:
        if not (url and email):
            mb.showwarning(title="Warning", message="Do not leave any fields empty. Please try again.")
            return None

        if (email := check_email(email)) and (url := check_url(url)):
            try:
                urls = data[email]
                if url in urls:
                    is_ok = mb.askokcancel(title="Confirmation", message=f"Email: {email}\nLink: {url}\n\nThis information will be permanently deleted. Do you want to continue?")
                    if is_ok:
                        url_entry.delete(0, tk.END)
                        email_entry.delete(0, tk.END)
                        budget_entry.delete(0, tk.END)
                        mb.showinfo(title="Info", message="Successfully deleted given link.")
                        del data[email][url]
                        if not data[email]:
                            del data[email]
                        set_data(data)
                else:
                    url_entry.config(foreground="red")
                    mb.showerror(title="Error", message="Given link not found. Please try again.")
                    url_entry.delete(0, tk.END)
                    url_entry.config(foreground=entry_txt_clr)
            except KeyError:
                email_entry.config(foreground="red")
                mb.showerror(title="Error", message="Given email ID not found. Please try again.")
                email_entry.delete(0, tk.END)
                email_entry.config(foreground=entry_txt_clr)

data = {}
url = ""
email = ""
budget = 0.0

bg_clr = "#A4B4C4"
info_label_clr = "#222831"
label_clr = "#000000"
entry_txt_clr = "#000000"
entry_bg_clr = "#EEEEEE"
rbutton_txt_clr = "#393E46"
rbutton_bg_clr = "#919FB1"
button_txt_clr = "#EEEEEE"
button_bg_clr1 = "#393E46"
button_bg_clr2 = "#4B86AC"


root = tk.Tk()
root.title("PyPriceTracker: Smart Shopping and Insights")
root.config(bg=bg_clr, padx=20, pady=20)

style = ttk.Style()

canvas = tk.Canvas(root, height=270, width=400, bg=bg_clr, highlightthickness=0)
logo_img = tk.PhotoImage(file="Logo.png")
canvas.create_image(160, 138, image=logo_img)

info_label = ttk.Label(root, text="Supported Websites: amazon.in, flipkart.com", style="InfoLabel.TLabel")

url_label = ttk.Label(root, text="Link:", style="Label.TLabel")
url_entry = ttk.Entry(root, width=38, font=("Lato", 12), style="Entry.TEntry")

email_label = ttk.Label(root, text="Email:", style="Label.TLabel")
email_entry = ttk.Entry(root, width=38, font=("Lato", 12), style="Entry.TEntry")

budget_label = ttk.Label(root, text="Budget:", style="Label.TLabel")
budget_entry = ttk.Entry(root, width=38, font=("Lato", 12), style="Entry.TEntry")

button_frame = ttk.Frame(style="ButtonFrame.TFrame")

rbutton_state = tk.IntVar()
rbutton_1 = ttk.Radiobutton(button_frame, text="Store", value=1, variable=rbutton_state, style="RButton.TRadiobutton", command=toggle_radio_button)
rbutton_2 = ttk.Radiobutton(button_frame, text="Delete", value=2, variable=rbutton_state, style="RButton.TRadiobutton", command=toggle_radio_button)
rbutton_state.set(1)

enter_button = ttk.Button(button_frame, text="Enter", style = "Button.TButton", command=toggle_enter_button)


style.theme_use("alt")
style.configure("InfoLabel.TLabel", font=("Arial Black", 15), background=bg_clr, foreground=info_label_clr)
style.configure("Label.TLabel", font=("Product Sans", 13), background=bg_clr, foreground=label_clr)

style.configure("Entry.TEntry", fieldbackground=entry_bg_clr, foreground=entry_txt_clr)

style.configure("ButtonFrame.TFrame", background=bg_clr)

style.configure("RButton.TRadiobutton", font=("Arial Black", 10), background=bg_clr, foreground=rbutton_txt_clr)

style.configure("Button.TButton", font=("Arial Black", 10), background=button_bg_clr1, foreground=button_txt_clr)

style.map("RButton.TRadiobutton", background=[("active", rbutton_bg_clr)])
style.map("Button.TButton", background=[("active", button_bg_clr2)])


canvas.grid(row=0, column=1)

info_label.grid(row=1, column=0, columnspan=3, pady=20)

url_label.grid(row=2, column=0, padx=10, pady=10)
url_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

email_label.grid(row=3, column=0, padx=10, pady=10)
email_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

budget_label.grid(row=4, column=0, padx=10, pady=10)
budget_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

button_frame.grid(row=5, column=0, columnspan=3)
rbutton_1.grid(row=0, column=0, padx=20, pady=30)
rbutton_2.grid(row=0, column=1)
enter_button.grid(row=0, column=2, padx=60, pady=50)


root.mainloop()

