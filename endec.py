#!/usr/bin/env python

# The MIT License (MIT)
# 
# Copyright (c) 2015 Marcin Woloszyn (@hvqzao)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Tested with Python 2.7.10 and 3.4.3

usage = '''
endec v1.03, Release: Sun Aug  9 12:46:39 CEST 2015

Tiny utility to encrypt and decrypt text data using aes-256-cbc algorithm.

Example usage: cat infile | ./endec (e|d) >outfile
'''

import os,sys,select,getpass,subprocess
if sys.version_info > (3,):
    buffer = memoryview
s=''
def wrap(t,n=64):
    return '\n'.join(list(map(lambda x: t[x:x+n], range(0, len(t), n))))
while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    l = sys.stdin.readline()
    if l:
        s += l
    else:
        break
if len(s) > 0 and len(sys.argv) == 2 and sys.argv[1] in ['e','d']:
    if sys.argv[1] == 'e':
        while True:
            password = getpass.getpass()
            confirm = getpass.getpass('Confirm password:')
            if password != confirm:
                sys.stderr.write('Passwords didn''t match!\n')
            else:
                break
        p = subprocess.Popen('/bin/gzip | /usr/bin/openssl enc -pass pass:"'+password+'" -a -aes-256-cbc', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if sys.version_info[0] >= 3:
            s = bytes(s,'utf-8')
        result = p.communicate(input=buffer(s))[0].decode().replace('\n','')
        sys.stdout.write(wrap(result,120)+'\n')
    else:
        password = getpass.getpass()
        p = subprocess.Popen('/usr/bin/openssl enc -pass pass:"'+password+'" -d -a -aes-256-cbc | /bin/gunzip', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        x = p.communicate(input=buffer(wrap(s).encode('utf-8')))
        result = x[0].decode('utf-8')
        sys.stdout.write(result)
else:
    sys.stderr.write(usage.lstrip().replace('./endec','./'+os.path.basename(sys.argv[0])))
    sys.exit(1)
