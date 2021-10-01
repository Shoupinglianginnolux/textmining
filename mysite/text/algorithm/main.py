import fire
from .data_preprocess import *

def main(rule_json, json_1, json_2=None):
    # Preprocess for rules
    _, rule_table = json2df(rule_json)
    rule_table['search_rule'] = rule_table['Rule'].apply(rule_preprocess)
    rule_table = rule_table.drop_duplicates('search_rule').reset_index(drop=True)
    
    sheet, df = json2df(json_1)
    if sheet == 'srqs':
        df = drop_duplicates_and_empty(df, ['SRNumber', 'InternalNotes'])
        df['clean_des'] = df['InternalNotes'].apply(text_cleaning)
    elif sheet == 'cases':
        df = drop_duplicates_and_empty(df, ['CaseNumber', 'Description'])
        df['clean_des'] = df['Description'].apply(text_cleaning)

    search_result = rule_searching(rule_table, df)
    
    if not json_2:
        return df2json(search_result, sheet)
    
    if json_2:
        sheet_2, df_2 = json2df(json_2)
        if sheet_2 == 'srqs':
            df_2 = drop_duplicates_and_empty(df_2, ['SRNumber', 'InternalNotes'])
            df_2['clean_des'] = df_2['InternalNotes'].apply(text_cleaning)
        elif sheet_2 == 'cases':
            df_2 = drop_duplicates_and_empty(df_2, ['CaseNumber', 'Description'])
            df_2['clean_des'] = df_2['Description'].apply(text_cleaning)

        search_result_2 = rule_searching(rule_table, df_2)
        
        return df2json(search_result, sheet), df2json(search_result_2, sheet_2)


if __name__ == '__main__':
    fire.Fire(main)
