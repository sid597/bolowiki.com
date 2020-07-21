from googletrans import Translator
translator=Translator()
print(translator.translate('हैलो।',dest="en"))
print(translator.translate('안녕하세요.', dest='en'))

