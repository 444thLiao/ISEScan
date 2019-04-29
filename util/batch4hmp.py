#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
from os.path import dirname
import isPredict
import tools

python3 = 'python3'
cmd = os.path.abspath(os.path.join(dirname(dirname(__file__)), 'isescan.py'))


def batch(args):
    dnaListFile4orgs = args['fileList']
    dir4prediction = args['dir2prediction']
    print('Batch running begins at', datetime.datetime.now().ctime())

    dnaFiles = tools.rdDNAlist(dnaListFile4orgs)
    # dnaFiles: [(file, org), ..., (file, org)]
    # file4orgs: {org: files, ..., org: files}
    # files: [file4fileid, ..., file4fileid]
    file4orgs = {}
    for fileOrg in dnaFiles:
        file, org = fileOrg
        if org not in file4orgs.keys():
            file4orgs[org] = []
        file4orgs[org].append(file)

    print('number of organisms to process:', len(file4orgs))

    dir2proteome = os.path.join(dir4prediction, 'proteome')
    dir2hmmsearchResults = os.path.join(dir4prediction, 'hmm')
    isPredict.isPredict(dnaListFile4orgs, dir2proteome, dir2hmmsearchResults, dir4prediction)
    # summarize IS elements in each genome DNA and each organism

    # get summarization of IS elements for each organism and write summarization
    # write 'organism.sum' in each organism directory
    tools.sum4org4hmp(file4orgs, dir4prediction=dir4prediction)
    # prepare and write 'is.sum' in current directory
    sum4is = {}
    for org in file4orgs.keys():
        sumFileByOrg = os.path.join(dir4prediction, '%s.sum' % org)
        if os.path.isfile(sumFileByOrg) and os.stat(sumFileByOrg).st_size > 0:
            sum4is[org] = tools.getSumFull(sumFileByOrg, org)

    print('Batch running finishes at', datetime.datetime.now().ctime())


if __name__ == "__main__":
    descriptionStr = 'Summarize prediction results of IS elements in each organism and all organisms'
    parser = argparse.ArgumentParser(description=descriptionStr)
    helpStr = 'input file containing NCBI genome fasta files, one file per line'
    parser.add_argument('fileList', help=helpStr)
    helpStr = 'directory holding the results of IS prediction, one organism per sub-directory'
    parser.add_argument('dir2prediction', help=helpStr)
    args = parser.parse_args()
    args4batch = {
        'fileList': args.fileList,
        'dir2prediction': args.dir2prediction,
    }
    batch(args4batch)
