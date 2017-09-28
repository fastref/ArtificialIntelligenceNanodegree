import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        bic = {}
        hmm_models = {}
        for i in range(self.min_n_components, self.max_n_components + 1):
            try:
                hmm_model = self.base_model(i)
                # Log-likelihood
                logL = hmm_model.score(self.X, self.lengths)
                # log number of observations
                logN = np.log(self.X.shape[0])
                # parameters: got it from https://rdrr.io/cran/HMMpa/man/AIC_HMM.html
                p = i * i + self.X.shape[1] * i - 1
                # calculate bic
                bic[i] = -2 * logL + i * logN
                # save model for saving model fitting in the return statement
                hmm_models[i] = hmm_model
            except Exception as error:
                continue

        if len(bic) > 0:
            best_index = min(bic, key=bic.get)
        else:
            best_index = None

        if best_index is None:
            return self.base_model(self.n_constant)
        else:
            return hmm_models[best_index]


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        dic = {}
        dicModels = {}
        for i in range(self.min_n_components, self.max_n_components + 1):
            # first we have to fit hmm for each word
            wordsModels = {}
            wordLogL = {}
            for word in self.words.keys():
                # data and length is saved in words and hwords
                X, Xlength = self.hwords[word]
                try:
                    # fit the model
                    hmm_model = GaussianHMM(n_components    = i,
                                            covariance_type = "diag",
                                            n_iter          = 1000,
                                            random_state    = self.random_state,
                                            verbose         = False).fit(X, Xlength)
                    # save model for later calculations
                    wordLogL[word] = hmm_model.score(X, Xlength)
                    wordsModels[word] = hmm_model
                except Exception as error:
                    continue

            if self.this_word not in wordLogL:
                continue

            # calculate 1/(M-1)SUM(log(P(X(all but i))
            meanLogP = np.mean([wordLogL[word] for word in wordLogL.keys() if word != self.this_word])
            # calculate log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i)) and save it
            dic[i] = wordLogL[self.this_word] - meanLogP
            # save model
            dicModels[i] = wordsModels[self.this_word]



        if len(dic) > 0:
            best_index = max(dic, key=dic.get)
        else:
            best_index = None

        if best_index is None:
            return self.base_model(self.n_constant)
        else:
            return dicModels[best_index]


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        # number of CV splits
        nSplits = 3
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        cvScore = {}
        for i in range(self.min_n_components, self.max_n_components + 1):
            # catch cases where no split is possible
            if (len(self.sequences) < nSplits):
                break
            # split into training and test set
            cvSplit = KFold(random_state=self.random_state, n_splits=nSplits)
            testScore = []
            for trainId, testId in cvSplit.split(self.sequences):
                # create train and test sets
                XTrain, trainLength = combine_sequences(trainId, self.sequences)
                XTest, testLength = combine_sequences(testId, self.sequences)
                # catch cases where the model do not fit
                try:
                    # fit the model
                    hmm_model = GaussianHMM(n_components    = i,
                                            covariance_type = "diag",
                                            n_iter          = 1000,
                                            random_state    = self.random_state,
                                            verbose         = False).fit(XTrain, trainLength)
                    # score the model on test set and save it
                    score = hmm_model.score(XTest, testLength)
                    if score is not None:
                        testScore.append()
                except Exception as error:
                    continue
            # calculate the average score accross test sets
            if len(testScore) > 0:
                cvScore[i] = np.mean(testScore)

        # find best score; model needs to be reestimated as upwards it was not trained on the full data
        if len(cvScore) > 0:
            best_index = max(cvScore, key=cvScore.get)
        else:
            best_index = None

        if best_index is None:
            return self.base_model(self.n_constant)
        else:
            return self.base_model(best_index)
