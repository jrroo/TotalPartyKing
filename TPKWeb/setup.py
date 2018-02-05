from setuptools import setup

setup(
    name='TPKWeb',
    version='0.0.1',
    description='Total Pary King Web API',
    url='http://github.com/jrroo/TotalPartyKing',
    author='Zach Lorusso',
    author_email='zlorusso@gmail.com',
    license='MIT',
    packages=['tpk_web'],
    install_requires=[
        "Flask~=0.12",
        "Flask-RESTful~=0.3",
        "Flask-SQLAlchemy~=2.3",
    ],
    zip_safe=False,
)
