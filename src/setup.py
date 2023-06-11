import sys
from cx_Freeze import setup, Executable

file_include = ["config.json", "Run Debug Mode.bat", "app.vrmanifest"]

build_exe_options = {"include_files": file_include}

setup(
    name="RandomNumber_OSC",
    version="0.1.0",
    description="RandomNumber_OSC",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", target_name="RandomNumber_OSC.exe", base=False), Executable("main.py", target_name="RandomNumber_OSC_NoConsole.exe", base="Win32GUI")],
)