# Build BaiduSpider
rm -rf ./dist
rm -rf ./build
python setup.py sdist build
echo "Build complete. Run twine upload dist/* to upload your package to PyPI."