#!/usr/bin/env python
# -*- coding:utf-8 -*-
  
import argparse
import subprocess
from itertools import permutations

def main():
  
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', help='word pattern', required=True)
    parser.add_argument('-i', '--include', help='include words', required=False)
    parser.add_argument('-e', '--exclude', help='exclude words', required=False)
    args = parser.parse_args()
    
    word_regex = "^("
    word_template = args.pattern
    seed = '' if None == args.include else args.include
    seed = seed + "-"*(word_template.count("_") - len(seed))
    exclude_pattern = '[^\']' if None == args.exclude else "[^\'" + args.exclude + "]"
    for p in set(permutations(seed)) :
        idx = 0
        for c in word_template :
            if '_' == c :
                word_regex += exclude_pattern if '-' == p[idx] else p[idx]
                idx += 1
            else :
                word_regex += c
            
        word_regex += "|"
    
    word_regex += ")$"

    command = "grep -E \"" + word_regex.replace("|)", ")") + "\" /usr/share/dict/words"

    proc = subprocess.Popen(
    command,
    shell  = True,                            # sh -c "command"
    stdin  = subprocess.PIPE,                 #1
    stdout = subprocess.PIPE,                 #2
    stderr = subprocess.PIPE)                 #3

    stdout_data, stderr_data = proc.communicate() #wait

    if (isinstance(stdout_data, bytes)):
        print (stdout_data.decode("UTF-8"))
    else:
        print (stdout_data)

if __name__ == '__main__':
    main()