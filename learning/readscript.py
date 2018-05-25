import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, '../')
REPORTS_DIR = os.path.join(PROJECT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')

# The Way of the Voice
sys.path.append(PROJECT_DIR)


from zulmeygut.subspack import model
from zulmeygut.subspack import time
from zulmeygut.subspack import script
from zulmeygut.utility import linereader

from helper import helper


if __name__ == '__main__':
    args = helper.arguments(sys.argv[1:], 'Subspack testing')
    audio, subtitles = args.audio, args.subtitles
    start, end = args.start, args.end

audio, subtitles = str(audio), str(subtitles)
start_cc, end_cc = time.incenties(start), time.incenties(end)


events = script.FormattedSection(model.Section.EVENTS)
lines = linereader.read_all(subtitles)
events.load(lines)
