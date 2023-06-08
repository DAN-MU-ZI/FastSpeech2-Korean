import argparse
import os
import json


def main(args):
    with open(args.inputpath, 'r',encoding='utf-8') as f:
        data = json.load(f)
    for k,v in data.items():
        with open('{}/{}.txt'.format(args.savepath,k.split('.')[0]), 'w', encoding='utf-8') as t:
            t.write(v)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DECA: video to jpg')

    parser.add_argument('-i', '--inputpath', type=str,
                        help='path to the test data, can be image folder, image path, image list, video')
    parser.add_argument('-s', '--savepath', type=str,
                        help='path to the test data, can be image folder, image path, image list, video')                        
    main(parser.parse_args())