from setuptools import setup, find_packages
exec(open("src/crypropayment/_resources.py").read())

setup(
    name=__package_name__,
    version=__version__,
    author=__author__,
    author_email='battenetciz@gmail.com',
    description='FastAPI application for crypto payments',
    install_requires=[
        'fastapi==0.78.0',
        'requests==2.27.1',
        'uvicorn==0.17.6',
        'sqlalchemy==1.4.36',
        'python-dotenv',
        'myloguru-deskent==0.0.12',
    ],
    scripts=['src/cryptopayment/example.py'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
)
