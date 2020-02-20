import re, hgtk

def hangul_jamosplit(sentence, EMPTY_JS_CHAR):
    import hgtk
    dg_jamo = {'ㅋ':'Gㄱ', 'ㅌ':'Gㄷ', 'ㅍ':'Gㅂ', 'ㅊ':'Gㅈ',
               'ㄲ':'Dㄱ', 'ㄸ':'Dㄷ', 'ㅃ':'Dㄷ', 'ㅆ':'Dㅅ', 'ㅉ':'Dㅈ'}
    mix_vowel = {'ㅐ':'ㅏㅣ', 'ㅔ':'ㅓㅣ', 'ㅒ':'ㅑㅣ',
                 'ㅖ':'ㅕㅣ', 'ㅘ':'ㅗㅏ', 'ㅙ':'ㅗㅏㅣ',
                 'ㅝ':'ㅜㅓ', 'ㅞ':'ㅜㅓㅣ', 'ㅚ':'ㅗㅣ',
                 'ㅟ':'ㅜㅣ', 'ㅢ':'ㅡㅣ'}
    result = []
    for word in sentence.split(' '):
        decomposed_word = ''
        for char in word:
            try:
                cho_joong_jong = list(hgtk.letter.decompose(char))
                try :
                    cho_joong_jong[0] = dg_jamo[cho_joong_jong[0]]
                except KeyError:
                    cho_joong_jong[0] = cho_joong_jong[0]
                try :
                    cho_joong_jong[1] = mix_vowel[cho_joong_jong[1]]
                except KeyError:
                    cho_joong_jong[1] = cho_joong_jong[1]    
                cho_joong_jong = tuple(cho_joong_jong)
                char_seq = ""
                for cvc in cho_joong_jong:
                    if cvc == '':
                        cvc = EMPTY_JS_CHAR
                    char_seq += cvc
                decomposed_word += char_seq
            except hgtk.exception.NotHangulException:
                decomposed_word += char
                continue
        result.append(decomposed_word)
    return " ".join(result)

def jamo_split(sentence) :
    result = pre_jamo_split(re.sub(r'([_?!~])\1+', r'\1',re.sub(' ', '_',re.sub('[-=+#/,.ㆍ\:$@*\"※~&%』\\‘|\(\)\[\]\<\>`\'…》]',
                                       ' ',sentence))))
    return result