import re

def verifyURL(line):
  verifyurl  = re.compile('://').search(line)
  if verifyurl:
    return True
  return False

def tvgTypeMatch(line):
  typematch = re.compile('tvg-type=\"(.*?)\"', re.IGNORECASE).search(streaminfo)
  if typematch:
    return typematch
  return False
  
def airDateMatch(line):
  datematch = re.compile('[1-2][0-9][0-9][0-9][ ][0-3][0-9][ ][0-1][0-9]').search(info)
  if datematch:
    return datematch
  return False

def tvgNameMatch(line):
  namematch = re.compile('tvg-name=\"(.*?)\"', re.IGNORECASE).search(thisline)
  if namematch:
    return namematch
  return False

def tvidmatch(line):
  tvidmatch = re.compile('tvg-ID=\"(.*?)\"', re.IGNORECASE).search(thisline)
  if tvidmatch:
    return tvidmatch
  return False

def tvgLogoMatch(line):
  logomatch = re.compile('tvg-logo=\"(.*?)\"', re.IGNORECASE).search(thisline)
  if logomatch:
    return logomatch
  return False

def tvgGroupMatch(line):
  groupmatch = re.compile('group-title=\"(.*?)\"', re.IGNORECASE).search(thisline)
  if groupmatch:
    return groupmatch
  return False
      
def infoMatch(line):
  infomatch = re.compile('[,](?!.*[,])(.*?)$', re.IGNORECASE).search(thisline)
  if infomatch:
    return infomatch
  return False

def getResult(re_match):
  return re_match.group().split('\"')[1]
      
def sxxExxMatch(line):
  tvshowmatch = re.compile('[s][0-9][0-9]&[e][0-9][0-9]', re.IGNORECASE).search(streaminfo)
  if tvshowmatch:
    return tvshowmatch
  tvshowmatch = re.compile('[0-9][0-9][x][0-9][0-9]', re.IGNORECASE).search(streaminfo)
  if tvshowmatch:
    return tvshowmatch
  return False

def tvgChannelMatch(line):
  tvgchnomatch = re.compile('tvg-chno=\"(.*?)\"', re.IGNORECASE).search(thisline)
  if tvgchnomatch:
    return tvgchnomatch
  tvgchannelid = re.compile('tvg-chno=\"(.*?)\"', re.IGNORECASE).search(thisline)
  if tvgchannelid:
    return tvgchannelid
  return False


      tvid = tvidmatch.group().split('\"')[1]
        print(tvid, 'tvid')
      
      
        logo = logomatch.group().split('\"')[1]
        print(logo, 'logo')
      
      
        group = groupmatch.group().split('\"')[1]
        print(group, 'group')
      
      
        info = infomatch.group().strip()

        resolutionmatch = re.compile('HD or SD').search(info)
        if resolutionmatch:
          if resolutionmatch.group() == 'HD':
            resolution = '720p'
          else:
            resolution = '480p'
          print(resolution, 'res')

        yearmatch = re.compile('[1-2][0-9][0-9][0-9]').search(info)
        if yearmatch:
          year = yearmatch.group()
          print(year,'year')
          datematch = re.compile('[1-2][0-9][0-9][0-9][ ][0-3][0-9][ ][0-1][0-9]').search(info)
          if datematch:
            date = datematch.group()
            streamtype = 'vod'
            print(date,'date')

        if streamtype == 'vod':
          seasonmatch = re.compile('[s][0-9][0-9]', re.IGNORECASE).search(info)
          if seasonmatch:
            print(seasonmatch.group(), 'season')
          
          episodematch = re.compile('[e][0-9][0-9]', re.IGNORECASE).search(info)
          if episodematch:
            print(episodematch.group(), 'episode')
        print(info,'firstinfo')
        if ',' in info:
          info = info.split(',')
        if info[0] == "":
          del info[0]
        info = info[0]
        if ':' in info:
          info = info.split(':')

        print(info,'lastinfo')
  def parseResolution(self, info):
    resolutionmatch = re.compile('HD|SD').search(info)
    if resolutionmatch:
      if resolutionmatch.group() == 'HD':
        resolution = '720p'
      else:
        resolution = '480p'
      print(resolution, 'res')