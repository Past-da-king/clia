from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='clia-swe-ai',
    version='0.1.0',
    packages=['gui', 'swe_tools'],
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'clia = gui.main:run_clia',
        ],
    },
    python_requires='>=3.8',
    description='A CLI AI assistant for software engineering tasks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/clia-swe-ai',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
