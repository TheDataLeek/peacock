#!/usr/bin/env python

import sys
import os
from PIL import Image
import argparse

def main():
    args = get_args()
    gen_thumbs(args.directory, args.thumbnails, args.size, args.force)
    md_gallery = gen_markdown(args.directory, args.thumbnails, args.width, args.Title)
    g_file = open(args.gallery, 'w')
    g_file.write(md_gallery)
    g_file.close()

def gen_thumbs(imgdir, thumbdir, size, force):
    '''
    Generate thumbnails from images
    '''
    images = [(imgdir, x) for x in os.listdir(imgdir)]
    try:
        os.mkdir(thumbdir)
    except:
        if force:
            for image in images:
                source     = os.path.join(image[0], image[1])
                name       = image[1].split('.')
                thumb_name = name[0] + '_thumb.' + name[1]
                path       = os.path.join(thumbdir, thumb_name)
                try:
                    source_img = Image.open(source)
                    source_img.thumbnail(size)
                    source_img.save(path)
                    print('%s Done...' % source)
                except:
                    print('%s Error, Skipping...' % source)
        else:
            print('Thumbnails exist. Skipping Step')


def gen_markdown(imgdir, thumbdir, width, title):
    '''
    Generate markdown gallery from directories
    '''
    images = [(imgdir, x) for x in os.listdir(imgdir)]
    images.sort()
    gallery = ""
    if title:
        gallery += 'Title: %s\n\n' % title
    count = 1
    for image in images:
        gallery += gen_link(image, thumbdir) + ' '
        if count % width == 0:
            gallery += "\n\n\n\n"
            count = 0
        count += 1
    return gallery

def gen_link(image, thumbdir):
    '''
    Create Markdown Link
    '''
    source     = os.path.join(image[0], image[1])
    name       = image[1].split('.')
    thumb_name = name[0] + '_thumb.' + name[1]
    path       = os.path.join(thumbdir, thumb_name)
    link       = "[![alt text](%s)](%s)" % (path, source)
    return link

def get_args():
    parser = argparse.ArgumentParser(
            description='Create thumbnails from directory')
    parser.add_argument('-d', '--directory', type=str,
                        default=None, help='Directory containing images')
    parser.add_argument('-t', '--thumbnails', type=str,
                        default='./thumbnails',
                        help='Directory to store thumbnails')
    parser.add_argument('-s', '--size', type=tuple,
                        default=(128, 128),
                        help='Size to store thumbnails in')
    parser.add_argument('-g', '--gallery', type=str,
                        default='gallery.md', help='Gallery File')
    parser.add_argument('-w', '--width', type=int,
                        default=4, help='Width of Gallery Images')
    parser.add_argument('-f', '--force', action='store_true',
                        default=False, help='Force Program Execution')
    parser.add_argument('-T', '--Title', type=str,
                        default='Wallpapers',
                        help='Name for Gallery. None if no name is desired')
    args = parser.parse_args()
    if args.directory is None:
        print("ERROR - Please Specify Source Directory")
        sys.exit(0)
    if args.Title.lower() == 'none':
        args.Title = False
    return args

if __name__ == "__main__":
    sys.exit(main())
