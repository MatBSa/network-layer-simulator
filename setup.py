'''
This script aims to build my entire project as a package.
'''

from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
        This function returns the list of packages in requirements.txt.

        Parameters
        ----------
        @param file_path: The path of requirements.txt file [type: string].
        
        Return
        ------
        @return requirements: List of strings containing the packages required for the project.
    '''
    requirements = list()
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    return requirements


# Defining the setup.
setup(
    name = 'Simulador de Camada Física e Camada de Enlace',
    version = '0.0.1',
    author = 'Pedro, Matheus e Davi',
    author_email = '211038271@aluno.unb.br, 170053016@aluno.unb.br, 190127767@aluno.unb.br',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)