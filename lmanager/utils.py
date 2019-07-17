def decode(self, ls):
    result = ''
    pad_count = 0

    for i in ls:
        if int(i) != 0:
            result += self.reverse_word_index.get(i, '?') + ' '
        else:
            pad_count += 1

    if pad_count > 0: result += '<PAD>' + '(x' + str(pad_count) + ')'
    # return ' '.join([self.reverse_word_index.get(i, '?') for i in ls])
    return result

def encode(self, text):
    text_ls = []
    for i in text.split():
        try:
            text_ls.append(self.word_index[i])
        except KeyError:
            self.lbl3_6.set_text(self.lbl3_6.get_text() + i + ' ')
            print('Unhandled word \'' + i + '\'')
    return text_ls

def decode_single(self, text):
    return self.reverse_word_index.get(text)

def encode_single(self, text):
    return self.word_index.get(text)

def insert_start(self, ls):
    ls.insert(0, 1)
    return ls
