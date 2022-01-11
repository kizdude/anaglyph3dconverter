import os, sys
from PIL import Image


def grey_to_red(input_image):
    output_image = input_image.convert("CMYK")
    input_image = input_image.convert("L")

    for x in range(output_image.width):
        for y in range(output_image.height):
            # for the given pixel at w,h, lets check its value against the threshold
            l = input_image.getpixel((x, y))
            output_image.putpixel((x, y), (0, 255 - l, 255 - l, 0))
    # return new image
    output_image = output_image.convert("RGBA")
    for x in range(output_image.width):
        for y in range(output_image.height):
            # for the given pixel at w,h, lets check its value against the threshold
            r, g, b, a = output_image.getpixel((x, y))
            l = round(r * 299 / 1000 + g * 587 / 1000 + b * 114 / 1000)
            output_image.putpixel((x, y), (r, g, b, round((255 - l)*0.4)))
    return output_image


def grey_to_cyan(input_image):
    output_image = input_image.convert("CMYK")
    input_image = input_image.convert("L")

    for x in range(output_image.width):
        for y in range(output_image.height):
            # for the given pixel at w,h, lets check its value against the threshold
            l = input_image.getpixel((x, y))
            output_image.putpixel((x, y), (255 - l, 0, 0, 0))
    # return new image
    output_image = output_image.convert("RGBA")
    for x in range(output_image.width):
        for y in range(output_image.height):
            # for the given pixel at w,h, lets check its value against the threshold
            r, g, b, a = output_image.getpixel((x, y))
            l = round(r * 299 / 1000 + g * 587 / 1000 + b * 114 / 1000)
            output_image.putpixel((x, y), (r, g, b, round((255 - l)*0.8) ))
    return output_image


for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + "-thumbnail.jpg"
    if infile != outfile:
        try:
            with Image.open(infile) as im:
                w = im.width
                h = im.height
                distort = round(w/30)

                redim = grey_to_red(im)

                cyanim = grey_to_cyan(im)

                greyim = im.convert("L")


                left = (distort, 0, w, h)
                right = (0, 0, w-distort, h)

                pasteim = greyim.convert("RGBA")

                region = cyanim.crop(left)
                pasteim.alpha_composite(region, (0,0))

                region = redim.crop(right)
                pasteim.alpha_composite(region, (distort,0))

                outfile = os.path.splitext(infile)[0] + "-anaglyph.png"
                pasteim.save(outfile, "PNG")

        except OSError:
            print("cannot create thumbnail for", infile)
