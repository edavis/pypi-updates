from setuptools import setup

install_requires = [
    "python-postmark==0.3.2",
    "pkgtools==0.7.1",
    "Jinja2==2.6",
]

setup(
    name = "pypi-updates",
    version = "0.1",
    description = "Email updates of new PyPI releases",
    author = "Eric Davis",
    author_email = "ed@npri.org",
    url = "https://github.com/edavis/pypi-updates",
    packages = ["pypi_updates"],
    license = "MIT",
    install_requires = install_requires,
    include_package_data = True,
    entry_points = {
        "console_scripts": [
            "email-updates = pypi_updates:main",
        ],
    },
)
