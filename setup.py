from setuptools import setup, find_packages

setup(
    name="brent-oil-analysis",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "streamlit>=1.24.0",
    ],
)