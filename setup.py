import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="caster-core",
    author="To be determined",
    author_email="to@be.determined",
    description="CasterVoice core library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CasterVoice/caster-core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYAML",
        "dragonfly2[kaldi]",
    ],
)
