import pafy 
 

def retrieveVideo(url = "https://www.youtube.com/watch?v=6zQkbTzN8yY"):
  video = pafy.new(url)
  best  = video.getbest()
  try:
    return best.url
  except Exception as e:
    raise e