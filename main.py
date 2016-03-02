import os
import subprocess
import soundcloud


class TerminalColors:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


isPlaying = False

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, '.secret')) as f:
    cid = f.readline().strip()
    cs = f.readline().strip()
    f.close()

un = "username"
pw = "password"

client = soundcloud.Client(
    client_id=cid,
    client_secret=cs
)

page_size = 20
tracks = None


def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


while not isPlaying:
    command = raw_input(TerminalColors.BOLD + "\n> " + TerminalColors.ENDC)
    if command:
        if tracks and represents_int(command):
            try:
                track = tracks[int(command) - 1]
                track_url = track.permalink_url
                track_pic = track.artwork_url
                track_title = track.title
                cmd = which('mpv')
                cmd += ' ' + track_url
                p = subprocess.Popen([cmd, track_url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                print TerminalColors.BOLD + '"' + track_title + '"' + TerminalColors.ENDC + ' playing...'
                stdout, stderr = p.communicate()

            except IndexError:
                print 'Please enter a valid number'

        elif command[0] == '/' and len(command) > 1:
            tracks = client.get('/tracks', q=command[1:], limit=page_size)
            for i in range(0, len(tracks) - 1):
                formattedOrderNum = str(i + 1)
                if len(formattedOrderNum) == 1:
                    formattedOrderNum = '0' + formattedOrderNum
                print TerminalColors.OKBLUE + formattedOrderNum + TerminalColors.ENDC + TerminalColors.OKGREEN + ' ' + tracks[
                    i].title + TerminalColors.ENDC

        elif command == 'quit' or command == 'exit':
            break
        else:
            print 'Command not accepted'
