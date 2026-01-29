import re

def search_query(query:str) -> str:
    """
    cleans raw search query

    Args:
        query: raw search query (string)

    Returns:
        a clean search query (string)
    """
    # 1. Remove all ambiguous symbols
    cleaned_query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    
    # 2. Keep only the first occurrence of each word
    words = cleaned_query.split(" ")
    seen = set()
    unique_words = []

    for word in words:
        lower_word = word.lower()  # optional: treat 'Life' and 'life' as duplicates
        if lower_word not in seen:
            seen.add(lower_word)
            unique_words.append(word)

    cleaned_query = " ".join(unique_words)

    # 3. Replace multiple consecutive spaces with a single space
    cleaned_query = re.sub(r"\s+", " ", cleaned_query).strip()

    # print(cleaned_query)
    return cleaned_query


sample_query = "@Rise #& Above! Life $& Struggles %42 — Keep_Hope! Life Always? Move*Forward & Learn@ Life"
search_query(query=sample_query)

# @Rise #& Above! Life $& Struggles %42 — Keep_Hope! Life Always? Move*Forward & Learn@ Life
# Chokra Jawaan Ishaqzaade Amit Trivedi Amit Trivedi; Vishal Dadlani; Sunidhi Chauhan; Habib Faisal