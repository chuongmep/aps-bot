import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)  # Run the standard install process first
        user_response = input("Would you like to add the necessary directory to your PATH? [y/N]: ")
        if user_response.lower() == 'y':
            self.add_to_path()
        else:
            print("Skipping PATH modification.")

    def add_to_path(self):
        # This is the directory where your command-line executable would be installed
        path_to_add = os.path.join(sys.prefix, 'bin')  # Adjust this path as necessary

        if sys.platform == 'win32':
            self.add_path_windows(path_to_add)
        elif sys.platform in ['linux', 'darwin']:  # darwin is for macOS
            self.add_path_unix(path_to_add)

    def add_path_windows(self, path_to_add):
        print(f"Adding {path_to_add} to PATH on Windows")
        try:
            import winreg
            with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as reg:
                with winreg.OpenKey(reg, 'Environment', 0, winreg.KEY_ALL_ACCESS) as key:
                    current_path, reg_type = winreg.QueryValueEx(key, 'Path')
                    if path_to_add not in current_path:
                        new_path = f"{current_path};{path_to_add}"
                        winreg.SetValueEx(key, 'Path', 0, reg_type, new_path)
            print("PATH updated successfully in the Windows registry.")
        except Exception as e:
            print(f"Failed to update PATH on Windows: {e}")

    def add_path_unix(self, path_to_add):
        print(f"Adding {path_to_add} to PATH on Unix/Linux")
        profile_path = os.path.expanduser('~/.bash_profile') if sys.platform == 'darwin' else os.path.expanduser('~/.bashrc')
        path_line = f'export PATH="$PATH:{path_to_add}"\n'

        if not self.is_path_in_file(profile_path, path_to_add):
            try:
                with open(profile_path, 'a') as file:
                    file.write(path_line)
                print(f"PATH updated successfully in {profile_path}")
            except Exception as e:
                print(f"Failed to update PATH on Unix/Linux: {e}")

    def is_path_in_file(self, file_path, path_to_add):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if path_to_add in line:
                        return True
        except FileNotFoundError:
            pass
        return False

setup(
    name="apsbot",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "aps-toolkit",
        "pyperclip",
        "tabulate"
    ],
    entry_points={
        "console_scripts": [
            "apsbot=apsbot.cli:apsbot",
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    author="chuongmep",
    author_email="chuongpqvn@gmail.com",
    description="A simple CLI tool to interact with the Autodesk Forge API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chuongmep/aps-bot.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
