"""Calvin Kim - CS 5001 - Day 9 - Project 9 / Lab 9: TKinter Window"""

import tkinter as tk
import tkinter.ttk as ttk
import jsonpickle


def get_config_data(
    trees, tree_size, babies, flock_size, adult_size, baby_size, flyer_size
):
    """Checks for valid inputs and gets config data from tk window."""
    try:
        trees = int(trees.get())
        tree_size = int(tree_size.get())
        babies = int(babies.get())
        flock_size = int(flock_size.get())
        adult_size = int(adult_size.get())
        baby_size = int(baby_size.get())
        flyer_size = int(flyer_size.get())

        config_data = {
            "trees": trees,
            "tree_size": tree_size,
            "babies": babies,
            "flock_size": flock_size,
            "adult_size": adult_size,
            "baby_size": baby_size,
            "flyer_size": flyer_size,
        }

        if (
            (trees > 20 or trees < 12)
            or (tree_size > 200 or tree_size < 100)
            or (babies > 6 or babies < 2)
            or (flock_size > 7 or flock_size < 3)
            or (adult_size > 75 or adult_size < 60)
            or (baby_size > 35 or baby_size < 15)
            or (flyer_size > 30 or flyer_size < 15)
        ):
            raise OutOfRangeError("Values must be in valid range.")

        with open(
            file="/Users/calvinkim/Desktop/cs_5001/Module 9/Project 9/config.json",
            mode="w",
        ) as config_file:
            config_data_str = jsonpickle.encode(config_data, indent=2)
            config_file.write(config_data_str)

        print("Success")  # Replace with a tkinter window
    except OutOfRangeError as err:
        print(err)  # Replace with a tkinter window
    except ValueError:
        print(
            "Must fill out all input fields and inputs must be numbers."
        )  # Replace with a tkinter window
    except FileNotFoundError:
        print(
            "File not found. Check the absolute path of the file location in the open function."
        )  # Replace with a tkinter window


class OutOfRangeError(ValueError):
    """Exception that handles values that are out of range"""

    def __init__(self, *args):
        super().__init__(*args)


class App:
    """Main app class"""

    def run(self):
        """Runs the tk window"""
        # Run the Config UI
        self.root = tk.Tk()
        self.root.title("Into The Forest")
        my_frame = ttk.Frame(self.root, padding=10)
        my_frame.grid()

        # Config 1
        ttk.Label(my_frame, text="Amount of Trees (Between 12-20):").grid(
            row=0, column=0
        )
        trees = tk.StringVar()
        ttk.Entry(my_frame, textvariable=trees).grid(row=0, column=1)

        # Config 2
        ttk.Label(my_frame, text="Tree Size (Between 100-200):").grid(row=1, column=0)
        tree_size = tk.StringVar()
        ttk.Entry(my_frame, textvariable=tree_size).grid(row=1, column=1)

        # Config 3
        ttk.Label(my_frame, text="Amount of Babies (Between 2-6):").grid(
            row=2, column=0
        )
        babies = tk.StringVar()
        ttk.Entry(my_frame, textvariable=babies).grid(row=2, column=1)

        # Config 4
        ttk.Label(my_frame, text="Flock Size (Between 3-7):").grid(row=3, column=0)
        flock_size = tk.StringVar()
        ttk.Entry(my_frame, textvariable=flock_size).grid(row=3, column=1)

        # Config 5
        ttk.Label(my_frame, text="Adult Size (Between 60-75):").grid(row=4, column=0)
        adult_size = tk.StringVar()
        ttk.Entry(my_frame, textvariable=adult_size).grid(row=4, column=1)

        # Config 6
        ttk.Label(my_frame, text="Baby Size (Between 15-35):").grid(row=5, column=0)
        baby_size = tk.StringVar()
        ttk.Entry(my_frame, textvariable=baby_size).grid(row=5, column=1)

        # Config 7
        ttk.Label(my_frame, text="Flyer Size (Between 15-30):").grid(row=6, column=0)
        flyer_size = tk.StringVar()
        ttk.Entry(my_frame, textvariable=flyer_size).grid(row=6, column=1)

        # Button
        ttk.Button(
            my_frame,
            text="Into the forest!",
            command=lambda: get_config_data(
                trees, tree_size, babies, flock_size, adult_size, baby_size, flyer_size
            ),
        ).grid(row=7, column=1)

        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
