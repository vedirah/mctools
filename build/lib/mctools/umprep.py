# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:44:51 2020

@author: chohaha
"""
import re

def PREP(abaqus):

    opfile = abaqus + '[prepd]'
    
    with open(abaqus,'r') as read:
        with open(opfile,'w') as write:
            flag = False
            c = 0
            s = ''
            a=0
            oldtype = re.compile('(?<=\=)(.*?)(?=\,)')
            newtype = re.compile('C.*(?<=D)(\d+)')
            excess = re.compile('(?<=\=).*')
            for line in read:
                if flag:
                    if line[0]=='*':
                        flag = False
                        
                #add PART before NODE   
                
                if 'NODE' in line:  
                    write.write('*Part, name=PART-1\n'+line)
                    
                #remove color comments
                
                elif 'COLOR' in line: 
                    continue
                
                #reconcile details for MCNP
                
                elif 'ELEMENT' in line:   
                    flag = True
                    c = 0
                    if a==0:
                        ot = oldtype.search(line).group()   #matches element type NOT NECESSARY
                        nt = newtype.search(ot).group()     #matches mcnp compatible type
                        exc = excess.search(line).group()   #matches all after 'TYPE='
                        nl=line.replace(exc,nt).replace('T,T','T, T') #replaces uncompatible details
                        write.write(nl)
                        a=1
                    else:
                        continue
                    
                #remove hmassem comments    
                
                elif 'HMASSEM' in line: 
                    continue   
                
                #remove hmname comments
                
                elif 'HMNAME' in line:
                    continue
                                    
                #ending part, instance, assembly etc
                
                elif '*****' in line:
                    write.write('*End Part\n**\n**\n** ASSEMBLY\n**\n*Assembly, na\
me=Assembly\n**\n*Instance, name=PART-1-1, part=PART-1\n*End Instance\n*End Assembly\n')
                    write.write(line)
                    
                #for 2nd tet to put element data on one line per element
                
                elif flag:
                    if nt == 'C3D10':
                        if c==0:
                            s = line[:-1]
                            c =1
                        elif c ==1:
                            write.write(s+line)
                            c = 0
                    else:
                        write.write(line)
                else:
                    write.write(line)