import dbaser
import re

        
        
#def tohrs(seconds):              <= Worked in python 2.7
#  z=seconds
#  h=z/3600 
#  m=z%3600/60 
#  s=z%3600%60
#  hr = str(h) + ":" + str(m)
#  return hr
#  
  
        
def tohrs(seconds):
  a=seconds
  h=((a//3600))%24
  m=(a//60)%60
  s=a%60
  if m<10:
      m=str('0'+str(m))
  else:
      m=str(m)
  if s<10:
      s=str('0'+str(s))
  else:
      s=str(s)
  hr=str(h)+':'+str(m)
  return hr
