# Wildlife-Test
Simple program with a GUI that tests your knowledge of identifying species. Inspired by a course I took in university where I had to learn to identify species but forgot most of them. Currently, only bird species found in Ontario are available in the Images directory.

# How It Works
Images are saved in the "Images" directory with each species having its own subdirectory. The program determines the name of the species based on the name of the subdirectory where the images are contained so make sure to double check the spelling of the name. 

To play, run wildlife_test.py. Capitalization does not matter for answers. You can also use the Up Arrow and Down Arrow keys to go through your previously submitted answers (if the same species shows up twice in a row let's say, then you can press Up Arrow instead of typing its name all over again).

# Known Issues
- The test ends 1 too early (e.g. if there are 9 images in total then it will end on 8 and show your score out of 8).

# To Do
- Center the widgets on the window and make sure they remain centered if window is resized
- Add species categories (e.g. birds, reptiles, mammals, etc.)
- Add a start page with options the user can change before beginning the game
  - Add an option for the user to change the number of images they are tested on (currently it tests all the images so if there are 300 you will have to go through all 300 to      reach the end)
  - Once species categories are added, add an option to let the user choose what category they are tested on (dropdown list of all available categories)
  
