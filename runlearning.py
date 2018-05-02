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
    main_parser.add_argument('script', choices=scripts + ['all'])
    subparsers = main_parser.add_subparsers()
    
    #formatter = event.TimeFormat('SSA')
    dataset_parser = subparsers.add_parser('dataset', description='Case to process')
    dataset_parser.add_argument('dataset', choices=datasets)
    dataset_parser.add_argument('--case', type=str)
    #dataset_parser.add_argument('--start', type=formatter.from_str)
    #dataset_parser.add_argument('--end'  , type=formatter.from_str)
    
    args = main_parser.parse_args(argv)
    #print( args )
    
    script = args.script + SCRIPT_EXT
    script = os.path.join(SCRIPTS_DIR, script)
    script = os.path.abspath(script)
    
    dataset = args.dataset + DATASET_EXT
    dataset = os.path.join(SETS_DIR, dataset)
    dataset = ast.literal_eval( open(dataset, 'r').read() )
    
    audio = dataset['audio']
    subtitles = dataset['subtitles']
    case = dataset['cases'][args.case]
    
    
    audio, subtitles = os.path.join(DATA_DIR, audio), os.path.join(DATA_DIR, subtitles)
    audio, subtitles = os.path.abspath(audio), os.path.abspath(subtitles)
    
    task = [sys.executable,
            script,
            '--start={}'.format(case['start']),
            '--end={}'.format(case['end']),
            audio,
            subtitles]
    
    process = subprocess.run(task, stdout=subprocess.PIPE, shell=False)
    print( process.stdout )

if __name__ == '__main__' :
    main(sys.argv[1:])












