import pandas as pd
import os


def main():
    os.chdir('scraping_python')
    path = os.getcwd()

    # csvをloadする
    series = get_word_list_from_csv('outputs/keyword_list.csv')
    # series = get_word_list_from_csv('outputs_test/keyword_list_test.csv')

    print(series)

    # keywordの\t区切りの文字列をListにしてDFにAppendしていく
    df = create_word_list_df(series)
    print(df)

    # 頻度の計算をする
    frequency_df = frequency_count(df)
    # 頻度が1のものは捨てる
    df_filtered = filter_df(frequency_df)
    # キーワードが格納されているindexをカラムにする
    df_filtered.reset_index(inplace=True)
    df_filtered.rename(columns={'index': 'keyword', 'word': 'frequency'}, inplace=True)
    # CSVに書き出す
    write_csv(df_filtered, 'outputs/frequency.csv')


def filter_df(df):
    df_filtered = df[df.word >= 2]
    return df_filtered


def frequency_count(df):
    frequency_series = df['word'].value_counts()
    return pd.DataFrame(frequency_series)


def write_csv(df, path):
    df.to_csv(path, index=False)


def separate_tsv_text(text):
    result_list = text.split('\t')
    return result_list


def get_word_list_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path, header=0)
    return df['word_list']


def create_word_list_df(series):
    df = pd.DataFrame(columns=['word'])
    values = series.values
    for idx in range(series.shape[0]):
        l = separate_tsv_text(values[idx])
        # print(l)
        tmp_df = pd.DataFrame(data=l, columns=df.columns)
        df = df.append(tmp_df, ignore_index=True)
    return df


if __name__ == '__main__':
    main()
