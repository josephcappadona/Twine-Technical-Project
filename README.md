## Instructions

`python twine.py people.csv config.csv outfile.csv`

For example,

```
python twine.py test_data/example1_people.csv test_data/example1_config.csv groups1.csv
diff groups1.csv test_data/example1_groups.csv
```

## Potential Improvements

* Generalize fit score calculation to arbitrary number of people so that we can compute the best groups of arbitrary size

* Generalize attribute fit score calculation to allow for partial fits (i.e., attribute fit scores need not be only 0 or 1)

* Create test example with many more people to better check edge cases (e.g., the case where multiple pairs of people have identical fit scores so that we can ensure that ties are broken correctly)

## Other Instructions

Find tests in `test_twine.py`. Run via `python test_twine.py`.

Also note that I have corrected the typos in the test data, which can be found in the `test_data/` directory.
