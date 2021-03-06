# -*- coding: utf-8 -*-
import ast
import os
import sys
import argparse
import subprocess


SET = 'hyperdimension-neptunia_01'
SCRIPT_EXT = '.py'
DATASET_EXT = '.dataset'

CURRENT_DIR = os.path.dirname( os.path.abspath(__file__) )
PROJECT_DIR = os.path.join(CURRENT_DIR)
SCRIPTS_DIR = os.path.join(PROJECT_DIR, 'learning')
DATA_DIR    = os.path.join(PROJECT_DIR, 'data/raw')
SETS_DIR    = os.path.join(PROJECT_DIR, 'data/set')


#from zulmeygut.subspack import event


def load_files(path, extension) :
    files = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file() :
                name, ext = os.path.splitext(entry.name)
                if ext == extension :
                    files.append(name)
    return files


def main(argv) :
    '''
    '''
    scripts  = load_files(SCRIPTS_DIR, SCRIPT_EXT)
    datasets = load_files(SETS_DIR, DATASET_EXT)
    
    main_parser = argparse.ArgumentParser(
            description='Launchs learning scripts with specified arguments',
            epilog='Nep-Nep')
    subparsers = main_parser.add_subparsers()
    dataset_parser = subparsers.add_parser('dataset', description='Case to process')
    dataset_parser.add_argument('dataset', choices=datasets)
    dataset_parser.add_argument('--case', type=str)
    main_parser.add_argument('script', choices=scripts + ['all'])
    
    args = main_parser.parse_args(argv)
    
    script = args.script + SCRIPT_EXT
    script = os.path.join(SCRIPTS_DIR, script)
    script = os.path.abspath(script)
    
    dataset = args.dataset + DATASET_EXT
    dataset = os.path.join(SETS_DIR, dataset)
    dataset = ast.literal_eval( open(dataset, 'r').read() )
    
    audio = dataset['audio']
    subtitles = dataset['subtitles']
    try:
        case = dataset['cases'][args.case]
    except KeyError:
        print('Argument "case" must be one of the folowing: {}'.format(dataset['cases'].keys()))
        sys.exit(1)

    audio     = os.path.join(DATA_DIR, str(args.dataset), audio    )
    subtitles = os.path.join(DATA_DIR, str(args.dataset), subtitles)
    audio, subtitles = os.path.abspath(audio), os.path.abspath(subtitles)
    
    print( 'Executing script "{}" with:'.format(script) )
    print( 'start {}'.format(case['start']) )
    print( 'end   {}'.format(case['end'  ]) )
    print( 'audio     "{}"'.format(audio    ) )
    print( 'subtitles "{}"'.format(subtitles) )
    
    task = [sys.executable,
            script,
            '--start={}'.format(case['start']),
            '--end={}'.format(case['end']),
            '{}'.format(audio),
            '{}'.format(subtitles)]
    
    process = subprocess.run(task, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
    
    print( 'Return code: {}'.format(process.returncode) )
    try :
        process.check_returncode()
    except subprocess.CalledProcessError :
        print( 'Error:  {}'.format(process.stdout) )
    else :
        print( 'Output: {}'.format(process.stdout) )

if __name__ == '__main__' :
    main(sys.argv[1:])












