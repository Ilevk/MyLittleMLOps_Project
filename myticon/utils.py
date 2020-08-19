import argparse

import cv2
import numpy as np

from torchvision import transforms
from PIL import Image, ImageFilter

from myticon.pix2pix.options.base_options import BaseOptions
from myticon.pix2pix.util.util import tensor2im

def pre_prop(image_pil):
    img_arr = np.array(image_pil) 

    l2b = np.vectorize(lambda x: -1 if x < 5 else x)
    w2b = np.vectorize(lambda x: 0 if x > 235 else x)
    b2l = np.vectorize(lambda x: 0 if x == -1 else x)
    
    img_arr = b2l(w2b(l2b(img_arr)))

    image = Image.fromarray(img_arr.astype(np.uint8))
    return image

def post_prop(image_tensor, aspect_ratio=1.0):
    image_numpy = tensor2im(image_tensor)
    image_pil = Image.fromarray(image_numpy)
    h, w, _ = image_numpy.shape

    if aspect_ratio > 1.0:
        image_pil = image_pil.resize((h, int(w * aspect_ratio)), Image.BICUBIC)
    if aspect_ratio < 1.0:
        image_pil = image_pil.resize((int(h / aspect_ratio), w), Image.BICUBIC)
        
    return image_pil.filter(ImageFilter.GaussianBlur).filter(ImageFilter.SMOOTH())

def image_loader(img):
    """load image, returns cuda tensor"""
    loader = transforms.Compose([transforms.Resize((256, 256), Image.BICUBIC), 
                                 transforms.ToTensor(), 
                                 transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    
    image = loader(img).float()
    image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
    return image  #assumes that you're using GPU

class TestOptions(BaseOptions):
    """This class includes test options.

    It also includes shared options defined in BaseOptions.
    """
    def __init__(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser = BaseOptions.initialize(self, parser)  # define shared options
        parser.add_argument('--ntest', type=int, default=float("inf"), help='# of test examples.')
        parser.add_argument('--results_dir', type=str, default='./results/', help='saves results here.')
        parser.add_argument('--aspect_ratio', type=float, default=1.0, help='aspect ratio of result images')
        parser.add_argument('--phase', type=str, default='test', help='train, val, test, etc')
        # Dropout and Batchnorm has different behavioir during training and test.
        parser.add_argument('--eval', action='store_true', help='use eval mode during test time.')
        parser.add_argument('--num_test', type=int, default=50, help='how many test images to run')
        # rewrite devalue values
        parser.set_defaults(model='test')
        # To avoid cropping, the load_size should be the same as crop_size
        parser.set_defaults(load_size=parser.get_default('crop_size'))
        self.isTrain = False