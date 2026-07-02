from setuptools import setup, find_packages
setup(
    name="dormitory-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "django>=4.2,<4.3",
        "mysqlclient>=2.2.0",
        "gunicorn>=21.2.0",
        "whitenoise>=6.6.0",
        "openpyxl>=3.1.0",
    ],
)
