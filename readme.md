# start
```bash
#### click open and select pixel model
python python/qt5.py
```

# process
```bash
#### together we have two structures for image signal processing,ISP and Pipeline
#### ISP is for pixel division and is the channel to pipeline
#### Pipeline works mainly for image signal processing.
#### In function 'execute', Pipeline gets all modules listed in test.yaml  
#### Then Pipeline runs the modules in their order
#### dpc is dead pixel correction, with input [H,W] and output [H,W]
#### blc is black level compensation, with input [H,W] and output [H,W]
#### aaf is anti-aliasing filter, with input [H,W] and output [H,W]
#### awb is auto white balance, with input [H,W] and output [H,W]
#### cnf is chroma noise filtering, with input [H,W] and output [H,W]
#### cfa is color filter array interpolation, with input [H,W] and output [H,W,3]
#### ccm is color correction matrix, with input [H,W,3] and output [H,W,3]
#### gac is gamma correction, with input [H,W,3] and output [H,W,3]
#### csc is color space convertion, with input [H,W,3] and output [H,W,3]
#### nlm is non-local means denoising, with input [H,W,3] and output [H,W,3]
#### bnf is bilateral noise filtering, with input [H,W,3] and output [H,W,3]
#### ceh is contrast enhancement, with input [H,W,3] and output [H,W,3]
#### eeh is edge enhancement, with input [H,W,3] and output [H,W,3]
#### fcs is false color correction, with input [H,W,3] and output [H,W,3]
#### hsc is hue saturation control, with input [H,W,3] and output [H,W,3]
#### bcc is brightness contrast control, with input [H,W,3] and output [H,W,3]
#### above is all modules to be processed, further modules like flat field correction will be added 
```

# result
```bash
#### we save all the images ina new file in 'Image'
#### in Pipeline we can choose whether to save the images towards each inner process
```