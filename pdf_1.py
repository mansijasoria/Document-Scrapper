import fitz  # PyMuPDF
import re
from typing import List, Tuple, Optional

def extract_complete_article_details(pdf_path: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], List[Tuple[str, int]], Optional[str]]:
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Variables to hold extracted data
    journal_name = None
    publication_date = None
    indexing_agency = None
    article_type = None
    authors = []
    corresponding_author = None

    # Regular expressions for data extraction
    journal_name_pattern = re.compile(r"Journal of [\w\s]+")
    publication_date_pattern = re.compile(r"\b(20\d{2}|\d{2}/\d{2}/\d{2,4}|\d{2}/\d{2,4})\b")
    indexing_agency_pattern = re.compile(r"Indexing Agency: ([\w\s,]+)")
    article_type_patterns = {
        "Original Research": re.compile(r"Original"),
        "Review Article": re.compile(r"Review"),
        "Case Report": re.compile(r"Case"),
        "Case Studies": re.compile(r"Case"),
        "Letter to the Editor": re.compile(r"Letter to the Editor"),
        "Blog": re.compile(r"Blog"),
        "Webpage": re.compile(r"Webpage"),
        "Systematic Review": re.compile(r"Systematic"),
        "Meta-analysis": re.compile(r"Meta-analysis")
    }

    author_pattern = re.compile(r"([A-Za-z\s]+)(\d+|[a-z]+)(?![\w])")
    corresponding_author_pattern = re.compile(r"(?:Corresponding Author|Correspondence to):? ([\w\s,]+)")

    # Concatenate all pages' text
    full_text = "\n".join([page.get_text() for page in doc])

    # Extract Journal Name
    journal_match = journal_name_pattern.search(full_text)
    if journal_match:
        journal_name = journal_match.group().strip()

    # Extract Publication Date
    publication_date_match = publication_date_pattern.search(full_text)
    if publication_date_match:
        publication_date = publication_date_match.group()

    # Extract Indexing Agency
    indexing_agency_match = indexing_agency_pattern.search(full_text)
    if indexing_agency_match:
        indexing_agency = indexing_agency_match.group(1).strip()

    # Extract Type of Article
    for article_type_key, pattern in article_type_patterns.items():
        if pattern.search(full_text):
            article_type = article_type_key
            break

    # Initialize an empty dictionary to store authors with their positions
    author_order_dict = {}

    # Extract Authors and their order from the superscript numbers or letters
    for page in doc:
        text_instances = page.search_for(r"\d|[a-z]")
        for inst in text_instances:
            # Extract the text block that includes the author name and superscript order
            block = page.get_text("dict", clip=fitz.Rect(inst[0] - 50, inst[1] - 10, inst[2] + 10, inst[3] + 10))
            for b in block["blocks"]:
                for line in b["lines"]:
                    for span in line["spans"]:
                        author_match = author_pattern.search(span["text"])
                        if author_match:
                            author_name = author_match.group(1).strip()
                            order_marker = author_match.group(2).strip()
                            # Convert letters to numbers if necessary
                            if order_marker.isalpha():
                                # Convert 'a' to 1, 'b' to 2, etc.
                                order = ord(order_marker.lower()) - ord('a') + 1
                            else:
                                order = int(order_marker)
                            # Add to dictionary, checking for duplicates
                            if author_name not in author_order_dict:
                                author_order_dict[author_name] = order

    # Convert the author dictionary to a sorted list of tuples
    authors = sorted(author_order_dict.items(), key=lambda x: x[1])

    # Extract Corresponding Author
    corresponding_author_match = corresponding_author_pattern.search(full_text)
    if corresponding_author_match:
        corresponding_author = corresponding_author_match.group(1).strip()

    # Close the PDF file
    doc.close()

    return journal_name, publication_date, indexing_agency, article_type, authors, corresponding_author

# Example usage
pdf_path = 'example1.pdf'  # Update this path to your PDF file
article_details = extract_complete_article_details(pdf_path)

# Formatting and printing the output
print("(a) Name of the Journal -", article_details[0])
print("(b) Date of Publication -", article_details[1])
print("(c) Authorship sequence:")
# print("(d) Authorship sequence:", article_type_patterns)
print(article_details)
for author, order in article_details[4]:
    suffix = "th"
    if order == 1: suffix = "st"
    elif order == 2: suffix = "nd"
    elif order == 3: suffix = "rd"
    print(f"    {order}{suffix} author: {author}")

import fitz  # PyMuPDF
import re

import fitz  # PyMuPDF
import re

def extract_authorship_sequence_from_title(pdf_path: str):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Assuming the title and authors are on the first page
    first_page_text = doc[0].get_text("text")

    # Regular expression to identify the title and the authors right after it
    # This pattern assumes the title ends with a newline and authors are listed after it
    title_authors_pattern = re.compile(r"^(.+?)\n([A-Za-z\s,]+)(\d+|[a-d]),?([A-Za-z\s,]+)(\d+|[a-d])", re.MULTILINE)

    match = title_authors_pattern.search(first_page_text)
    authors = []
    if match:
        # Extract authors
        for i in range(2, 6, 2):  # Author names are in groups 2 and 4
            author_name = match.group(i).strip()
            authors.append(author_name)

    # Close the PDF file
    doc.close()

    return authors

# Extract authorship sequence from the provided PDF
pdf_path = 'example.pdf'
authorship_sequence = extract_authorship_sequence_from_title(pdf_path)
print(authorship_sequence)

