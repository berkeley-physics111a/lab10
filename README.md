## Lab 10 Installation Instructions

### Prerequisite software

First, check through that everything from A.1-A.3 in Appendix A has been installed correctly. 

#### Python and dependencies

Open a terminal (or PowerShell, if on Windows) and run the command

```python3 --version```

You should get a version >= 3.11. If the first command doesn't work, try ```py3 --version``` and ```py --version```. Whichever of these commands works tells you what you should replace ```python3``` with in the commands that follow (i.e., if ```py3 --version``` gives you an acceptable version, you should be running ```py3 -m pip install [whatever]``` in the commands below instead of ```python3 -m pip install [whatever]```). If none of these work, there is something wrong with your Python install. See the 'Debugging Tips' section below.

![Image of terminal screen showing user testing py3 --version, py --version, and python3 --version, with only py --version running successfully. Instead of erroring, py --version prints Python 3.12.3, indicating the user is ready to proceed.](setup_instruction_pics/pythonversioncheck.jpg "Test of whether python is installed properly - on shown system, py is the correct command")

If you did get a version >= 3.11, run ```python3``` (or ```py3``` or ```py``` as appropriate) in your terminal (or PowerShell, if on Windows). This will open an interactive Python session. Run the following:

```import numpy```

```import matplotlib```

!["Image of terminal screen showing user running 'py' to start an interactive Python session, and then running import numpy and import matplotlib with no errors. The user then runs quit() to return to the regular terminal.](setup_instruction_pics/packageimportcheck.jpg "Test of whether packages are imported properly - you may need to replace py with python3 or py3 depending on your system")

These should just run successfully without producing any output. If there's an error, you need to install these packages. Use ```quit()``` to exit the interactive Python session and return to the main terminal (or PowerShell, if on Windows). Then run the following:

```python3 -m pip install --upgrade pip```

```python3 -m pip install numpy matplotlib```

The first upgrades pip, and the second installs two standard packages we will need. Run ```python3``` again to open the interactive Python session, and try the import statements again to make sure they worked. If they did not even once you have run pip install, see the 'Debugging Tips' section below.

#### Git

It is optional but highly recommended to install git. Git is version control software, much like the document history in a word processor like Google Docs, but designed for management of large codebases. You will likely use it in the future whether in graduate school or in industry. If you do not want to install it, proceed to the next section.

Install git following the instructions here: https://github.com/git-guides/install-git

Then, open your terminal (or PowerShell, if on Windows) again and run ```git```. If it does not error and gives you a help message, it was successfully installed; if it errors even after following the steps above, see the 'Debugging Tips' section.

!["Image of terminal screen showing user testing whether git is installed by running the command git. It is indeed installed successfully, so a lengthy help message is shown."](setup_instruction_pics/gitinstallcheck.jpg "Test of whether git is installed properly - it was, so it is showing a help message")

### Downloading the repository


#### With git

If you installed git, open the terminal (or PowerShell, if on Windows) and navigate to the directory you want the folder to be in. To do this, you can use the following commands:

```cd [name]``` will navigate inside the ```[name]``` folder/directory (replace ```[name]``` as appropriate).
```ls``` will list all of the files/folders within your current directory. (See below for image demonstrating their use.)

You can use tab to autocomplete folder/file names. Once inside the folder you want to save your code in, run the command

```git clone https://github.com/berkeley-physics111a/lab10```

!["A terminal window is open, with the git clone command given above run. The repository downloads successfully."](setup_instruction_pics/repositoryclone.png "Cloning the lab10 repository using git")

If you run ```ls``` again, you should now see a folder called ```lab10``` containing all the files from the repository.

#### Without git

If you did not install git, you may alternatively download the files individually. Make sure you are at https://github.com/berkeley-physics111a/lab10 (which you are presumably already at if you are reading this), go to the green "Code" drop-down menu, and select "Download ZIP". Then unzip the folder.

!["Image of Github page for the lab10 repository at given URL. The green code button drop down at the top right is selected, with several options in the resulting menu. The Download ZIP option at the bottom of this menu is circled in red."](setup_instruction_pics/repoinstallnogit.jpg "Location of Code button and Download ZIP (circled) for installing without git")

### Installing the last dependency

You should already have NumPy and Matplotlib installed; see the 'Prerequisite Software' section.

#### With git

In a Terminal window (or PowerShell, if on Windows), run the following command to install the software which controlls the ADS:

```python3 -m pip install git+https://github.com/Digilent/WaveForms-SDK-Getting-Started-PY#egg=WF_SDK```

Next, run ```python3``` in your terminal (or PowerShell, if on Windows) to open an interactive Python session. Run

```import WF_SDK```

If it runs without producing any output/erroring, it has installed successfully; run ```quit()``` to close the session - you are ready to begin the lab. If it errors, see the 'Debugging Tips' section.

#### Without git

In a Terminal window (or PowerShell, if on Windows), navigate inside the ```lab10``` folder you installed in the previous step. To do this, you can use the following commands:

```cd [name]``` will navigate inside the ```[name]``` folder/directory (replace ```[name]``` as appropriate).
```ls``` will list all of the files/folders within your current directory.

!["A terminal window is shown with cd lab10 run to navigate into the lab10 directory and then ls run to list all of the files and folders in the lab10 folder."](setup_instruction_pics/usingcdls.png "Example use of ls and cd to navigate to lab10 folder")

You can use tab to autocomplete folder/file names. Once inside the ```lab10``` folder, run the command

```pip install .```

!["A terminal window is shown with py -m pip install . run to install WF_SDK. There are various notices and messages, but no errors, indicating the package was installed successfully."](setup_instruction_pics/pipinstallwfsdknogit.png "Running pip install . to install WF_SDK")

If it runs without erroring, run ```python3``` in your terminal (or PowerShell, if on Windows) to open an interactive Python session. Run

```import WF_SDK```

If it runs without producing any output/erroring, it has installed successfully; run ```quit()``` to close the session - you are ready to begin the lab. If it errors, or if the ```pip install .``` command errored, see the 'Debugging Tips' section.


### Debugging Tips

