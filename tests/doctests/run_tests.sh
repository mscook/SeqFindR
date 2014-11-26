pip install coverage
coverage run run_tests.py
coverage report --omit "*/Bio/*"
