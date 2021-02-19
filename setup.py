import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='BaiduSpider',
    version='0.1.2',
    author='Sam Zhang',
    author_email='samzhang951@outlook.com',
    description='BaiduSpider，一个爬取百度的利器',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BaiduSpider/BaiduSpider',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: Free for non-commercial use'
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'bs4',
        'htmlmin'
    ]
)
