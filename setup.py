import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setuptools.setup(
        name="lemonrunner",
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        author="sveinrou",
        author_email="sveinrou@gmail.com",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/sveinrou/lemonrunner",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
    )
