import argparse
import subprocess
from glob import glob




def main(args):
    paths = glob('{}/*.mp4'.format(args.inputpath))
    for i in paths:
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(i, '{}/{}.wav'.format(args.savepath, i.split('\\')[-1].split('.')[0]))
        subprocess.call(command, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DECA: video to jpg')

    parser.add_argument('-i', '--inputpath', type=str,
                        help='path to the test data, can be image folder, image path, image list, video')
    parser.add_argument('-s', '--savepath', type=str,
                        help='path to the test data, can be image folder, image path, image list, video')                        
    main(parser.parse_args())