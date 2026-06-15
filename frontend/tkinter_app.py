import tkinter as tk
from tkinter import messagebox

from state import app_data

try:
    from .api_client import add_numbers, combine_name
except ImportError:
    from api_client import add_numbers, combine_name


def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

# Add two numbers page and return the result from different pages
#--------------------------------------------------------------------------------------------
def show_add_page(root):
    clear_window(root)

    tk.Label(root, text="Adder Page").pack()

    tk.Label(root, text="A").pack()
    entry_a = tk.Entry(root)
    entry_a.pack()
    entry_a.insert(0, app_data["a"])

    tk.Label(root, text="B").pack()
    entry_b = tk.Entry(root)
    entry_b.pack()
    entry_b.insert(0, app_data["b"])

    result_label = tk.Label(root, text="Result:")
    result_label.pack()

    def calculate():
        try:
            app_data["a"] = entry_a.get().strip()
            app_data["b"] = entry_b.get().strip()

            a = int(app_data["a"])
            b = int(app_data["b"])

            result = add_numbers(a, b)
            result_label.config(text=f"Result: {result['result']}")

        except ValueError:
            messagebox.showerror("Input Error", "Enter valid integers")
        except Exception as e:
            result_label.config(text=f"Error: {e}")

    def next_page():
        app_data["a"] = entry_a.get().strip()
        app_data["b"] = entry_b.get().strip()
        show_first_name_page(root)

    tk.Button(root, text="Add", command=calculate).pack()
    tk.Button(root, text="Go to First Name Page", command=next_page).pack()


#--------------------------------------------------------------------------------------------
# Enter First name 
def show_first_name_page(root):
    clear_window(root)

    tk.Label(root, text="First Name Page").pack()

    tk.Label(root, text="Enter first name").pack()
    first_name_entry = tk.Entry(root)
    first_name_entry.pack()
    first_name_entry.insert(0, app_data["first_name"])

    def next_page():
        app_data["first_name"] = first_name_entry.get().strip()

        if not app_data["first_name"]:
            messagebox.showerror("Input Error", "Enter a first name")
            return

        show_last_name_page(root)

    tk.Button(root, text="Next", command=next_page).pack()
    tk.Button(root, text="Back to Add Page", command=lambda: show_add_page(root)).pack()

#--------------------------------------------------------------------------------------------
# Enter Last name and return the full name from different pages
def show_last_name_page(root):
    clear_window(root)

    tk.Label(root, text="Last Name Page").pack()
    tk.Label(root, text=f"First Name: {app_data['first_name']}").pack()

    tk.Label(root, text="Enter last name").pack()
    last_name_entry = tk.Entry(root)
    last_name_entry.pack()
    last_name_entry.insert(0, app_data["last_name"])

    result_label = tk.Label(root, text="Full Name:")
    result_label.pack()

    def submit_name():
        app_data["last_name"] = last_name_entry.get().strip()

        if not app_data["last_name"]:
            messagebox.showerror("Input Error", "Enter a last name")
            return

        try:
            result = combine_name(
                app_data["first_name"],
                app_data["last_name"]
            )

            full_name = result.get("full_name") or result.get("result")

            if full_name is None:
                raise KeyError("full_name")

            result_label.config(text=f"Full Name: {full_name}")

        except Exception as e:
            result_label.config(text=f"Error: {e}")

    tk.Button(root, text="Submit Name", command=submit_name).pack()
    tk.Button(root, text="Back", command=lambda: show_first_name_page(root)).pack()
    tk.Button(root, text="Back to Add Page", command=lambda: show_add_page(root)).pack()

#--------------------------------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Adder App")
    root.geometry("300x250")

    show_add_page(root)

    root.mainloop()


if __name__ == "__main__":
    main()
