import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BaiduSpider",
    version="1.0.2.6",
    author="Sam Zhang",
    author_email="samzhang951@outlook.com",
    description="BaiduSpider，一个爬取百度的利器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BaiduSpider/BaiduSpider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "License :: Free for non-commercial use",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=["requests>=2.25.1", "bs4>=0.0.1"],
)
