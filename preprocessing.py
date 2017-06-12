"""
This script takes in a archive folder produced by github-backup
and creates a folder with a issue content per files,
where the text was preprocessed to strip markdown and


"""
import os.path
import pandas as pd
from glob import glob
import re

import numpy as np


DATA_DIR = '../scikit-learn_scikit-learn/issue/'

OUT_DIR = './data/'

fname = os.path.join(DATA_DIR, '1000')


def parse_issue(file_path):
    """ Parse files saved by github-backup 
    saved in Haskel serialized format
    (couldn't find an appropriate Python parser
    """

    md = {}
    with open(file_path, 'rt') as fh:
        txt = fh.read()

    md['type'] = txt.splitlines()[0]
    if md['type'] == 'Issue':

        m = re.search(',\s+issueTitle\s*=\s*"(?P<title>.*)"\s+,', txt)
        md['title'] = m.group('title')
        m = re.search(',\s+issueHtmlUrl\s*=\s*Just\s*\(\s*URL\s*"(?P<url>.*)"\)\s+,', txt)
        md['url'] = m.group('url')
        m = re.search(',\s+issueBody\s*=\s*Just\s*"(?P<body>.*)"\s+,', txt)
        if m:
            md['body'] = m.group('body')
        else:
            m = re.search(',\s+issueBody\s*=\s*Nothing\s+,', txt)
            if m:
                md['body'] = ''
            else:
                raise ValueError("issueBody not found in \n" + txt)
    elif md['type'] == 'IssueComment':
        m = re.search(',\s+issueCommentBody\s*=\s*"(?P<body>.*)"\s+,', txt)
        if m:
            md['body'] = m.group('body')
        else:
            m = re.search(',\s+issueCommentBody\s*=\s*Nothing\s+,', txt)
            if m:
                md['body'] = ''
            else:
                raise ValueError("issueCommentBody not found in \n" + txt)

    else:
        raise ValueError

    return md


parse_issue(fname)

file_name = [os.path.split(fname)[1] for fname in
             glob(os.path.join(DATA_DIR, '*'))]
file_name = [int(el) for el in file_name if '_comment' not in el]
issue_ids = np.array(sorted(file_name))

md_res = []

idx = 0

for doc_id in issue_ids:
    md = parse_issue(DATA_DIR + '{}'.format(doc_id))
    md['document_id'] = doc_id
    body = [md.pop('body')]
    md_res.append(md)

    # conctanate comments for the the main issue
    for file_path in glob(DATA_DIR + '{}_comment/*'.format(doc_id)):
        md_tmp = parse_issue(file_path)
        body += [md_tmp.pop('body')]
    body = '\n'.join(body)
    # remove urls
    body = re.sub('^https?:\S+', 'URL_LINK_TOKEN', body)
    # save files for processing
    with open(os.path.join(OUT_DIR, '{:05}'.format(doc_id)), 'wt') as fh:
        fh.write(body)

md_res = pd.DataFrame(md_res)
md_res.to_pickle('./db.pkl')
print(md_res)
