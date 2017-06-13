# FreeDiscovery demo: review of GitHub issues.

A FreeDiscovery demo of information retrieval on the 9100 Github issues from the `scikit-learn` project (PyParis2017 conference)

To run this demo,

1. [Install FreeDiscovery](https://github.com/FreeDiscovery/FreeDiscovery#installation) (preferably in a [conda] virtualenv), and start the server in a separate terminal.
2. Unzip data: `tar xzf scikit-learn_scikit-learn.tgz` and run the preprocessing scipt (requires numpy and pandas),
   ```
   python preprocessing.py
   ```
   this would create a new folder `data/` with one text file per github issue, and a pickled pandas dataframe `db.pkl` with metadata.

3. Start jupyer notebook and run `freediscovery-github-issues-demo.ipynb`

# Notes 

The raw data in `scikit-learn_scikit-learn.tgz` was obtained by running [github-backup](https://github.com/joeyh/github-backup) on the scikit-learn public repository,


```
git clone https://github.com/scikit-learn/scikit-learn.git
cd scikit-learn
github-backup --no-forks 
git checkout github
tar czf scikit-learn_scikit-learn.tgz scikit-learn_scikit-learn/
```
