from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT="-e ."


def get_requirements(filepath: str) -> List[str]:
    """
    This function reads the requirements.txt file and returns a list of Python packages required for the project.

    Args:
    filepath (str): The path to the requirements.txt file.

    Returns:
    List[str]: A list of Python packages required for the project.
    """

    with open(filepath, "r") as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        return requirements


setup(
    name="source-code-analyser",
    version="0.0.1",
    author="Arjuna",
    author_email="sivasandeeppasumarthi@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
