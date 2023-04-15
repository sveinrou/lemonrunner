import setuptools

version = "0.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []

if __name__=='__main__':
    setuptools.setup(
        name="definitely",
        version=version,
        author="sveinrou",
        author_email="sveinrou@gmail.com",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        install_requires=requirements,
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
    )
