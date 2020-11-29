import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re


def main():
    os.chdir('scraping_python')
    path = os.getcwd()

    csv_files = load_csv_files('csv_files')
    df = create_link_df(csv_files)
    scripe_url(df)
    write_csv(df, 'outputs/keyword_list.csv')
    print(df)


def write_csv(df, path):
    df.to_csv(path)


# 1行ずつURLからBodyのデータを取得する
# ref: https://kunai-lab.hatenablog.jp/entry/2018/04/08/134924
def scripe_url(df):
    link_series = df['link']
    values = link_series.values
    # body_list = []
    word_list = []
    for idx in range(link_series.shape[0]):
        text = extract_body(values[idx])
        keyword_list = search_katakana_words(text)
        # body_list.append(text)
        word_list.append(keyword_list)
    # df['body'] = pd.DataFrame(body_list)
    df['word_list'] = pd.DataFrame(word_list)


def search_katakana_words(text):
    result_list = re.findall(r'[ァ-ヴー・]{2,}', text)
    result_set = set(result_list)
    return '\t'.join(result_set)


def extract_body(url):
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    body = soup.find('body').get_text()
    # 空白改行コード削除して' ' に置き換え
    body = re.sub(r',,+', ', ', re.sub(r'[\r\n\t\s]', ' ', body))
    return body


def create_link_df(csv_files):
    df = pd.DataFrame({'link': []})
    for i in csv_files:
        _tmp = filter_link_from_csv(i)
        _df = _tmp.to_frame('link')
        df = df.append(_df)
    return df


def load_csv_files(dic_path):
    file_names = os.listdir(dic_path)
    return [f'{dic_path}/{i}' for i in file_names]


def filter_link_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path, header=0)
    return df['link-href']


if __name__ == '__main__':
    main()
