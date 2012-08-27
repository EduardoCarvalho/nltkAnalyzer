from os.path import split
from urllib import urlopen
from os import listdir, rmdir
from tempfile import mkdtemp, NamedTemporaryFile

from re import split as re_split

from nltk.corpus import PlaintextCorpusReader
from nltk.util import clean_html 
from stopwords import STOPWORDS
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
from nltk.tokenize import regexp_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from BeautifulSoup import BeautifulStoneSoup


class TxtRequirementProcessor(object):

    def __init__(self, txt_file, number_of_cat):
        self.txt_file = txt_file
        self.number_of_cat = number_of_cat 
    
    def split_path(self, txt_file):
        spliter = split(txt_file)
        corpus_root = spliter[0]
        fileid = spliter[1]
        return corpus_root, fileid

    def search_fileid(self, corpus_root, fileid):
        new_corpus_fileids_list = PlaintextCorpusReader(corpus_root, '.*')   
        raw_text = new_corpus_fileids_list.raw(fileids=[fileid])
        return raw_text    

    def list_raw_txt_file(self, raw_text, STOPWORDS):
        text_no_punct_list = regexp_tokenize(raw_text, "[\w']+")
        stopwords_list = regexp_tokenize(STOPWORDS, "[\w']+")
        return text_no_punct_list, stopwords_list
        
    def split_stopwords(self, text_no_punct_list, stopwords_list):
        text_alpha_no_punct_stopword_list = [w.lower() for w in text_no_punct_list 
                               if w.lower() not in stopwords_list and w.isalpha()]
        return text_alpha_no_punct_stopword_list

    def lemmatize_text_as_list(self, text_alpha_no_punct_stopword_list):
        lemmatizer = WordNetLemmatizer()
        lemmatized_list_by_verb = []
        lemmatized_list_by_verb_noun = []
        lemmatized_list_by_verb_noun_adj = []
        lemmatized_list_by_verb_noun_adj_adv = []
        for i in text_alpha_no_punct_stopword_list:
            lemmatized_list_by_verb.append(lemmatizer.lemmatize(i, pos='v'))
        for i in lemmatized_list_by_verb:
            lemmatized_list_by_verb_noun.append(lemmatizer.lemmatize(i, pos='n'))
        for i in lemmatized_list_by_verb_noun:
            lemmatized_list_by_verb_noun_adj.append(lemmatizer.lemmatize(i, pos='a'))
        for i in lemmatized_list_by_verb_noun_adj:
            lemmatized_list_by_verb_noun_adj_adv.append(lemmatizer.lemmatize(i, pos='r'))
        return lemmatized_list_by_verb_noun_adj_adv

    @property
    def create_temp_directory(self):
        categories_directory = mkdtemp()
        spliter = split(categories_directory)
        tmp_root = spliter[0]
        tmp_folderid = spliter[1]
        boolean_for_directory_test = tmp_folderid in listdir(tmp_root)     
        return categories_directory, boolean_for_directory_test, tmp_root, tmp_folderid

    def list_wordtypes_from_lemmatized_list(self, lemmatized_list_by_verb_noun_adj_adv, 
                                                  number_of_cat):
        fdist = FreqDist(lemmatized_list_by_verb_noun_adj_adv) 
        wordtype_categories = fdist.keys()[:number_of_cat]
        return wordtype_categories

    def create_temp_files_named_by_wordtypes(self, wordtype_categories, categories_directory):
        category_tmp_file_list = []
        boolean_list = []
        boolean_for_file_test = ''
        for i in range(len(wordtype_categories)):
            category_tmp_file_list.append(NamedTemporaryFile(suffix='wordtype_'+wordtype_categories[i], 
                                                             prefix='.txt', dir=categories_directory)) 
        for i in range(len(category_tmp_file_list)):
            boolean_list.append(category_tmp_file_list[i].closed)
        if False in boolean_list:
            boolean_for_file_test = False
        else:
            boolean_for_file_test = True     
        return category_tmp_file_list, boolean_for_file_test

    def assign_temp_files_txt_content(self, wordtype_categories, 
                                            lemmatized_list_by_verb_noun_adj_adv):
        category_tmp_file_content = []
        boolean_for_content_test = ''
        for i in range(len(wordtype_categories)):
            category_tmp_file_content.append([w for w in lemmatized_list_by_verb_noun_adj_adv 
                                                if w==wordtype_categories[i]])
        boolean_for_content_test = len(wordtype_categories) == len(category_tmp_file_content)
        return category_tmp_file_content, boolean_for_content_test

    def assign_temp_content_to_temp_files(self, category_tmp_file_content, 
                                                category_tmp_file_list):
        boolean_list = []
        boolean_for_check_content_file_test = ''
        for i in range(len(category_tmp_file_content)):
            category_tmp_file_list[i].writelines('\n'.join(category_tmp_file_content[i]))
        for i in range(len(category_tmp_file_list)):
            category_tmp_file_list[i].seek(0)
        for i in range(len(category_tmp_file_list)):
            boolean_list.append(category_tmp_file_list[i].read()!='')
        if False in boolean_list:
            boolean_for_check_content_file_test = False
        else:
            boolean_for_check_content_file_test = True
        for i in range(len(category_tmp_file_list)):
            category_tmp_file_list[i].seek(0)
        return category_tmp_file_list, boolean_for_check_content_file_test

    def create_categorized_corpus(self, categories_directory):
        boolean_list = []
        boolean_for_categories_test = ''
        reader = CategorizedPlaintextCorpusReader(categories_directory, 
                                                  r'\.txt.*wordtype_(\w+)', 
                                                  cat_pattern=r'\.txt.*wordtype_(\w+)')
        for category in reader.categories():
            boolean_list.append(category != '') 
        if False in boolean_list:
            boolean_for_categories_test = False
        else:
            boolean_for_categories_test = True
        return reader, boolean_for_categories_test
    
    def tabulate_categorized_words(self, reader, number_of_cat):
        wordtypes = reader.words()
        print '\n%s %5s %7s %14s\n' %('rank', 'fi', 'Fi*', 'wordtype')
        fd = FreqDist(wordtypes)
        cumulative = 0.0
        rank = 0
        for word in fd.keys()[:number_of_cat]:
            rank += 1
            cumulative += fd[word] * 100.0 / fd.N()
            print "%4d %6d %4d%% %15s" %(rank, fd[word], cumulative, word)         
        
    def plot_txt_results(self, lemmatized_list_by_verb_noun_adj_adv, 
                               number_of_cat):
        fdist = FreqDist(w for w in lemmatized_list_by_verb_noun_adj_adv)
        fdist.plot(number_of_cat)

    def delete_temporary_files(self, category_tmp_file_list):
        boolean_list = []
        boolean_for_file_test = ''
        for i in range(len(category_tmp_file_list)):
            category_tmp_file_list[i].close()
        for i in range(len(category_tmp_file_list)):
            boolean_list.append(category_tmp_file_list[i].closed)
        if False in boolean_list:
            boolean_for_file_test = False
        else:
            boolean_for_file_test = True
        return boolean_for_file_test
        
    def remove_categories_directory(self, categories_directory, 
                                          tmp_root, 
                                          tmp_folderid):
        rmdir(categories_directory)
        boolean_for_categories_test = tmp_folderid not in listdir(tmp_root)
        return boolean_for_categories_test


class HtmlRequirementProcessor(object):

    def __init__(self, html_file, number_of_cat):
        self.html_file = html_file
        self.number_of_cat = number_of_cat
        
    def open_html_file(self, html_file):
        html_and_text = urlopen(html_file).read()
        raw_text_and_space = clean_html(html_and_text)
        return raw_text_and_space
        
    def split_html_entities(self, raw_text_and_space):
        raw_text_free_from_html_entity = unicode(BeautifulStoneSoup(raw_text_and_space, 
                                                                    convertEntities='html'))
        return raw_text_free_from_html_entity
        
    def list_raw_html_file(self, raw_text_free_from_html_entity, STOPWORDS):
        text_no_punct_list = regexp_tokenize(raw_text_free_from_html_entity, "[\w']+")
        stopwords_list = regexp_tokenize(STOPWORDS, "[\w']+")
        return text_no_punct_list, stopwords_list
        
    def split_stopwords(self, text_no_punct_list, stopwords_list):
        text_alpha_no_punct_stopword_list = [w.lower() for w in text_no_punct_list 
                               if w.lower() not in stopwords_list and w.isalpha()]
        return text_alpha_no_punct_stopword_list
        
    def lemmatize_text_as_list(self, text_alpha_no_punct_stopword_list):
        lemmatizer = WordNetLemmatizer()
        lemmatized_list_by_verb = []
        lemmatized_list_by_verb_noun = []
        lemmatized_list_by_verb_noun_adj = []
        lemmatized_list_by_verb_noun_adj_adv = []
        for i in text_alpha_no_punct_stopword_list:
            lemmatized_list_by_verb.append(lemmatizer.lemmatize(i, pos='v'))
        for i in lemmatized_list_by_verb:
            lemmatized_list_by_verb_noun.append(lemmatizer.lemmatize(i, pos='n'))
        for i in lemmatized_list_by_verb_noun:
            lemmatized_list_by_verb_noun_adj.append(lemmatizer.lemmatize(i, pos='a'))
        for i in lemmatized_list_by_verb_noun_adj:
            lemmatized_list_by_verb_noun_adj_adv.append(lemmatizer.lemmatize(i, pos='r'))
        return lemmatized_list_by_verb_noun_adj_adv
        
    @property
    def create_temp_directory(self):
        categories_directory = mkdtemp()
        spliter = split(categories_directory)
        tmp_root = spliter[0]
        tmp_folderid = spliter[1]
        boolean_for_directory_test = tmp_folderid in listdir(tmp_root)     
        return categories_directory, boolean_for_directory_test, tmp_root, tmp_folderid
        
    def list_wordtypes_from_html_list(self, lemmatized_list_by_verb_noun_adj_adv, number_of_cat):
        fdist = FreqDist(lemmatized_list_by_verb_noun_adj_adv) 
        wordtype_categories = fdist.keys()[:number_of_cat]
        return wordtype_categories
        
    def create_temp_files_named_by_wordtypes(self, wordtype_categories, categories_directory):
        category_tmp_file_list = []
        boolean_list = []
        boolean_for_file_test = ''
        for i in range(len(wordtype_categories)):
            category_tmp_file_list.append(NamedTemporaryFile(suffix='wordtype_'+wordtype_categories[i], 
                                                             prefix='.txt', 
                                                             dir=categories_directory)) 
        for i in range(len(category_tmp_file_list)):
            boolean_list.append(category_tmp_file_list[i].closed)
        if False in boolean_list:
            boolean_for_file_test = False
        else:
            boolean_for_file_test = True     
        return category_tmp_file_list, boolean_for_file_test
        
    def assign_temp_files_html_content(self, wordtype_categories, 
                                             lemmatized_list_by_verb_noun_adj_adv):
        category_tmp_file_content = []
        boolean_for_content_test = ''
        for i in range(len(wordtype_categories)):
            category_tmp_file_content.append([w for w in lemmatized_list_by_verb_noun_adj_adv 
                                                if w==wordtype_categories[i]])
        boolean_for_content_test = len(wordtype_categories) == len(category_tmp_file_content)
        return category_tmp_file_content, boolean_for_content_test
        
    def assign_temp_content_to_temp_files(self, category_tmp_file_content, 
                                                category_tmp_file_list):
        boolean_list = []
        boolean_for_check_content_file_test = ''
        for i in range(len(category_tmp_file_content)):
            category_tmp_file_list[i].writelines('\n'.join(category_tmp_file_content[i]))
        for i in range(len(category_tmp_file_list)):
            category_tmp_file_list[i].seek(0)
        for i in range(len(category_tmp_file_list)):
            boolean_list.append(category_tmp_file_list[i].read()!='')
        if False in boolean_list:
            boolean_for_check_content_file_test = False
        else:
            boolean_for_check_content_file_test = True
        for i in range(len(category_tmp_file_list)):
            category_tmp_file_list[i].seek(0)
        return category_tmp_file_list, boolean_for_check_content_file_test

    def create_categorized_corpus(self, categories_directory):
        boolean_list = []
        boolean_for_categories_test = ''
        reader = CategorizedPlaintextCorpusReader(categories_directory, 
                                                  r'\.txt.*wordtype_(\w+)', 
                                                  cat_pattern=r'\.txt.*wordtype_(\w+)')
        for category in reader.categories():
            boolean_list.append(category != '') 
        if False in boolean_list:
            boolean_for_categories_test = False
        else:
            boolean_for_categories_test = True
        return reader, boolean_for_categories_test
    
    def tabulate_categorized_words(self, reader, number_of_cat):
        wordtypes = reader.words()
        print '\n%s %5s %7s %14s\n' %('rank', 'fi', 'Fi*', 'wordtype')
        fd = FreqDist(wordtypes)
        cumulative = 0.0
        rank = 0
        for word in fd.keys()[:number_of_cat]:
            rank += 1
            cumulative += fd[word] * 100.0 / fd.N()
            print "%4d %6d %4d%% %15s" %(rank, fd[word], cumulative, word)
            
    def plot_html_results(self, lemmatized_list_by_verb_noun_adj_adv, number_of_cat):
        fdist = FreqDist(w for w in lemmatized_list_by_verb_noun_adj_adv)
        fdist.plot(number_of_cat)
        
    def delete_temporary_files(self, category_tmp_file_list):
        boolean_list = []
        boolean_for_file_test = ''
        for i in range(len(category_tmp_file_list)):
            category_tmp_file_list[i].close()
        for i in range(len(category_tmp_file_list)):
            boolean_list.append(category_tmp_file_list[i].closed)
        if False in boolean_list:
            boolean_for_file_test = False
        else:
            boolean_for_file_test = True
        return boolean_for_file_test
        
    def remove_categories_directory(self, categories_directory, 
                                          tmp_root, 
                                          tmp_folderid):
        rmdir(categories_directory)
        boolean_for_categories_test = tmp_folderid not in listdir(tmp_root)
        return boolean_for_categories_test            
            
