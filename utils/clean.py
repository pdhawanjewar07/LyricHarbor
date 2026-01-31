import re

def search_query(query:str) -> str:
    """
    cleans raw search query

    Args:
        query: raw search query (string)

    Returns:
        a clean search query (string)
    """

    # 1. Replace -, _, and . with space
    cleaned_query = re.sub(r"[-_.]", " ", query)

    # 2. Remove all ambiguous symbols
    cleaned_query = re.sub(r"[^a-zA-Z0-9 ]+", "", cleaned_query)

    # 3. Replace multiple consecutive spaces with a single space
    cleaned_query = re.sub(r"\s+", " ", cleaned_query).strip()

    # 4. Remove " Various Interprets" from query
    cleaned_query = re.sub(r"\s*Various Interprets", "", cleaned_query, flags=re.IGNORECASE)

    # print(cleaned_query)
    return cleaned_query


# sample_query = "Ha Raham  (Mehfuz) Aamir  (Original Motion Picture Soundtrack) Amit Trivedi Various Interprets"
# search_query(query=sample_query)

"""
@Rise #& Above! Life $& Struggles %42 — Keep_Hope! Life Always? Move*Forward & Learn@ Life
Chokra Jawaan Ishaqzaade Amit Trivedi Amit Trivedi; Vishal Dadlani; Sunidhi Chauhan; Habib Faisal
Bezubaan Phir Se ABCD 2 Sachin-Jigar Vishal Dadlani; Anushka Manchanda; Madhav Krishna
Jaane Bhi De Heyy Babyy Shankar Mahadevan Shankar Mahadevan
Ha Raham  (Mehfuz) Aamir  (Original Motion Picture Soundtrack) Amit Trivedi Various Interprets
"""