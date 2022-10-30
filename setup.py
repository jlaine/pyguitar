import os.path

import setuptools

root_dir = os.path.abspath(os.path.dirname(__file__))

about = {}
about_file = os.path.join(root_dir, "src", "pyguitar", "about.py")
with open(about_file, encoding="utf-8") as fp:
    exec(fp.read(), about)

readme_file = os.path.join(root_dir, "README.rst")
with open(readme_file, encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    url=about["__uri__"],
    author=about["__author__"],
    author_email=about["__email__"],
    license=about["__license__"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=["pyguitar"],
    install_requires=["colorama", "mido", "scipy"],
    extras_require={
        "dev": [
            "black",
            "coverage",
            "flake8",
            "isort",
        ]
    },
)
