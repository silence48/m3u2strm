import re
import os

def verifyURL(line):
  verifyurl  = re.compile('://').search(line)
  if verifyurl:
    return True
  return

def tvgTypeMatch(line):
  typematch = re.compile('tvg-type=\"(.*?)\"', re.IGNORECASE).search(line)
  if typematch:
    return typematch
  return
  
def ufcwweMatch(line):
  ufcwwematch = re.compile('[U][f][c]|[w][w][e]|[r][i][d][i][c][u][l]', re.IGNORECASE).search(line)
  if ufcwwematch:
    return ufcwwematch
  return

def airDateMatch(line):
  datematch = re.compile('[1-2][0-9][0-9][0-9][ ][0-3][0-9][ ][0-1][0-9]|[1-2][0-9][0-9][0-9][ ][0-1][0-9][ ][0-3][0-9]').search(line)
  if datematch:
    return datematch
  return

def tvgNameMatch(line):
  namematch = re.compile('tvg-name=\"(.*?)\"', re.IGNORECASE).search(line)
  if namematch:
    return namematch
  return

def tvidmatch(line):
  tvidmatch = re.compile('tvg-ID=\"(.*?)\"', re.IGNORECASE).search(line)
  if tvidmatch:
    return tvidmatch
  return

def tvgLogoMatch(line):
  logomatch = re.compile('tvg-logo=\"(.*?)\"', re.IGNORECASE).search(line)
  if logomatch:
    return logomatch
  return

def tvgGroupMatch(line):
  groupmatch = re.compile('group-title=\"(.*?)\"', re.IGNORECASE).search(line)
  if groupmatch:
    return groupmatch
  return
      
def infoMatch(line):
  infomatch = re.compile('[,](?!.*[,])(.*?)$', re.IGNORECASE).search(line)
  if infomatch:
    return infomatch
  return

def getResult(re_match):
  return re_match.group().split('\"')[1]
      
def sxxExxMatch(line):
  tvshowmatch = re.compile('[s][0-9][0-9][e][0-9][0-9]|[0-9][0-9][x][0-9][0-9][ ][-][ ]|[s][0-9][0-9][ ][e][0-9][0-9]|[0-9][0-9][x][0-9][0-9]', re.IGNORECASE).search(line)
  if tvshowmatch:
    return tvshowmatch
  tvshowmatch = seasonMatch2(line)
  if tvshowmatch:
    return tvshowmatch
  tvshowmatch = episodeMatch2(line)
  if tvshowmatch:
    return tvshowmatch
  return

def tvgChannelMatch(line):
  tvgchnomatch = re.compile('tvg-chno=\"(.*?)\"', re.IGNORECASE).search(line)
  if tvgchnomatch:
    return tvgchnomatch
  tvgchannelid = re.compile('tvg-chno=\"(.*?)\"', re.IGNORECASE).search(line)
  if tvgchannelid:
    return tvgchannelid
  return

def yearMatch(line):
  yearmatch = re.compile('[(][1-2][0-9][0-9][0-9][)]').search(line)
  if yearmatch:
    return yearmatch
  return

def resolutionMatch(line):
  resolutionmatch = re.compile('HD|SD|720p WEB x264-XLF|WEB x264-XLF').search(line)
  if resolutionmatch:
    return resolutionmatch
  return

def episodeMatch(line):
  episodematch = re.compile('[e][0-9][0-9]|[0-9][0-9][x][0-9][0-9]', re.IGNORECASE).search(line)
  if episodematch:
    if episodematch.end() - episodematch.start() > 3:
      episodenumber = episodematch.group()[3:]
      #print(episodenumber,'E#')
    else:
      episodenumber = episodematch.group()[1:]
      #print(episodenumber,'E#')
    return episodenumber
  return

def episodeMatch2(line):
  episodematch = re.compile('[e][0-9][0-9]|[0-9][0-9][x][0-9][0-9]', re.IGNORECASE).search(line)
  if episodematch:
    return episodematch
  return

def seasonMatch2(line):
  seasonmatch = re.compile('[s][0-9][0-9]', re.IGNORECASE).search(line)
  if seasonmatch:   
    return seasonmatch
  return

def seasonMatch(line):
  seasonmatch = re.compile('[s][0-9][0-9]|[0-9][0-9][x][0-9][0-9]', re.IGNORECASE).search(line)
  if seasonmatch:
    if seasonmatch.end() - seasonmatch.start() > 3:
      seasonnumber = seasonmatch.group()[:3]
      #print(seasonnumber,'s#')
    else:
      seasonnumber = seasonmatch.group()[1:]
      #print(seasonnumber,'s#')
    return seasonnumber
  return

def imdbCheck(line):
  imdbmatch = re.compile('[t][t][0-9][0-9][0-9]').search(line)
  if imdbmatch:
    return imdbmatch
  return

def parseMovieInfo(info):
  if ',' in info:
    info = info.split(',')
  if info[0] == "":
    del info[0]
  info = info[-1]
  if '#' in info:
    info = info.split('#')[0]
  if ':' in info:
    info = info.split(':')
    if resolutionMatch(info[0]):
      info = info[1]
    else:
      info = ':'.join(info)
  return info.strip()
     
def parseResolution(match):
  resolutionmatch = match.group().strip()
  if resolutionmatch == 'HD' or resolutionmatch == '720p WEB x264-XLF':
    return '720p'
  elif resolutionmatch == 'SD' or resolutionmatch == 'WEB x264-XLF':
    return '480p'
  return

def makeStrm(filename, url):
  if not os.path.exists(filename):
    streamfile = open(filename, "w+")
    streamfile.write(url)
    streamfile.close
    print("strm file created:", filename)
    streamfile.close()

def makeDirectory(directory):
  if not os.path.exists(directory):
    os.mkdir(directory)
  else:
    print("directory found:", directory)

def stripYear(title):
  yearmatch = re.sub('[(][1-2][0-9][0-9][0-9][)]|[1-2][0-9][0-9][0-9]', "", title)
  if yearmatch:
    return yearmatch.strip()
  return

def languageMatch(line):
  languagematch = re.compile('[|][A-Z][A-Z][|]', re.IGNORECASE).search(line)
  if languagematch:
    return languagematch
  return

def stripLanguage(title):
  languagematch = re.sub('[|][A-Z][A-Z][|]', "", title, flags=re.IGNORECASE)
  if languagematch:
    return languagematch.strip()
  return

def stripResolution(title):
  resolutionmatch = re.sub('HD|SD|720p WEB x264-XLF|WEB x264-XLF', "", title)
  if resolutionmatch:
    return resolutionmatch.strip()
  return

def stripSxxExx(title):
  sxxexxmatch = re.sub('[s][0-9][0-9][e][0-9][0-9]|[0-9][0-9][x][0-9][0-9][ ][-][ ]|[0-9][0-9][x][0-9][0-9]|[s][0-9][0-9][ ][e][0-9][0-9]', "", title, flags=re.IGNORECASE)
  if sxxexxmatch:
    return sxxexxmatch.strip()
  return

def parseEpisode(title):
  airdate = airDateMatch(title)
  titlelen = len(title)
  showtitle, episodetitle, language = None, None, None
  if airdate:
    showtitle = title[:airdate.start()].strip()
    if airdate.end() != titlelen:
      episodetitle = title[airdate.end():].strip()
    return [showtitle,episodetitle,airdate.group()]
  seasonepisode = sxxExxMatch(title)
  if seasonepisode:
    print(seasonepisode)
    if seasonepisode.end() - seasonepisode.start() > 6 or len(seasonepisode.group()) == 5:
      
      episodetitle = title[seasonepisode.end():].strip()
      seasonnumber = seasonMatch(title)
      episodenumber = episodeMatch(title)
      showtitle = title[:seasonepisode.start()]
      languagem = languageMatch(showtitle)
      if languagem:
        language = languagem.group().strip('|')
        showtitle = showtitle[languagem.end():]
        language2 = languageMatch(showtitle)
        if language2:
          showtitle = showtitle[:language2.start()]
          season = seasonMatch2(showtitle)
          if season:
            showtitle = showtitle[:season.start()]
    else:
      seasonnumber = seasonMatch(title)
      episodenumber = episodeMatch(title)
      showtitle = stripSxxExx(title)
    return [showtitle, episodetitle, seasonnumber, episodenumber, language]
  
 