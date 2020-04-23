from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import json
import qrcode
import qrcode.image.svg
import time

class WpRestApi:
    def __init__(self):
        load_dotenv(dotenv_path=Path.cwd()/'.env')
        self.createBulkPost(int(os.getenv('LIMIT')))

    def createBulkPost(self,limit):
        for x in range(limit):
            data={
                "title":os.getenv('TITLE_PREFIX') + ' ' + str(x),
                "description":os.getenv('DESCRIPTION_PREFIX')+ str(x),
                "categories":{17},
                "status":os.getenv('STATUS'),
                "slug":os.getenv('SLUG') + str(x),
            }
            slug = self.createPost(data)
            self.createQrCode(slug)
            print(os.getenv('API_DOMAIN')+slug+' created!')
            time.sleep(1)

    def createPost(self,data={}):
        slug = os.getenv('CREATE_POST')
        return self.doRequest(slug=slug,data=data)

    def doRequest(self,slug,data={}):
        try:
            r = requests.post(os.getenv('API_DOMAIN')+slug,auth=(os.getenv('API_USER'),os.getenv('API_PASS')),data=data)
        except requests.exceptions.RequestException as err:
            return ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            return ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            return ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            return ("Timeout Error:",errt)  
        
        return r.json()['slug']
    
    def createQrCode(self,slug):
        img = qrcode.make(os.getenv('API_DOMAIN')+slug)
        img_file = os.getcwd()+'\\'+os.getenv('IMG_DIR')+'\\'+slug+'.png'
        img.save(img_file)
        
        img = qrcode.make(os.getenv('API_DOMAIN')+slug, image_factory = qrcode.image.svg.SvgImage)
        img_file = os.getcwd()+'\\'+os.getenv('IMG_DIR')+'\\'+slug+'.svg'
        img.save(img_file)