from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='django-remote-form-helpers',
    version='0.1.0',
    description='A library to enhance frontend performance and streamline dynamic data handling in Django applications',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='django, forms, ajax, remote data, dynamic forms, form helpers, django widgets, django integration, frontend performance, django library',
    author='Deivid Hugo',
    author_email='deividhugoof@gmail.com',
    url='https://github.com/DeividHugo/django-remote-form-helpers',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Django>=1.9',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
