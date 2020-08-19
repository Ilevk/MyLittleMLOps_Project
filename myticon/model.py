import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from myticon.pix2pix.models import create_model
from myticon.utils import TestOptions

def load_model():
    opt = TestOptions()  # get test options
    # hard-code some parameters for test
    opt.dataset_mode = 'aligned'
    opt.model = 'pix2pix'
    opt.gpu_ids = []
    opt.isTrain = False
    opt.checkpoints_dir = './myticon/pix2pix/checkpoints'
    opt.name = 'myticon_pix2pix'
    opt.preprocess = 'resize_and_crop'
    opt.input_nc = 3
    opt.output_nc = 3
    opt.ngf = 64
    opt.nbf = 64
    opt.netG = 'unet_256'
    opt.netD = 'basic'
    opt.norm = 'batch'
    opt.no_dropout=False
    opt.init_type = 'normal'
    opt.init_gain = 0.02
    opt.direction='AtoB'
    opt.num_threads = 1   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    opt.load_iter = 200
    opt.phase = 'test'

    model = create_model(opt)      # create a model given opt.model and other options
    model.load_networks(200)
    model.eval()

    return model
    