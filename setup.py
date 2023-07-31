import setuptools

VERSION = "0.0.1"  # PEP-440

NAME = "streamlit_airtable"

INSTALL_REQUIRES = [
    "streamlit>=1.22.0",
    "pyairtable>=1.5.0",
]


setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Streamlit Connection for Airtable.",
    url="https://github.com/marks/streamlit-airtable-connection",
    project_urls={
        "Source Code": "https://github.com/marks/streamlit-airtable-connection",
    },
    author="Mark Silverberg",
    author_email="mark.silverberg@airtable.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["streamlit_airtable"],
)
