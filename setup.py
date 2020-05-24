import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyopenms-extra-Fabian1567", # Replace with your own username
    version="0.0.1",
    author="Fabian Rosner",
    author_email="fabian@rosner.email",
    description="Pyopenms-extra test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lauraschoeneberg/pyopenms-extra",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)