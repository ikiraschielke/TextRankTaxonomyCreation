# Textrank implementation for extracting most relevant keywords of document
# adapted for english language

from collections import OrderedDict
import numpy as np
import spacy
# python -m spacy download en_core_web_sm
from spacy.lang.en.stop_words import STOP_WORDS
import time
import os

nlp = spacy.load('en_core_web_sm')

class TextRank4Keyword():
    """Extract keywords from text"""
    
    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 10 # iteration steps
        self.node_weight = None # save keywords and its weight

    
    def set_stopwords(self, stopwords):  
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
    
    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences
        
    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab
    
    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs
        
    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())
    
    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1
            
        # Get Symmeric matrix
        g = self.symmetrize(g)
        
        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm
        
        return g_norm

    
    def get_keywords(self, number=10):
        """SAVE top number of keyword"""
        keywords = []
        """Print top number keywords"""
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            'save key, value'
            'use int instead of float, as the value will be relevant for the parent array'
            keywords.append((key,int(value)))
            #print(key + ' - ' + str(value))
            keywords.append
            if i > number:
                return keywords

        
        
    def analyze(self, text, 
                candidate_pos=['NOUN', 'PROPN'], 
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""

        stopwords=["#","t","ve"]
        # Set stop words
        self.set_stopwords(stopwords)
        
        # Parse text by spaCy
        doc = nlp(text)
        
        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower) # list of list of words
        
        # Build vocabulary
        vocab = self.get_vocab(sentences)
        
        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)
        
        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)
        
        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))
        
        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]
        
        self.node_weight = node_weight

def GetKeyRanks_GiveMat():
    times = []
    mat = []
    with os.scandir('reviews\product_reviews_1') as files:
        for entry in files:
            t0 = time.time()
            with open(entry, "r", ) as f:
                text = f.read()

                tr4w = TextRank4Keyword()
                """Nouns are easier to comprehend in text summarisation 
                and representation
                hence target Nouns and Proper Nouns
                """
                tr4w.analyze(text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
                kwords = tr4w.get_keywords(5)


                mat.append(kwords)
                t1 = time.time()
                it = t1-t0
                times.append(round(it,5))

    t2 = time.time()
    dt = t2
    times.append(round(dt,5))
    'print statments can be commented or uncommented'
    print("processing time in sec {}".format(times))
    print('Extracted most relevant words in corpus {}'.format(mat))
    return times, mat


"""
Values at index 0 have need a parent one index above that, 
this is represented by the 'root' at an index -1.
print levels of trees
"""

def TreePrint(mat):
    print('                                           root                                                        ')
    for i in range(5):
        print("\n")
        level = [sub[i] for sub in mat]
        print(level)

    

times,mat = GetKeyRanks_GiveMat()
TreePrint(mat)

