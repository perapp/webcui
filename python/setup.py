import setuptools
import pathlib

home = pathlib.Path(__file__).parent.parent
readme = (home/"README.md").read_text()

setuptools.setup(
    name="webcui",
    version="0.1.1",
    author="Per Appelgren",
    author_email="per@appgren.se",
    description="A web command user interface",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/perapp/webcui",
    packages=["webcui"],
    package_dir={"": "python"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
