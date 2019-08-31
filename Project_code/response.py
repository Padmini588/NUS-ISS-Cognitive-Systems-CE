def buttons(title,url):
    buttons=[]
    b={
            "title":title,
            "openUrlAction":{
                "url":url    
                    }
            
            }
    buttons.append(b)
    return buttons        


def suggesstions(val):
    l=[]
    for i in val:
        l.append(dict([('title',i)]))
    return l

def image(url,accessibiityText):
    image= {"url":url,"accessibilityText":accessibiityText}
    return image

def permissions(permissions,context):
    resp = {
                "payload": {
                        "google":{
                                "expectUserResponse":"true",
                                "systemIntent":{
                                        "intent":"actions.intent.PERMISSION",
                                        "data":{
                                                "@type":"type.googleapis.com/google.actions.v2.PermissionValueSpec",
                                                "optContext":context,
                                                "permissions":permissions
                                                }
                                        
                                        }
                                
                                
                                
                                }
                        
                        
                        }
                
                }
    return resp

def response(text):
    d ={"simpleResponse":{"textToSpeech":text}}
    return d
          
def simpleResponse(text,expectedResponse):
    resp={
                    "payload":{
                            "google":{
                                    "expectUserResponse":expectedResponse,
                                    "richResponse":{
                                            "items":[
                                                 {"simpleResponse":{
                                                 "textToSpeech":text
                                                    }
                                            }
                                            ]
                                            }
                                    
                                    }
                            
                            }
                    
                    
                    } 
    return resp

def responseSuggestions(text,sug):
    resp={
                    "payload":{
                            "google":{
                                    "expectUserResponse":True,
                                    "richResponse":{
                                            "items":[
                                                 {"simpleResponse":{
                                                 "textToSpeech":text
                                                    }
                                            }
                                            ],
                                            "suggestions":sug
                                            }
                                    
                                    }
                            
                            }
                    
                    
                    } 
    return resp

def responseSuggestionsLink(text,sug,linkName,url):
    resp={
                    "payload":{
                            "google":{
                                    "expectUserResponse":True,
                                    "richResponse":{
                                            "items":[
                                                 {"simpleResponse":{
                                                 "textToSpeech":text
                                                    }
                                            }
                                            ],
                                            "suggestions":sug,
                                            "linkOutSuggestion": {
                                                    "destinationName": linkName,
                                                    "url": url
                                                    }
                                            }
                                    
                                    }
                            
                            }
                    
                    
                    } 
    return resp

      
def createCard(title,text_description,image=None,button=None,subtitle = None):
    
    if image and button and subtitle:
        card = { "title": title,
                "subtitle":subtitle,
                "formattedText":text_description,
                "image":image,
                "buttons":button,
                "imageDisplayOptions": 'CROPPED' }
    elif image and subtitle:
        card = { "title": title,
                "subtitle":subtitle,
                "formattedText":text_description,
                "image":image,
                "imageDisplayOptions": 'CROPPED' }
    elif button and subtitle:   
        card = { "title": title,
                "subtitle":subtitle,
                "formattedText":text_description,
                "buttons":button,
                }
    elif image and button:
        card = { "title": title,
                "formattedText":text_description,
                "image":image,
                "buttons":button,
                "imageDisplayOptions": 'CROPPED' }
    elif image:
        card = { "title": title,
                "formattedText":text_description,
                "image":image,
                "imageDisplayOptions": 'CROPPED' }
    elif button:
        card = { "title": title,
                "formattedText":text_description,
               "buttons":button,
                "imageDisplayOptions": 'CROPPED' }    
    else:
        card = { "title": title,
                "formattedText":text_description,
                }
        
    return card



def responseCard(text1,text2,card):
    resp={
                    "payload":{
                            "google":{
                                    "expectUserResponse":True,
                                    "richResponse":{
                                            "items":[
                                                 {"simpleResponse":{
                                                 "textToSpeech":text1
                                                    }
                                            }, 
                                             {"basicCard":card},
                                             {
                                                "simpleResponse":{
                                                 "textToSpeech":text2
                                                    }    
                                             }
                                            ]
                                            }
                                    
                                    }
                            
                            }
                    
                    
                    } 
    return resp

def createCarouselWImage(key,title):
    carousel = {
                  "optionInfo": {
                    "key": key,
                    "synonyms": [key]
                  },
                  "title": title
                }
    return carousel

def createCarouselDesc(key,image,description,title):
    carousel = {
                  "optionInfo": {
                    "key": key,
                    "synonyms": [key]
                  },
                  "image": image,
                  "title": title,
                  "description":description
                }
    return carousel

def createCarousel(key,image,title):
    carousel = {
                  "optionInfo": {
                    "key": key,
                    "synonyms": [key]
                  },
                  "image": image,
                  "title": title
                }
    return carousel

def respCarousel(carousels,text):
    resp = {
    "payload": {
      "google": {
        "expectUserResponse": True,
        "systemIntent": {
          "intent": "actions.intent.OPTION",
          "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "carouselSelect": {
              "items": carousels 
            }
          }
        },
        "richResponse": {
          "items": [
            {
              "simpleResponse": {
                "textToSpeech": text
              }
            }
          ]
        }
      }
    }
  }
    return resp

def respCarouselS(carousels,text,sug):
    resp = {
    "payload": {
      "google": {
        "expectUserResponse": True,
        "systemIntent": {
          "intent": "actions.intent.OPTION",
          "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "carouselSelect": {
              "items": carousels 
            }
          }
        },
        "richResponse": {
          "items": [
            {
              "simpleResponse": {
                "textToSpeech": text
              }
            }
          ],
          "suggestions":sug   
        }
      }
    }
  }
    return resp

def respButtonSuggestion(button,text1,text2,sug):
    resp = {
                
                    "payload":{
                            "google":{
                                    "expectUserResponse":True,
                                    "richResponse":{
                                            "items":[
                                                 {"simpleResponse":{
                                                 "textToSpeech":text1
                                                    }
                                            }, 
                                             {"basicCard":button},
                                             {
                                                "simpleResponse":{
                                                 "textToSpeech":text2
                                                    }    
                                             }
                                             ],
                                             "suggestions":sug 
                                             }
                                             
                                             
                                            }
                                    }
                            }
    return resp  