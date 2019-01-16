from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="django_volunteer_apply",
    version="0.1",
    author="zhaofeng-shu33",
    description="search student information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhaofeng-shu33/apply",
    author_email="616545598@qq.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
