# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 10:48:16 2022

@author: srira
"""
import os
import torch
import argparse
import numpy as np
import torchvision.transforms as transforms 
from hparams import hparams as hps
from torch.utils.data import DataLoader
from utils.util import mode
from utils.dataset import I2SData, pad_collate,pad_collate_BU
from model.model import I2SModel
from waveglow.denoiser import Denoiser
from scipy.io.wavfile import write




def prepare_dataloaders(fdir,split,args):
    imsize = hps.img_size
    image_transform = transforms.Compose([
        transforms.Resize(int(imsize * 76 / 64)),
        transforms.RandomCrop(imsize),
        transforms.RandomHorizontalFlip()])
    dataset = I2SData(args,fdir,split,imsize,transform=image_transform)
    data_loader = DataLoader(dataset, num_workers = 2, shuffle = False,
                                pin_memory = True,
                                drop_last = False)
    return data_loader

def infer(model,val_loader,args,epoch,waveglow=None):
	model.eval()
	i = 0
	for imgs,vis_info, keys in val_loader:
		imgs = imgs.float().cuda()
		vis_info = vis_info.float().cuda()
		with torch.no_grad():
			output = model.inference(imgs,vis_info)
		mel_outputs, mel_outputs_postnet, _ ,_, mel_lengths= output

		with torch.no_grad():
			audios = waveglow.infer(mel_outputs_postnet,sigma=hps.sigma_infer)
			audios = audios.float()
			audios = denoiser(audios, strength=hps.denoising_strength).squeeze(1)
		
		for j, audio in enumerate(audios):
			i += 1
			key = keys[j]
			root = os.path.join(args.save_path,'audios',str(epoch))
			if not os.path.exists(root):
				os.makedirs(root)
			path = os.path.join(root,key) + '.wav'
			audio = audio[:mel_lengths[j]*hps.seft_hop_length*hps.n_frames_per_step]
			audio = audio/torch.max(torch.abs(audio))
			write(path, 22050, (audio.cpu().numpy()*32767).astype(np.int16))
			print('processed {} audio'.format(i))
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data_dir', type = str, default = 'Data_for_SAS',
						help = 'directory to load data')
    parser.add_argument('--waveglow_model',type=str,default = 'waveglow_256channels.pt')
    parser.add_argument('-o','--save_path',type=str,default='output')
    parser.add_argument('--img_format',type=str,default='BU',choices=['BU','vector','tensor','img'])
    parser.add_argument('--start_epoch',type=int,default=0)
    parser.add_argument('--max_epoch',type=int,default=1100)
    parser.add_argument('--result_file',type=str,default='results')
    parser.add_argument('--gamma1',type=float,default=0.5,
						help = 'parameter of the image embedding constraint loss')
    parser.add_argument('--only_val',action="store_true",default=True,
						help = 'true for synthesizing speech in inference stage')
    parser.add_argument('--k',type=int,default=160,
						help = 'parameter of the inverse sigmoid in scheduled sampling')
    parser.add_argument('--m',type=float,default=0.025,
						help = 'max sampling rate of inferred spectrogram frames in scheduled sampling')
    parser.add_argument('--scheduled_type',type=str,default='sigmoid',choices=['sigmoid', 'linear','exp'])
    args = parser.parse_args()

    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = False # faster due to dynamic input shape
    args.save_path = os.path.join(args.save_path)
    val_loader = prepare_dataloaders(args.data_dir,'test',args)	
    model = I2SModel(args)
    mode(model, True)

    waveglow_path = args.waveglow_model
    waveglow = torch.load(waveglow_path)['model']
    denoiser = Denoiser(waveglow).cuda()

    print ('start processing epoch')
    model.load_state_dict(torch.load("%s/models/I2SModel_%d.pth" % (args.save_path,1100))) 
    infer(model,val_loader,args,args.start_epoch,waveglow)
