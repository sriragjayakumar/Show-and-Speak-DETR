# Show-and-Speak-DETR
In recent times, developments in the fields of image captioning have proposed novel models such as show and speak (SAS) which directly synthesize spoken description of images, bypassing the need for any text or phonemes. The basic structure of SAS is an encoder-decoder architecture that takes an image as input and predicts the spectrogram of speech that describes this image. The final speech audio is obtained from the predicted spectrogram via WaveNet. Further, SAS uses recurrent neural network-based models such as LSTMs for speech production. We propose to investigate in this study the use of transformers for SAS models to generate Bottom-up-Features, given the superior performance of transformers for generating sequential data.<br />
Use DETR_HF.ipynb to generate the BU using DETR.<br />
The required pretrained waveglow model for this project can be obtained by executing the following: 
```
import gdown
waveglow_pretrained_model = 'waveglow_old.pt'
gdown.download('https://drive.google.com/uc?id=1WsibBTsuRg_SF2Z6L6NFRTT-NjEy1oTx', waveglow_pretrained_model, quiet=False) 
``` 

Use app.py to run streamlit dashboard
#### Reference <br/>
[SHOW AND SPEAK: DIRECTLY SYNTHESIZE SPOKEN DESCRIPTION OF IMAGES](https://arxiv.org/abs/2010.12267).
