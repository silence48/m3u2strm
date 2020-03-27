import tools
import logger
import streamClasses
import wget
import sys

ipttvurl = 'https://tv123.me/m3u.php' #replace url with your link, or comment this line out and put the filename in the streamlist below.
'''for i in range(20):
  url = baseurl + str(i)
  print(wget.download(url, ('m3u/apollotvshows-'+str(i)+'.m3u')))
  apollolist = streamClasses.rawStreamList('m3u/apollotvshows-'+str(i)+'.m3u')'''

print(wget.download(iptmovieurl, ('m3u/iptmovies.m3u'))) #if not downloading comment out this line.
apollomovies = streamClasses.rawStreamList('m3u/iptmovies.m3u')

