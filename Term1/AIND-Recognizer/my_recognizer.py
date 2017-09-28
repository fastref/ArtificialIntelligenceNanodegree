import warnings
from asl_data import SinglesData

def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    for i in range(test_set.num_items):
        X, Xlength = test_set.get_item_Xlengths(item=i)
        wordLogValues = {}
        # calculate for each word the log-likelihood
        for word, model in models.items():
            try:
                wordLogValues[word] = model.score(X, Xlength)
            except Exception as error:
                wordLogValues[word] = float("-inf")

        # add word probabilities to the output list
        probabilities.append(wordLogValues)

        # extract best fit
        best_word = max(wordLogValues, key=wordLogValues.get)
        guesses.append(best_word)
    return probabilities, guesses
