from setuptools import find_packages,setup
from typing import List

HYPHEN_E = '-e .'

def get_requirements(file_path:str)->List[str]: #gets all requirements from requirements.txt
    requirements =[]
    with open (file_path) as file_obj :
        requirements=file_obj.readlines()
        requirements = [req.replace("\n","")for req in requirements ]
        if HYPHEN_E in requirements :
            requirements.remove(HYPHEN_E) #exclude the -e command from the requirements file
    return requirements

setup(
    name='mlproject',
    author='Glory KO',
    author_email='koladeg37@gmail.com',
    version='0.0.1',
    packages=find_packages(),
    install_requires =get_requirements('requirements.txt'),
)