from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from googletrans import Translator

#Functions
'''
---------------------------------
=================================
---------------------------------
'''
def translate(text, source="", destination=""):
    translator = Translator();
    translatedText=""
    ERROR_TEXT = "Something went wrong!"
    DEFAULT_DESTINATION = "hr"

    if (source == "" and destination == ""):
        try: 
            translatedText = translator.translate(text, dest=DEFAULT_DESTINATION).text
        except ValueError:
            translatedText = ERROR_TEXT
    
    elif (source == "" and destination != ""):
        try: 
            translatedText = translator.translate(text, dest=destination).text
        except ValueError:
            translatedText = ERROR_TEXT
    
    else:
        try: 
            translatedText = translator.translate(text, src=source, dest=destination).text
        except ValueError:
            translatedText = ERROR_TEXT

    return translatedText

def parse(argument):
    text=""
    src=""
    dest=""

    try:
        temp = -1
        counter = 0
        for i in range (len(argument)):
            if (argument[i] == ":" and counter == 0):
                dest += argument[i+1] + argument[i+2]
                temp = i
                counter = 1
                for j in range (i+1, len(argument)):
                    if (argument[j] == ":"):
                        src += argument[j+1] + argument[j+2]
                        temp = j
            if (temp == -1 and argument[i] != " "):
                temp = i-2
                text += argument[i]

            if (i > temp+2):
                text += argument[i]
            
    except IndexError:
        pass

    return text, src, dest

'''
---------------------------------
=================================
---------------------------------
'''

# Class decleration
class GoogleTranslateExtension(Extension):

    def __init__(self):
        super(GoogleTranslateExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        argument = event.get_argument()
        text, src, dest = parse(argument)
        translation = translate(text, src, dest)

        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=translation,
                                                           on_enter=HideWindowAction())])

        
if __name__ == '__main__':
    GoogleTranslateExtension().run();
