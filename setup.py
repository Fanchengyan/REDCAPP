import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="REDCAPP",
    version="0.1.0",
    author="caobin, fanchegyan",
    author_email="caobin198912@outlook.com, fanchy14@lzu.edu.cn",
    description="downscaling reanalysis data in mountainous areas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fanchengyan/REDCAPP",
    packages=setuptools.find_packages(),
    install_requires=[
        'pygrib',
        'netCDF4',
        'setuptools',
        'numpy',
        'scipy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
