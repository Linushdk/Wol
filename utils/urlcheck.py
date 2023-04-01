from urllib.request import urlopen
import validators

def is_url_image(url):
    if "discordapp.com" in url:
        return False    
    else:    
        if is_string_url(url): 
            image_formats = ("image/png", "image/jpeg", "image/gif")
            site = urlopen(url)
            meta = site.info()
            if meta["content-type"] in image_formats:
                return True
            else: 
                return False
        else:
            return False 

def is_string_url(url):
    return validators.url(url)


