# Build BaiduSpider
echo "Formatting source files..."
source ./lint.sh
echo "Source files formatted."
echo "Building packages..."
rm -rf ./dist
rm -rf ./build
python setup.py sdist build
echo "Build complete."
echo "Publishing to PyPI..."
PASS=`grep -oP "(?<=PyPi Token: ).*" /d/Personal/Passwords.txt`
twine upload -u __token__ -p $PASS dist/*
echo "Package published to PyPI successfully."