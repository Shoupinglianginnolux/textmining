import json
import pandas as pd


def json2df(json_table):
    df = pd.DataFrame()
    sheet = json_table[0]['model'].split('.')[-1]
    for i in range(len(json_table)):
        json_data = json_table[i]
        df_data = pd.json_normalize(json_data['fields'])
        df = pd.concat([df, df_data])
    df = df.reset_index(drop=True)
    
    return sheet, df


def drop_duplicates_and_empty(dataframe, to_check_columns):
    dataframe = dataframe.drop_duplicates(to_check_columns).reset_index(drop=True)
    dataframe = dataframe.dropna(subset=to_check_columns).reset_index(drop=True)

    return dataframe


def text_cleaning(sentence):
    import re
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)
    sentence = sentence.lstrip().rstrip()
    return sentence


def sentence_tokenize(sentence):
    from nltk.tokenize import RegexpTokenizer
    
    tokenizer = RegexpTokenizer(r'\w+')
    word_list = tokenizer.tokenize(sentence)
    
    return word_list


def words_lemmatize(words):
    import nltk
    from collections import OrderedDict
    
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    lemma_list = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, 'v')
        if lemma == word:
            lemma = lemmatizer.lemmatize(word, 'n')
        lemma_list.append(lemma)

    lemma_list = list(OrderedDict.fromkeys(lemma_list))
    return lemma_list


def words_detokenize(word_list):
    from nltk.tokenize.treebank import TreebankWordDetokenizer
    
    detokenizer = TreebankWordDetokenizer()
    sentence = detokenizer.detokenize(word_list)
    
    return sentence


def description_preprocess(sentence):
    sentence = sentence.lower()
    tokenized = sentence_tokenize(sentence)
    lemmed = words_lemmatize(tokenized)
    re_sentence = words_detokenize(lemmed)
    
    return re_sentence


def rule_preprocess(sentence):
    import re
    
    sentence = sentence.lower()
    lists = re.findall('\([^()]*\)', sentence)
    cleaned_words = []
    for item in lists:
        tokenized = sentence_tokenize(item)
        lemmed = words_lemmatize(tokenized)
        re_sentence = words_detokenize(lemmed)
        cleaned_words.append(re_sentence)
    sentence = '.*'.join(cleaned_words)
    
    return sentence


def rule_searching(rule_table, dataframe):
    classes = rule_table['Class'].unique()
    all_queried_df = pd.DataFrame()
    for cate in classes:
        to_queried_df = dataframe.copy()
        queried_df = pd.DataFrame()

        rules = rule_table[rule_table['Class'] == cate].copy()
        actions = rules['Action'].unique()

        if 'Remove' in actions:
            # Search the remove rules firstly 
            to_remove = rules[rules['Action'] == 'Remove'].copy()
            for rule in to_remove.search_rule:
                to_queried_df = to_queried_df[~to_queried_df['clean_des'].str.contains(rule, regex=True)].copy()

            can_insert = rules[rules['Action'] == 'Insert'].copy()
            for rule in can_insert.search_rule:
                queried = to_queried_df[to_queried_df['clean_des'].str.contains(rule, regex=True)].copy()
                queried['Class'] = cate
                queried_df = pd.concat([queried_df, queried])

            queried_df = queried_df.drop_duplicates().reset_index(drop=True)
            all_queried_df = pd.concat([all_queried_df, queried_df])

        else:
            can_insert = rules[rules['Action'] == 'Insert'].copy()
            for rule in can_insert.search_rule:
                queried = to_queried_df[to_queried_df['clean_des'].str.contains(rule, regex=True)].copy()
                queried['Class'] = cate
                queried_df = pd.concat([queried_df, queried])

            queried_df = queried_df.drop_duplicates().reset_index(drop=True)
            all_queried_df = pd.concat([all_queried_df, queried_df])

    all_queried_df = all_queried_df.reset_index(drop=True)
    all_queried_df = all_queried_df.drop(columns=['clean_des'])
    
    return all_queried_df


def df2json(dataframe, sheet):
    df_dict = dataframe.to_dict('records')
    df_json = pd.DataFrame({'model': 'text.%s' %sheet, 'fields': df_dict}).to_dict('records')
    
    return df_json