import pandas as pd

def main():
    # csvをloadする
    df = pd.read_csv('outputs/frequency.csv', header=0)
    print(df)

    df_filtered = filter_df(df)
    print(df_filtered)

    # CSVに書き出す
    write_csv(df_filtered, 'outputs/filtering.csv')


def filter_df(df):
    # 頻度の低すぎるものと高すぎるものを削除
    df_filtered = df[(df.frequency >= 20) & (df.frequency <= 1344)]
    # 先頭の中黒と伸ばし棒を削除
    df_filtered = df_filtered[df_filtered['keyword'].str.match('^[^・ー].+')]
    return df_filtered


def frequency_count(df):
    frequency_series = df['word'].value_counts()
    return pd.DataFrame(frequency_series)


def write_csv(df, path):
    df.to_csv(path, index=False)


def separate_tsv_text(text):
    result_list = text.split('\t')
    return result_list


def create_word_list_df(series):
    df = pd.DataFrame(columns=['word'])
    values = series.values
    for idx in range(series.shape[0]):
        l = separate_tsv_text(values[idx])
        print(l)
        tmp_df = pd.DataFrame(data=l, columns=df.columns)
        df = df.append(tmp_df, ignore_index=True)
    return df


if __name__ == '__main__':
    main()

