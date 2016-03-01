import subprocess

import soundcloud


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


isPlaying = False

cid = "1118184d5e041ecc64565a674981f85d"
cs = "92368b7a0ee608438a7788ebcc63778e"

un = "==="
pw = "==="

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
    command = raw_input(bcolors.BOLD + "\n> " + bcolors.ENDC)
    if command:
        if tracks and represents_int(command):
            try:
                track = tracks[int(command) - 1]
                track_url = track.permalink_url
                track_pic = track.artwork_url
                track_title = track.title
                cmd = which('mpv')
                cmd += ' ' + track_url
                p = subprocess.Popen(['mpv', track_url], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                print bcolors.BOLD + '"' + track_title + '"' + bcolors.ENDC + ' playing...'
                stdout, stderr = p.communicate()

            except IndexError:
                print 'Please enter a valid number'

        elif command[0] == '/' and len(command) > 1:
            tracks = client.get('/tracks', q=command[1:], limit=page_size)
            for i in range(0, len(tracks) - 1):
                formattedOrderNum = str(i + 1)
                if len(formattedOrderNum) == 1:
                    formattedOrderNum = '0' + formattedOrderNum
                print bcolors.OKBLUE + formattedOrderNum + bcolors.ENDC + bcolors.OKGREEN + ' ' + tracks[i].title + bcolors.ENDC

        elif command == 'quit' or command == 'exit':
            break
        else:
            print 'Command not accepted'
