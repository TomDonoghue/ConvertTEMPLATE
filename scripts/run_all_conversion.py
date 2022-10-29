"""Run conversion on all sessions."""

import sys
sys.path.append('..')
from conv import Paths
from conv.io import get_files, make_session_name
from convt3.utils import print_status

# Import processing functions (from local scripts)
from prepare_data import prepare_data
from convert_data import convert_data

# Import settings
from settings import PROJECT_PATH, EXPERIMENT, SETTINGS, SKIP

###################################################################################################
###################################################################################################

def run_all_conversions():
    """Run NWB conversion on all available TH sessions."""

    msg = '\n\nRUNNING ALL CONVERSIONS FOR - {}\n\n'.format(EXPERIMENT)
    print_status(SETTINGS['VERBOSE'], msg, 0)

    # Initialize paths
    paths = Paths(PROJECT_PATH)

    # Get a list of all available sessions
    all_sessions = {}
    subjects = get_files(paths.recordings)
    for subject in subjects:
        all_sessions[subject] = get_files(paths.recordings / subject / EXPERIMENT, select='session')

    # Get a list of already converted sessions
    converted = get_files(paths.nwb, select='nwb')

    for subject, sessions in all_sessions.items():

        if subject in SKIP['SUBJECTS']:
            print_status(SETTINGS['VERBOSE'], 'SKIPPING SUBJECT: \t{}'.format(subject), 0)
            continue

        for session in sessions:

            # Collect together the subject information & define session ID
            SESSION = {'SUBJECT' : subject, 'EXPERIMENT' : EXPERIMENT, 'SESSION' : session}
            session_name = make_session_name(SESSION['SUBJECT'],
                                             SESSION['EXPERIMENT'],
                                             SESSION['SESSION'])

            # Check for skipping subject
            if session_name in SKIP['SESSIONS']:
                print_status(SETTINGS['VERBOSE'], 'SKIPPING SESSION: \t{}'.format(session_name), 0)
                continue

            # Check for whether to skip already run
            if SETTINGS['SKIP_ALREADY_RUN'] and session_name + '.nwb' in converted:
                print_status(SETTINGS['VERBOSE'], 'SESSION ALREADY RUN: \t{}'.format(session_name), 0)
                continue

            # Prepare data
            prepare_data(SESSION=SESSION, SETTINGS=SETTINGS)

            # Run data conversion
            convert_data(SESSION=SESSION, SETTINGS=SETTINGS)

    msg = '\n\n FINISHED CONVERSIONS FOR - {}\n\n'.format(EXPERIMENT)
    print_status(SETTINGS['VERBOSE'], msg, 0)


if __name__ == '__main__':
    run_all_conversions()
