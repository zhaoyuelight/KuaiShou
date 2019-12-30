fontscn_h57yip2q = {
    '\\uabcf': '4',
    '\\uaced': '3',
    '\\uaedd': '8',
    '\\uaede': '0',
    '\\uafcd': '6',
    '\\ubdaa': '5',
    '\\ubdcd': '1',
    '\\ubfad': '9',
    '\\uccda': '2',
    '\\ucfbe': '7',
}
fontscn_3jqwe90k = {
    '\\uaacb': '4',
    '\\uabcd': '3',
    '\\uacdd': '0',
    '\\uaefb': '8',
    '\\uafbc': '6',
    '\\ubbca': '1',
    '\\ubdca': '5',
    '\\ubfee': '9',
    '\\uccac': '2',
    '\\ucfba': '7',
}
fontscn_yuh4hy4p = {
    '\\uaabd': '5',
    '\\uaadd': '0',
    '\\uacde': '9',
    '\\uadaa': '2',
    '\\uadac': '1',
    '\\uadcb': '7',
    '\\uaeed': '8',
    '\\ubebb': '3',
    '\\ucbdc': '6',
    '\\ucccf': '4',
}
fontscn_qw2f1m1o = {
    '\\uabcb': '4',
    '\\uaccd': '3',
    '\\uacda': '0',
    '\\uaeff': '8',
    '\\uafbb': '6',
    '\\ubdca': '1',
    '\\ubdcc': '5',
    '\\ubfef': '9',
    '\\uccaa': '2',
    '\\ucfba': '7',
}
fontscn_yx77i032 = {
    '\\uabce': '4',
    '\\uaccd': '6',
    '\\uaeda': '8',
    '\\uaefe': '0',
    '\\uafed': '3',
    '\\ubaaa': '5',
    '\\ubddd': '1',
    '\\ubfad': '2',
    '\\ubfae': '9',
    '\\uc44f': '7',
}

class Jiemi(object):
    def __init__(self):
        pass
    @staticmethod
    def getCnString(argument, jiemi_key):
        woff_dict = {'h57yip2q': fontscn_h57yip2q, '3jqwe90k': fontscn_3jqwe90k, 'yuh4hy4p': fontscn_yuh4hy4p,
                     'qw2f1m1o': fontscn_qw2f1m1o, 'yx77i032': fontscn_yx77i032}
        li = []
        new_data = (list(map(lambda x: x.encode('unicode_escape'), argument)))
        # print(new_data,'这个值是new_data')

        for i in new_data:
            if len(str(i)) > 5:
                num = woff_dict[jiemi_key][str(i)[3:-1]]
                li.append(num)
            else:
                li.append(str(i)[2:-1])


        res = ''.join(li)
        # print(res)
        return res

if __name__ == '__main__':
    jm = Jiemi()
    jm.getCnString('뷝ꯎ쑏껾', 'yx77i032')





