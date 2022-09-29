cirillic = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'yi',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ш': 'sh',
    'щ': 'sch',
    'ь': '',
    'ъ': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    'ч': 'ch',
    'ы': 'i',
}


def cirillic_to_eng(word: str):
    word = word.replace(' ', '_').lower()
    s = ''
    for ch in word:
        s += cirillic.get(ch, ch)
    return s