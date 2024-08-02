from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='django-remote-form-helpers',
    version='0.1.0',
    description='A library to enhance frontend performance and streamline dynamic data handling in Django applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Deivid Hugo',
    author_email='deividhugoof@gmail.com',
    url='https://github.com/PythonCreatedLibs/django_remote_form_helpers',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Django>=1.9,<=5.0.7',
    ],
)
