import pandas as pd
import glob
import re

file_path = 'E:/data/corpus/peoplepaper/'
file_name = glob.glob(file_path+'*.txt')

flag = {'nr': 'PERSON_NAME', 'ns': 'LOCAL_NAME', 'nt': 'ORG_NAME', 'nz': 'OTHER_NAME', 't': 'DDCT', 'n': 'NOUN'}


def strQ2B(ustring):
    """全角转半角"""
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374: #全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring


def func(data, person_name, concat_person_name):            # 去掉人名空格部分
    result = []
    for (i, j), k in zip(zip(person_name['person_name'], concat_person_name['concat_person_name']), data['sentence']):
        for p_c in [('  '.join(p), l) for p, l in zip(i, j)]:
            k = re.sub(p_c[0], p_c[1], k)
        k = strQ2B(k)
        result.append(k)
    return result


with open(file_path+'/People_daily_BI_data', 'w', encoding='utf-8') as f:
    for num, file in enumerate(file_name):
        print(num, file)
        data = pd.read_csv(file, names=['sentence'], index_col=None, delimiter='9999', encoding='utf-8')
        data = data.applymap(lambda x: str(x).split('  ', 1)[-1])

        pattern = '([\u4e00-\u9fa5]+/nr)  ([\u4e00-\u9fa5]+/nr)'

        person_name = data.applymap(lambda x: re.findall(pattern, str(x)))
        person_name.rename(columns={'sentence': 'person_name'}, inplace=True)

        concat_person_name = pd.DataFrame(person_name).applymap(lambda x: [''.join(i).replace('/nr', '', 1) for i in x])
        concat_person_name.rename(columns={'person_name': 'concat_person_name'}, inplace=True)

        result = pd.DataFrame(func(data, person_name, concat_person_name))
        result.rename(columns={0: 'sentence'}, inplace=True)
        print(result)
        # for line in result.applymap(lambda x: str(x).split('  '))['sentence']:
        #     for i in line:
        #         _ = i.split('/')
        #         if _[1] in flag:
        #             num = 0
        #             for w in _[0]:
        #                 if num == 0:
        #                     f.writelines(w + ' B-' + flag[_[1]] + '\n')
        #                     num += 1
        #                     continue
        #                 f.writelines(w + ' I-' + flag[_[1]] + '\n')
        #
        #         else:
        #             for w in _[0]:
        #                 f.writelines(w + ' O\n')
        #     f.writelines('\n')
