# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Author: shaoze.luo
# @DateTime: 2017-05-27 12:34:25

import shlex
import subprocess
import yaml
import os.path as op
import os
import re



def list_view_in_code():
    """

    """
    cmd = 'find /home/shaoze.luo2/sighub/code -type f -regex ".*\(\.sigs\|\.yaml\)$"'
    # sigs_cmd = 'find /home/shaoze.luo2/sighub/code -type f -regex ".*\(\.sigs\)$"'

    args = shlex.split(cmd)
    filelist = subprocess.check_output(args).strip().split('\n')
    filelist = set(filelist)

    mainlist = []

    for file in filelist:
        suffix = op.basename(file).split('.')[-1]
        if suffix == 'yaml':
            with open(file) as f:
                content = yaml.load(f.read())
            try:
                lib = content['library']
                views = []
                if 'views' in content:
                    for i in xrange(len(content['views'])):
                        name = content['views'][i]['name']
                        try:
                            vtype = content['views'][i][
                                'outputDefinition']['type']
                        except Exception as e:
                            vtype = ""
                        try:
                            mode = content['views'][i][
                                'persist']['historical']['mode']
                        except Exception as e:
                            mode = ""
                        views.append((name, vtype, mode, "yaml"))
                # elif 'automate' in content:
                #     for i in xrange(len(content['automate'])):
                #         for j in xrange(len(content['automate'][i]['include'])):
                #             name = content['automate'][i]['include'][j]['view']
                #             views.append((name,""))
            except Exception as e:
                print file
                continue
        elif suffix == 'sigs':
            with open(file) as f:
                content = f.read()
            views = []
            libse = re.search('library:(.*);', content)
            modese = re.search('persist:[ ]*mode\((.*)\);', content)

            if libse is not None:
                lib = libse.group(1).strip()
            else:
                lib = ""

            if modese is not None:
                mode = modese.group(1).strip()
            else:
                mode = ""
            name = '.'.join([op.basename(file).split('.')[0]] * 2)
            views.append((name, "", mode, "sigs"))

        fileinfo = dict(basename=op.basename(file),
                        dirname=op.dirname(file),
                        abspath=op.abspath(file),
                        library=lib,
                        views=views
                        )

        mainlist.append(fileinfo)

    viewlist = []
    viewtype = []

    for lis in mainlist:
        isWorkFlow = (lis['library'].split('.')[0] == 'workflow')
        for view, vtype, mode, ftype in lis['views']:
            if isWorkFlow:
                # realview = view
                continue
            else:
                realview = lis['library'] + '.' + view
            viewlist.append(realview)
            viewtype.append((realview, vtype, mode, ftype))
    viewlist = set(viewlist)

    with open('out.put', 'w+') as f:
        for view, vtype, mode, ftype in viewtype:
            f.writelines("%s,%s,%s,%s\n" % (view, vtype, mode, ftype))

    return viewlist


def print_view_in_pd(viewlist):
    pdpath = '/mnt/hdfs/projects/CVSC0014/output/prod/views'
    tmplist = set(os.listdir(pdpath))
    # if 'tmplist' not in dir():
    #     tmplist = {}
    totlist = viewlist.union(tmplist)
    count = 0
    with open('checklist.dat', 'w+') as f:
        for view in totlist:
            if op.exists(op.join(pdpath, view)):
                f.writelines('%s|True\n' % view)
            else:
                print '[%s] not exists' % view
                count += 1
                f.writelines('%s|False\n' % view)
    print '%d out of %d not exists' % (count, len(totlist))
