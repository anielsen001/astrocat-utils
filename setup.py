import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="astrocat-utils",
    version="0.0.1",
    author="Aaron Nielsen",
    author_email="apn@apnielsen.com",
    description="Astrometry catalog utilities",
    url="https://github.com/anielsen001/astrocat-utils",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
