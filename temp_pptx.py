# -*- coding: utf-8 -*-  
import zipfile  
z=zipfile.ZipFile(r'd:\game\socialSimulation\Ä£ÄâÉç»á.pptx','r')  
for n in z.namelist():  
    if 'slide' in n.lower():  
        print(n)  
