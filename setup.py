from setuptools import setup

setup(
    name="Pandemic",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["run-server = server.__main__"],
        "gui_scripts": ["run-client = client.__main__"],
    },
    install_requires=[
        "pygame",
        "jsonpickle"
    ]
)
