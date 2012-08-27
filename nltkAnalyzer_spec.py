from unittest import TestCase
from should_dsl import should

from nltkAnalyzer import TxtRequirementProcessor, HtmlRequirementProcessor
from specvar import Variables


class TestTxtRequirementProcessor(TestCase):

    def setUp(self):
        self.v = Variables()
        self.trp = TxtRequirementProcessor(self.v.path, self.v.n_cat)
    
    def it_receives_a_path(self):
        self.trp.txt_file |should| equal_to(self.v.path)
        
    def it_splits_corpus_root_and_fileid_from_path(self):
        self.trp.split_path(self.v.path) |should| equal_to((self.v.root, self.v.fileid))
        
    def it_searches_fileid_in_a_folder_and_returns_its_string_content(self):
        self.trp.search_fileid(self.v.corpus_root, self.v.spec_fileid) \
        |should| equal_to(self.v.concise_raw_text)

    def it_lists_raw_text_and_stopwords_in_a_tuple(self):
        self.trp.list_raw_txt_file(self.v.concise_raw_text, self.v.concise_stopwords) \
        |should| equal_to((self.v.concise_text_list, self.v.concise_stopwords_list))

    def it_splits_stopwords_and_numbers_from_text_as_a_list(self):
        self.trp.split_stopwords(self.v.concise_text_list, self.v.concise_stopwords_list) \
        |should| equal_to(self.v.text_list_free_from_stopwords)

    def it_lists_lemmatized_verb_noun_and_adjective(self):
        self.trp.lemmatize_text_as_list(self.v.text_list_free_from_stopwords) \
        |should| equal_to(self.v.lemmatized_list)

    def it_creates_temporary_directory(self):
        self.trp.create_temp_directory[1] |should| equal_to(True)

    def it_creates_wordtypes_from_lemmatized_list_of_words(self):
        self.trp.list_wordtypes_from_lemmatized_list(self.v.lemmatized_list, self.v.n_cat) \
        |should| equal_to(self.v.wordtypes_list)
    
    def it_creates_temporary_files_named_by_wordtypes_inside_temporary_directory(self):
        self.trp.create_temp_files_named_by_wordtypes(self.v.wordtypes_list, self.v.temporary_directory)[1] \
        |should| equal_to(False) 

    def it_assigns_temporary_file_content_by_wordtype_to_a_list(self):
        self.trp.assign_temp_files_txt_content(self.v.wordtypes_list, self.v.lemmatized_list)[1] \
        |should| equal_to(True)

    def it_assigns_temporary_content_to_temporary_files(self):
        obj = self.trp.create_temp_files_named_by_wordtypes(self.v.wordtypes_list, self.v.temporary_directory)[0]
        self.trp.assign_temp_content_to_temp_files(self.v.categories_content, obj)[1] \
        |should| equal_to(True)

    def it_creates_categorized_plaintextcorpusreader(self):
        self.trp.create_categorized_corpus(self.trp.create_temp_directory[0])[1] \
        |should| equal_to(True)     

    def it_deletes_all_wordtypes_temporary_files(self):
        obj = self.trp.create_temp_files_named_by_wordtypes(self.v.wordtypes_list, self.v.temporary_directory)[0]
        self.trp.delete_temporary_files(obj) |should| equal_to(True)
    
    def it_checks_temporary_directory_was_removed_from_tmp_folder(self):
        categories_directory = self.trp.create_temp_directory[0]
        tmp_folderid = self.trp.create_temp_directory[3]
        self.trp.remove_categories_directory(categories_directory, self.v.temporary_directory, tmp_folderid) \
        |should| equal_to(False) # True
        
class TestHtmlRequirementProcessor(TestCase):

    def setUp(self):
        self.v = Variables()
        self.hrp = HtmlRequirementProcessor(self.v.url, self.v.n_cat)
    
    def it_receives_a_url(self):
        self.hrp.html_file |should| equal_to(self.v.url)
        
    def it_opens_and_cleans_html_file(self):
        self.hrp.open_html_file(self.v.url) |should| equal_to(self.v.raw_text_and_space_spec)
        
    def it_splits_html_character_entities(self):
        self.hrp.split_html_entities(self.v.raw_text_and_space_spec) \
        |should| equal_to(self.v.raw_text_free_from_html_entity_spec)
        
    def it_lists_raw_html_file(self):
        self.hrp.list_raw_html_file(self.v.raw_text_free_from_html_entity_spec, self.v.concise_stopwords) \
        |should| equal_to((self.v.text_no_punct_list_spec, self.v.concise_stopwords_list))
   
    def it_splits_stopwords_from_html(self):
        self.hrp.split_stopwords(self.v.text_no_punct_list_spec, self.v.concise_stopwords_list) \
        |should| equal_to(self.v.text_alpha_no_punct_stopword_list_spec)
        
    def it_lists_lemmatized_verb_noun_and_adjective(self):
        self.hrp.lemmatize_text_as_list(self.v.text_alpha_no_punct_stopword_list_spec) \
        |should| equal_to(self.v.lemmatized_html_list)
        
    def it_creates_temporary_directory(self):
        self.hrp.create_temp_directory[1] |should| equal_to(True)
        
    def it_creates_wordtypes_from_html_lemmatized_list_of_words(self):
        self.hrp.list_wordtypes_from_html_list(self.v.lemmatized_html_list, self.v.n_cat) \
        |should| equal_to(self.v.wordtypes_html_list) 
        
    def it_creates_temporary_files_named_by_wordtypes_inside_temporary_directory(self):
        self.hrp.create_temp_files_named_by_wordtypes(self.v.wordtypes_html_list, self.v.temporary_directory)[1] \
        |should| equal_to(False) 
    
    def it_assigns_temporary_file_content_by_wordtype_to_a_list(self):
        self.hrp.assign_temp_files_html_content(self.v.wordtypes_html_list, self.v.lemmatized_html_list)[1] \
        |should| equal_to(True)
        
    def it_assigns_temporary_content_to_temporary_files(self):
        obj = self.hrp.create_temp_files_named_by_wordtypes(self.v.wordtypes_html_list, self.v.temporary_directory)[0]
        self.hrp.assign_temp_content_to_temp_files(self.v.categories_html_content, obj)[1] \
        |should| equal_to(True)
        
    def it_creates_categorized_plaintextcorpusreader(self):
        self.hrp.create_categorized_corpus(self.hrp.create_temp_directory[0])[1] \
        |should| equal_to(True)
        
    def it_deletes_all_wordtypes_temporary_files(self):
        obj = self.hrp.create_temp_files_named_by_wordtypes(self.v.wordtypes_html_list, self.v.temporary_directory)[0]
        self.hrp.delete_temporary_files(obj) |should| equal_to(True)
    
    def it_checks_temporary_directory_was_removed_from_tmp_folder(self):
        categories_directory = self.hrp.create_temp_directory[0]
        tmp_folderid = self.hrp.create_temp_directory[3]
        self.hrp.remove_categories_directory(categories_directory, self.v.temporary_directory, tmp_folderid) \
        |should| equal_to(False) # True
        
    
    
    
        
    
        
    
    
