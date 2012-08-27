from nltkAnalyzer import TxtRequirementProcessor, HtmlRequirementProcessor
from stopwords import STOPWORDS

def txt_analyzer(txt_file, number_of_cat):
    trp = TxtRequirementProcessor(txt_file, number_of_cat)
    corpus_root, fileid = trp.split_path(txt_file)
    raw_text = trp.search_fileid(corpus_root, fileid)
    text_no_punct_list, \
    stopwords_list = trp.list_raw_txt_file(raw_text, 
                                           STOPWORDS)
    text_alpha_no_punct_stopword_list = \
        trp.split_stopwords(text_no_punct_list, 
                            stopwords_list)
    lemmatized_list_by_verb_noun_adj_adv = \
        trp.lemmatize_text_as_list(text_alpha_no_punct_stopword_list)
    categories_directory, \
    boolean_for_directory_test, \
    tmp_root, tmp_folderid = trp.create_temp_directory
    wordtype_categories = \
        trp.list_wordtypes_from_lemmatized_list(lemmatized_list_by_verb_noun_adj_adv, 
                                                number_of_cat)
    category_tmp_file_list, \
    boolean_for_file_test = \
        trp.create_temp_files_named_by_wordtypes(wordtype_categories, 
                                                 categories_directory)
    category_tmp_file_content, \
    boolean_for_content_test = \
        trp.assign_temp_files_txt_content(wordtype_categories, 
                                          lemmatized_list_by_verb_noun_adj_adv)
    category_tmp_file_list, \
    boolean_for_check_content_file_test = \
        trp.assign_temp_content_to_temp_files(category_tmp_file_content, 
                                              category_tmp_file_list)
    reader, \
    boolean_for_categories_test = trp.create_categorized_corpus(categories_directory)
    trp.tabulate_categorized_words(reader, number_of_cat)
    trp.plot_txt_results(lemmatized_list_by_verb_noun_adj_adv, 
                         number_of_cat)
    boolean_for_file_test = trp.delete_temporary_files(category_tmp_file_list)
    boolean_for_directory_test = trp.remove_categories_directory(categories_directory, 
                                                                 tmp_root, 
                                                                 tmp_folderid)
    
def html_analyzer(html_file, number_of_cat):
    hrp = HtmlRequirementProcessor(html_file, number_of_cat)
    raw_text_and_space = hrp.open_html_file(html_file)
    raw_text_free_from_html_entity = hrp.split_html_entities(raw_text_and_space)
    text_no_punct_list, \
    stopwords_list = hrp.list_raw_html_file(raw_text_free_from_html_entity, 
                                            STOPWORDS)
    text_alpha_no_punct_stopword_list = hrp.split_stopwords(text_no_punct_list, 
                                                            stopwords_list)
    lemmatized_list_by_verb_noun_adj_adv = \
        hrp.lemmatize_text_as_list(text_alpha_no_punct_stopword_list)
    categories_directory, \
    boolean_for_directory_test, \
    tmp_root, tmp_folderid = hrp.create_temp_directory
    wordtype_categories = \
        hrp.list_wordtypes_from_html_list(lemmatized_list_by_verb_noun_adj_adv, 
                                          number_of_cat)
    category_tmp_file_list, \
    boolean_for_file_test = \
        hrp.create_temp_files_named_by_wordtypes(wordtype_categories, 
                                                 categories_directory)
    category_tmp_file_content, \
    boolean_for_content_test = \
        hrp.assign_temp_files_html_content(wordtype_categories, 
                                           lemmatized_list_by_verb_noun_adj_adv)
    category_tmp_file_list, \
    boolean_for_check_content_file_test = \
        hrp.assign_temp_content_to_temp_files(category_tmp_file_content, 
                                              category_tmp_file_list)
    reader, \
    boolean_for_categories_test = hrp.create_categorized_corpus(categories_directory)
    hrp.tabulate_categorized_words(reader, number_of_cat)
    hrp.plot_html_results(lemmatized_list_by_verb_noun_adj_adv, number_of_cat)
    boolean_for_file_test = hrp.delete_temporary_files(category_tmp_file_list)
    boolean_for_categories_test = hrp.remove_categories_directory(categories_directory, 
                                                                  tmp_root, 
                                                                  tmp_folderid)
    
    
