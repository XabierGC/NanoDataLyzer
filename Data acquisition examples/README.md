# Data acquisition with NanoDataLyzer

NanoDataLyzer is not able to communicate directy with instruments, but with OS console shell or even with specific versions of python (currently python 3.9, 3.10 and 3.11). Therefore, a python function can be created to acquire data using the library pyvisa and pass the results directy to NanoDataLyzer. Even loops or automatizations of measurements can be easily programmed using NanoDataLyzer's tool Create Dataset Batch.

## Instructions for acquiring data using Python

-Install a compatible version of Python (3.9, 3.10 or 3.11). We recommend to install Anaconda as it automatically sets everything (version of [Anaconda 3_2023.09-0](https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Windows-x86_64.exe) in [https://repo.anaconda.com/archive/](https://repo.anaconda.com/archive/) ).

-Once installed, you should ensure that Python is on the Windows path. If you open a cmd instance in Windows and write "python --version" and after pressing enter, the proper Python version appers, then skip the next step.

-If Python is not retrievable through the system path, then you have to add it and add the folder that contains it. (If you have installed Anaconda, python.exe is located inside Anaconda folder by default in program files folder) [Here how to add to path in windows](https://www.wikihow.com/Change-the-PATH-Environment-Variable-on-Windows).

-Once python can be called from cmd, then it can be called from NanoDataLyzer. Next step will be install in anaconda prompt (or other Python console) the libraries that are going to be used in the Python file, for example pyvisa (check the first comments in the '.py' files of the folder). Finally install all the drivers of the instrument if necessary.

-Then you can call Python files directly from NanoDataLyzer using Matlab code syntax. Using NanoDataLyzer's Tools>Create Dataset Batch utility, you can edit, test and debug code and save it as a template in files with '.ndl' extension (NanoDataLyzer dataset files)
