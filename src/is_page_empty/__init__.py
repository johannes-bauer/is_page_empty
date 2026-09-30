try:
    import skimage
    def load_image(fn):
        return skimage.io.imread(fn)
except ImportError:
    try:
        import imageio.v3 as iio
        def load_image(fn):
            return iio.imread(fn)
    except ImportError:
        import PIL, numpy
        def load_image(fn):
            im = PIL.Image.open(fn)
            return numpy.array(im)
    
import sys

CUTOFF = 0.02

def score(im):
    ratio_bright = (im > 127).mean()
    return min(ratio_bright, 1-ratio_bright)


def is_empty(im, cutoff=CUTOFF):
    if isinstance(im, str):
        im = load_image(im)
        if len(im.shape) == 3:
            im = im[..., 0] / 3 + im[..., 1] / 3 + im[..., 2] / 3

    smaller_dim, larger_dim = sorted(im.shape)
    max_stride = smaller_dim / 10

    scores = [
        score(im[
            x:int(x+max_stride),
            y:int(y+max_stride)
        ])
        for x in range(0, (im.shape[0] - int(max_stride) - 1), int(max_stride))
        for y in range(0, (im.shape[1] - int(max_stride) - 1), int(max_stride))
    ]

    im_score = sum(sorted(scores)[-3:]) / 3
    return im_score < cutoff, im_score


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('-c', dest='cutoff', type=float, default=CUTOFF)
    parser.add_argument('-r', dest='retval', action='store_true')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    empty, im_score = is_empty(args.infile, args.cutoff)
    if args.verbose:
        verdict = '' if empty else 'not '
        print(f"File {args.infile} is {verdict}empty (score: {im_score})")
    if args.retval:
        status=(0 if empty else 1)
        sys.exit(status)

