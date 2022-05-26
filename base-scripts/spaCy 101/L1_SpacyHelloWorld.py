import spacy  # main library
from tabulate import tabulate

# creating nlp pipeline (blank)
# includes language-specific rules used
# for tokenizing the text into words and punctuation
nlp = spacy.blank("en")


# creating trained nlp pipeline
# you can predict linguistic attributes in context
# have Part-of-speech tags (pos)
# Syntactic dependencies
# Named entities
# Can be updated with more examples to fine-tune predictions
tr_nlp = spacy.load("en_core_web_trf")

# DOCS
# object to access information about the text
text = "My name is Gerardo and I'm learning spaCy in ten days! whddk"
doc = nlp(text)
doc2 = tr_nlp(text)

# some attributes in "docs"
doc.ents  # named entities (returns list of "spans")


# TOKENS
# doc in mainly divided in "tokens"
a_token = doc[2]

# some token attributes
for doc in [doc, doc2]:
    print("Blank Pipeline")
    token_atts = [
        [".text",  # "World" (original word text)
         ".i",  # 1 (index)
         ".is_alpha",  # True (alphanumeric)
         ".is_punct",  # False (punctuation)
         ".like_num",  # False (if token is number or text of number)
         ".shape_",  # (capitalization, punctuation, digits)
         ".is_stop",  # (part of most common words of the language list?)
         ".has_vector",  # (have a vector representation)
         ".is_oov"]]  # (out of vocabulary)

    for token in doc:
        temp_list = [
            token.text,
            token.i,
            token.is_alpha,
            token.is_punct,
            token.like_num,
            token.shape_,
            token.is_stop,
            token.has_vector,
            token.is_oov]

        token_atts.append(temp_list)

    print(tabulate(token_atts, headers="firstrow", tablefmt="github"))
    print('\n Trained Pipeline Dependent Attributes:')

    token_atts = [
        [".lemma_",  # (base form of the word)
         ".pos_",  # Noun (predicted Part of Speech)
         ".dep_",  # (predicted relation between tokens)
         ".head.text",  # (predicted parent token word is attached to)
         ".tag_"]]  # (detailed part-of-speech tag)

    for token in doc:
        temp_list = [
            token.lemma_,
            token.pos_,
            token.dep_,
            token.head.text,
            token.tag_]

        token_atts.append(temp_list)

    print(tabulate(token_atts, headers="firstrow", tablefmt="github"))
    print('\n')

# SPANS
# slice of doc is span
span = doc[5:8]

# some attributes of span
print(span.text)  # "I'm learning spaCy"
print(span.label_)  # (label) (works with entities)


# HELPFULL TOOLS
# spacy.explain("something")  # to understand attribute outputs
