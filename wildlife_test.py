from tkinter import *
from tkinter import ttk
from os import listdir
from os.path import isfile, join, normpath, basename
from PIL import ImageTk, Image
from random import choice


class SpeciesCategory:

    def __init__(self, path, name="use path"):
        """This class holds information that has to do with one species. Such as its name, path, and the filenames of
        all images in its subdirectory."""
        if name == "use path":
            self.name = basename(normpath(path))
        else:
            self.name = name
        self.path = path
        self.image_files = [f for f in listdir(path) if isfile(join(path, f))]


class Program(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, *kwargs)

        # Title of the window
        Tk.wm_title(self, "Wildlife Test")
        # Initial size of the window
        self.geometry("600x600")

        container = Frame(self)
        container.grid(sticky="nsew")
        # can configure each individual row i.e. if you wanted to change the
        # properties of row 2 you would use grid_rowconfigure(2)
        # weight determines to what extent it stretches to resize when widgets are resized
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create the frame which contains the game and launch it
        frame = Game(container, self)
        frame.grid(sticky="nsew")
        frame.tkraise()


class Game(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        # Internal Variables
        self.images_path = "./Images/"
        self.species_name_list = [sp for sp in listdir(self.images_path)]
        self.species_dict = {}
        self.n_correct = 0
        self.n_incorrect = 0
        self.n_total = 0

        # Create instance of SpeciesCategory for each species
        for species in self.species_name_list:
            self.species_dict[species] = SpeciesCategory(self.images_path + species)

        # Initialize these variables to be used below
        self.current_species_name = None
        self.current_img = None
        self.current_img_file = None

        # Store text in cache. The cache lets you use up arrow and down arrow to cycle through your previous answers
        # Currently the cache can hold the last 10 answers
        self.text_cache_size = 10
        self.text_cache = ["" for i in range(0, self.text_cache_size + 1)]
        self.text_cache_index = 0
        # Bind up arrow to move up the cache and down arrow to move down the cache
        controller.bind("<Up>", self.text_cache_up)
        controller.bind("<Down>", self.text_cache_down)

        # Image Widget
        self.image_panel = Label(parent)
        self.image_panel.grid(row=0, column=0)
        self.next_image()

        # Textbox Widget
        self.textbox = Text(parent, height=1, width=30)
        self.textbox.grid(row=1, column=0)
        controller.bind("<Return>", self.verify_answer_enter_pressed)

        # Next Button
        self.next_button = ttk.Button(parent, text="Submit", command=self.verify_answer)
        self.next_button.grid(row=2, column=0)

        # Skip Button
        self.skip_button = ttk.Button(parent, text="Skip", command=self.skip)
        self.skip_button.grid(row=3, column=0)

        # Info Label (text below the Skip button which shows instructions and if you were incorrect)
        self.info_label = Label(parent, text="Type the common name of the species", fg="black")
        self.info_label.grid(row=4, column=0)

    def next_image(self):
        # Try to get the next image. If index error is thrown it means there is nothing left in the list and the game is over
        while True:
            try:
                self.current_species_name = choice(self.species_name_list)
            except IndexError:
                self.display_end_text()
                return
            # Get the actual filename of the image. If index error is thrown it means there's no files left in that
            # species' directory so the species as a whole must be removed from the list of species still in the game
            try:
                self.current_img_file = choice(self.species_dict[self.current_species_name].image_files)
                break
            except IndexError:
                self.species_name_list.remove(self.current_species_name)
                del self.species_dict[self.current_species_name]

        # Open image and get its width and height
        self.current_img = Image.open(self.images_path + self.current_species_name + "/" + self.current_img_file)
        image_width = self.current_img.width
        image_height = self.current_img.height
        # Change its width and height depending on how big the image is so that it can fit on the screen
        # If the image is really big its size is divided by 4, if its medium-sized then it's divided by 2
        # otherwise it's left as is. The numbers they are divided by and the size thresholds are completely arbitrary
        if image_width >= 1000 or image_height >= 1000:
            resized_width = image_width // 4
            resized_height = image_height // 4
        elif image_width >= 500 or image_height >= 600:
            resized_width = image_width // 2
            resized_height = image_height // 2
        else:
            resized_width = image_width // 1
            resized_height = image_height // 1
        self.current_img = self.current_img.resize((resized_width, resized_height), Image.ANTIALIAS)
        self.current_img = ImageTk.PhotoImage(self.current_img)
        self.image_panel.config(image=self.current_img)

    def verify_answer_enter_pressed(self, event):
        """This is the verify method that runs when the Enter key is pressed. It is separate to the other verify
        answer method because tkinter forces you to make it have a parameter that will take the triggering event
        as input. If that 'event' parameter wasn't there it wouldn't work even though I never use that parameter anywhere"""
        user_answer = self.textbox.get("1.0", END).strip()
        # Check the user's answer to the actual answer. Everything converted to lowercase so capitalization does
        # not matter. If you want to make capitalization matter, remove the .lower()'s
        if user_answer.lower() == self.current_species_name.lower():
            self.display_default_info_text()
            self.text_cache_add(user_answer)
            try:
                self.species_dict[self.current_species_name].image_files.remove(self.current_img_file)
                self.next_image()
                self.n_correct += 1
            # I think this try and except statement might be pointless. The next_image method already runs
            # display_end_text if the end is reached so it might be redundant but I will have to double check
            except KeyError:
                self.display_end_text()
        else:
            self.display_incorrect_text()
        # Reset the textbox's contents otherwise the user presses Enter and it just goes to the next line.
        # The textbox will appear blank but actually the text remains in the line above not visible to the user unless
        # the contents are reset using the method below. Fun fact: this caused me a lot of frustration figuring out
        # why the first image worked perfectly but the second one would always say "incorrect" even when I had the
        # correct answer
        self.textbox.delete("1.0", END)

    def verify_answer(self):
        """Exact same as the verify_answer_enter_pressed method except this one does not take 'event' as an argument
        because this is the version that is triggered by pressing the Submit button instead of pressing the Enter key.
        Any modification to this method will have to be done to the other version of this method as well. There is
        probably a way to just have one verify answer method that works either way, something for the To Do list"""
        user_answer = self.textbox.get("1.0", END).strip()
        if user_answer.lower() == self.current_species_name.lower():
            self.display_default_info_text()
            self.text_cache_add(user_answer)
            try:
                self.species_dict[self.current_species_name].image_files.remove(self.current_img_file)
                self.next_image()
                self.n_correct += 1
            except KeyError:
                self.display_end_text()
        else:
            self.display_incorrect_text()
        self.textbox.delete("1.0", END)

    def skip(self):
        """This happens when the Skip button is pressed"""
        self.display_default_info_text()
        try:
            self.species_dict[self.current_species_name].image_files.remove(self.current_img_file)
            self.next_image()
            self.n_incorrect += 1
        # Try/Except block might be redundant as mentioned in the verify_answer_enter_pressed method's comments
        except KeyError:
            self.display_end_text()

    def display_incorrect_text(self):
        """Makes the 'Incorrect' text appear"""
        self.info_label.config(text="Incorrect", fg="red")

    def display_default_info_text(self):
        """Makes the default instruction text appear"""
        self.info_label.config(text="Type the common name of the species", fg="black")

    def text_cache_up(self, event):
        """When the Up Arrow key is pressed this gets the next item in the historical text cache"""
        if not self.text_cache_index == len(self.text_cache) - 1 and self.text_cache[self.text_cache_index + 1] != "":
            self.text_cache_index += 1
            self.textbox.delete("1.0", END)
            self.textbox.insert("1.0", self.text_cache[self.text_cache_index])

    def text_cache_down(self, event):
        """When the Down Arrow key is pressed this gets the previous item in the historical text cache"""
        if not self.text_cache_index == 0:
            self.text_cache_index -= 1
            self.textbox.delete("1.0", END)
            self.textbox.insert("1.0", self.text_cache[self.text_cache_index])

    def text_cache_add(self, text):
        """Adds a correct answer to the text cache"""
        for i in range(-1, 0 - len(self.text_cache), -1):
            if i == -1:
                continue
            elif i == 0 - len(self.text_cache) + 1:
                self.text_cache[i + 1] = self.text_cache[i]
                self.text_cache[i] = text
            elif i == 0 - len(self.text_cache):
                continue
            else:
                self.text_cache[i + 1] = self.text_cache[i]
        self.text_cache_index = 0

    def display_end_text(self):
        """This happens at the end of the game, displays the endgame text and score. Currently it destroys all the
        game's widgets and makes new ones. There is probably a way to switch frames using .tkraise() without having
        to destroy the widgets. That implementation would separate this method into its own class.Something for the
         To Do list."""
        self.image_panel.destroy()
        self.textbox.destroy()
        self.next_button.destroy()
        self.skip_button.destroy()
        self.info_label.destroy()
        end_text = Label(self.parent, text="End of Test")
        end_text.grid(row=0, column=0)
        self.n_total = self.n_correct + self.n_incorrect
        percent_correct = round((self.n_correct / self.n_total) * 100, 3)
        score_label = Label(self.parent, text=f"Score: {self.n_correct} / {self.n_total} = {percent_correct}%")
        score_label.grid(row=1, column=0)


def main():
    app = Program()
    app.mainloop()

main()

