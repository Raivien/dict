#!/bin/python
#coding=utf-8

import re
from urllib import quote, unquote
from getpass import getuser

yd_dir = '/home/{}/.yd'.format(getuser())
cache_file = yd_dir + '/.cache'
info_file = yd_dir + '/.info'

def init():
    import os, commands
    if not os.path.exists(yd_dir):
        os.makedirs(yd_dir)
    status, output = commands.getstatusoutput('rm -f {0} && touch {0}'.format(cache_file))
    if status != 0:
        print output
        exit(-1)

    commands.getoutput('echo "disk&" > {}'.format(info_file))

def search(args):
    word = args[0]
    with open(cache_file) as fp:
        for line in fp:
            if word == line.split(' ')[0]:
                result = line.split(' ')
                soundmark = map(unquote, result[1].split('&'))
                definition = map(unquote, result[2].split('&'))
                examples = map(unquote, result[3].split('&'))
                return word, soundmark, definition, examples

def save(dic):
    #   [word, soundmark, definition, examples]
    word = quote(dic[0])
    soundmark = '&'.join(map(quote, dic[1]))
    definition = '&'.join(map(quote, dic[2]))
    examples = '&'.join(map(quote, dic[3]))
    with open(cache_file, 'a+') as fp:
        if not re.search('^{} '.format(word), fp.read(), re.M):
            fp.write("{} {} {} {}\n".format(word, soundmark, definition, examples))