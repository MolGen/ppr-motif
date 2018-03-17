# PPR Motif Annotation using Neural Network

## Overview  
This is the code and weight files to run and deploy the Flask app [PPR motif](https://ppr-motif.appspot.com/), which uses pre-trained Keras model to predict 10 different variants of [PPR motif](http://onlinelibrary.wiley.com/doi/10.1111/tpj.13121/full#tpj13121-sec-0002). However, we still use [PROSITE model](https://prosite.expasy.org/PDOC51375) of the PPR motif.

## Sequence logo of *Arabidopsis thaliana* PPR motif variants  
P    
![P](static/Logo/P.png)  
P1   
![P1](static/Logo/P1.png)  
P2   
![P2](static/Logo/P2.png)  
L1   
![L1](static/Logo/L1.png)  
L2   
![L2](static/Logo/L2.png)  
S1   
![S1](static/Logo/S1.png)  
S2   
![S2](static/Logo/S2.png)  
SS   
![SS](static/Logo/SS.png)  
E1   
![E1](static/Logo/E1.png)  
E2   
![E2](static/Logo/E2.png)  

## Dependencies  
```sudo pip install -r requirements.txt```

## Todo 
- [ ] Bugs
    - [x] Handling inputs.
    - [x] Bed format coordinates (0-based exclusive) of the features.
    - [ ] Ending positions of the features.
- [ ] Optimization
    - [ ] Variable length features (pad_sequences?).
    - [ ] Unbalanced training set (sample_weight?).
    - [ ] Under-represented classes (class_weight?).
- [ ] Enhancement
    - [ ] Setting maximum number of query sequences.  
    - [x] Loading example query sequences from file.  
    - [ ] Uploading query sequences from file.  
    - [ ] Displaying and downloading annotations in either bed or GFF3 format.  
