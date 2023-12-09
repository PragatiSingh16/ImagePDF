import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def text_summarizer(text, num_sentences=3):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Remove stopwords (common words that don't add much meaning)
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]

    # Calculate word frequency
    word_freq = nltk.FreqDist(words)

    # Assign score to each sentence based on word frequency
    sent_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence not in sent_scores:
                    sent_scores[sentence] = word_freq[word]
                else:
                    sent_scores[sentence] += word_freq[word]

    # Get the top 'num_sentences' sentences with highest scores
    summary_sentences = sorted(sent_scores, key=sent_scores.get, reverse=True)[:num_sentences]

    # Join the summary sentences to create the summary
    summary = ' '.join(summary_sentences)
    return summary

# Example text
text_to_summarize = """ Cake is a flour confection made from flour, sugar, and other ingredients and is usually baked. In their oldest forms, cakes were modifications of bread, but cakes now cover a wide range of preparations that can be simple or elaborate and which share features with desserts such as pastries,meringues, custards, and pies.The most common ingredients include flour, sugar, eggs, fat (such as butter, oil, or margarine), a liquid, and a leavening agent, such as baking soda or baking powder. Common additional ingredients include dried, candied, or fresh fruit, nuts, cocoa, and extracts such as vanilla, with numerous substitutions for the primary ingredients. Cakes can also be filled with fruit preserves, nuts, or dessert sauces (like custard, jelly, cooked fruit, whipped cream, or syrups),[1] iced with buttercream or other icings, and decorated with marzipan, piped borders, or candied fruit.Cake is often served as a celebratory dish on ceremonial occasions, such as weddings, anniversaries, and birthdays. There are countless cake recipes; some are bread-like, some are rich and elaborate, and many are centuries old. Cake making is no longer a complicated procedure; while at one time considerable labor went into cake making (particularly the whisking of egg foams), baking equipment and directions have"""

# Call the function with the text and desired number of sentences in the summary
summary = text_summarizer(text_to_summarize, num_sentences=3)
print("Summary:")
print(summary)
