normal_names = ["wayne", "chen", "wei"]
slander_words = ["ryan", "patrick", "shiu"]
remove_words = ["diddy", "edp", "edp445"]
replace_with = "edp445"


def process_query(query):
    query_lower = query.lower()

    # If the query contains a normal name + any remove word,
    # remove the remove word(s) from the query.
    if any(name in query_lower for name in normal_names):
        words = query.split()

        words = [word for word in words if word.lower() not in remove_words]

        query = " ".join(words)
        query_lower = query.lower()

    # Replace slander words individually
    if not any(name in query_lower for name in normal_names):
        words = query.split()

        words = [
            replace_with if word.lower() in slander_words else word for word in words
        ]

        query = " ".join(words)

    return query
