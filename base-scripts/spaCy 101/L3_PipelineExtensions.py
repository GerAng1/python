# https://course.spacy.io/en/chapter3
from spacy.tokens import Span
import spacy

# This allows to create custom pipeline components
# Create the nlp object
nlp = spacy.load("en_core_web_sm")

# Define a custom component


@Language.component("custom_component")
def custom_component_function(doc):
    # Print the doc's length
    print("Doc length:", len(doc))
    # Return the doc object
    return doc


# Add the component first in the pipeline
nlp.add_pipe("custom_component", first=True)

# Process a text
doc = nlp("Hello world!")


# Add custom attributes to the Doc, Token and Span objects to store custom data

# Example 2:
# Use Span.set_extension to register "to_html" (method to_html).
# Call it on doc[0:2] with the tag "strong".

nlp = spacy.blank("en")


# Define the method
def to_html(span, tag):
    # Wrap the span text in a HTML tag and return it
    return f"<{tag}>{span.text}</{tag}>"


# Register the Span method extension "to_html" with the method to_html
Span.set_extension("to_html", method=to_html)

# Process the text and call the to_html method on the span
# with the tag name "strong"
doc = nlp("Hello world, this is a sentence.")
span = doc[0:2]
print(span._.to_html("strong"))


# Example 3:
# Complete the get_wikipedia_url getter so it only returns the URL
# if the span’s label is in the list of labels.
# Set the Span extension "wikipedia_url" using the getter get_wikipedia_url.

# Iterate over the entities in the doc and output their Wikipedia URL.

nlp = spacy.load("en_core_web_sm")


def get_wikipedia_url(span):
    # Get a Wikipedia URL if the span has one of the labels
    if span.label_ in ("PERSON", "ORG", "GPE", "LOCATION"):
        entity_text = span.text.replace(" ", "_")
        return "https://en.wikipedia.org/w/index.php?search=" + entity_text


# Set the Span extension wikipedia_url using the getter get_wikipedia_url
Span.set_extension("wikipedia_url", getter=get_wikipedia_url)

doc = nlp(
    "In over fifty years from his very first recordings right through to his "
    "last album, David Bowie was at the vanguard of contemporary culture."
)
for ent in doc.ents:
    # Print the text and Wikipedia URL of the entity
    print(ent.text, ent._.wikipedia_url)
