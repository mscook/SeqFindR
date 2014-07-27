#VERSION=0.31.2

# Lets run the examples first...
pip uninstall SeqFindr
python setup.py install
cd example
sh run_examples.sh
cd ..
rm -rf example/run1
rm -rf example/run2
rm -rf example/run3
rm -rf example/run4
rm -rf example/run5
pip uninstall SeqFindr
python setup.py clean


# Do all the versioning stuff here..
bumpversion patch


# Clean, test, build the source distribution & pip install it
# Need to get exit statuses here...
python setup.py clean
#python setup.py test
#STATUS=`echo $?`
#if [ $STATUS -eq 0 ]; then
#    echo ""
#else
#    echo "Tests failed. Will not release"
#    exit
#fi 

python setup.py sdist bdist_wheel
pip install dist/SeqFindr-$VERSION.tar.gz
STATUS=`echo $?`
if [ $STATUS -eq 0 ]; then
    echo ""
else
    echo "Package is not pip installable. Will not release"
    exit
fi 


# Docs
# Need to get exit statuses here...
cd docs
make clean
sphinx-apidoc -o API ../SeqFindr
mv API/* .
rmdir API
make html
cd ..

git push
# tag & push the tag to github
GIT=`git status`
CLEAN='# On branch master nothing to commit, working directory clean'
if [ "$s1" == "$s2" ]; then
    git tag v$VERSION
    git push --tags
else
    echo "Git not clean. Will not release"
    exit
fi 


# Upload to PyPI
twine upload -u mscook -p $PYPIPASS dist/*


# Clean up 
python setup.py clean
