from tkinter import *
from tkinter import ttk
from os import listdir
from os.path import isfile, join, normpath, basename
from PIL import ImageTk, Image
from random import choice


class SpeciesCategory:

    def __init__(self, path, name="use path"):
        if name == "use path":
            self.name = basename(normpath(path))
        else:
            self.name = name
        self.path = path
        self.image_files = [f for f in listdir(path) if isfile(join(path, f))]


class Program(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, *kwargs)

        Tk.wm_title(self, "Wildlife Test")
        self.geometry("600x600")

        container = Frame(self)
        container.grid(sticky="nsew")
        # can configure each individual row i.e. if you wanted to change the
        # properties of row 2 you would use grid_rowconfigure(2)
        # weight determines to what extent it stretches to resize when widgets are resized
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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

        # Create instance for each species
        for species in self.species_name_list:
            self.species_dict[species] = SpeciesCategory(self.images_path + species)

        self.current_card = None
        self.current_img = None
        self.current_img_file = None

        # Store text in cache
        self.text_cache = ["" for i in range(0, 11)]
        self.text_cache_index = 0
        controller.bind("<Up>", self.prev_text_cache)
        controller.bind("<Down>", self.next_text_cache)

        # Image
        self.image_panel = Label(parent)
        self.image_panel.grid(row=0, column=0)
        self.next_image()

        # Textbox
        self.textbox = Text(parent, height=1, width=30)
        self.textbox.grid(row=1, column=0)
        controller.bind("<Return>", self.verify_answer_enter_pressed)

        # Next Button
        self.next_button = ttk.Button(parent, text="Submit", command=self.verify_answer)
        self.next_button.grid(row=2, column=0)

        # Skip Button
        self.skip_button = ttk.Button(parent, text="Skip", command=self.skip)
        self.skip_button.grid(row=3, column=0)

        # Wrong/Right Text
        self.wrongright = Label(parent, text="Type the common name of the species (capitalization matters)", fg="black")
        self.wrongright.grid(row=4, column=0)

    def next_image(self):
        while True:
            try:
                self.current_card = choice(self.species_name_list)
            except IndexError:
                self.display_end_text()
                return
            try:
                self.current_img_file = choice(self.species_dict[self.current_card].image_files)
                break
            except IndexError:
                self.species_name_list.remove(self.current_card)
                del self.species_dict[self.current_card]
        self.current_img = Image.open(self.images_path + self.current_card + "/" + self.current_img_file)
        image_width = self.current_img.width
        image_height = self.current_img.height
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
        user_answer = self.textbox.get("1.0", END).strip()
        if user_answer.lower() == self.current_card.lower():
            self.display_default_info_text()
            self.add_text_cache(user_answer)
            try:
                self.species_dict[self.current_card].image_files.remove(self.current_img_file)
                self.next_image()
                self.n_correct += 1
            except KeyError:
                self.display_end_text()
        else:
            self.display_incorrect_text()
        self.textbox.delete("1.0", END)

    def verify_answer(self):
        user_answer = self.textbox.get("1.0", END).strip()
        if user_answer.lower() == self.current_card.lower():
            self.display_default_info_text()
            self.add_text_cache(user_answer)
            try:
                self.species_dict[self.current_card].image_files.remove(self.current_img_file)
                self.next_image()
                self.n_correct += 1
            except KeyError:
                self.display_end_text()
        else:
            self.display_incorrect_text()
        self.textbox.delete("1.0", END)

    def skip(self):
        self.display_default_info_text()
        try:
            self.species_dict[self.current_card].image_files.remove(self.current_img_file)
            self.next_image()
            self.n_incorrect += 1
        except KeyError:
            self.display_end_text()

    def display_incorrect_text(self):
        self.wrongright.config(text="Incorrect", fg="red")

    def display_default_info_text(self):
        self.wrongright.config(text="Type the common name of the species", fg="black")

    def prev_text_cache(self, event):
        if not self.text_cache_index == len(self.text_cache) - 1 and self.text_cache[self.text_cache_index + 1] != "":
            self.text_cache_index += 1
            self.textbox.delete("1.0", END)
            self.textbox.insert("1.0", self.text_cache[self.text_cache_index])

    def next_text_cache(self, event):
        if not self.text_cache_index == 0:
            self.text_cache_index -= 1
            self.textbox.delete("1.0", END)
            self.textbox.insert("1.0", self.text_cache[self.text_cache_index])

    def add_text_cache(self, text):
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
        self.image_panel.destroy()
        self.textbox.destroy()
        self.next_button.destroy()
        self.skip_button.destroy()
        self.wrongright.destroy()
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

