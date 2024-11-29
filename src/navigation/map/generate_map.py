from PIL import Image, ImageDraw
import sys

def generate(path: str):
    width = int((3500+50*2) / 50) #3.5m
    height = int((2000 + 50 * 2) / 50) #2m
    im = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, 0, height-1), fill=0)
    draw.rectangle((width-1, 0, width-1, height-1), fill=0)
    draw.rectangle((0, height-1, width-1, height-1), fill=0)
    draw.rectangle((0, 0, width-1, 0), fill=0)
    im.save(path)

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        generate(args[1])
    else:
        print('Usage: python generate_map.py <path>')
