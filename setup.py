import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='BaiduSpider',
    version='0.0.5',
    author='Sam Zhang',
    author_email='samzhang951@outlook.com',
    description='BaiduSpider，一个爬取百度的利器',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BaiduSpider/BaiduSpider',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha'
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'bs4',
        'htmlmin'
    ]
)
