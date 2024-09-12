from transformers import pipeline

triplet_extractor = pipeline(
    "text2text-generation",
    model="Babelscape/rebel-large",
    tokenizer="Babelscape/rebel-large",
)

# We need to use the tokenizer manually since we need special tokens.
extracted_text = triplet_extractor.tokenizer.batch_decode(
    [
        triplet_extractor(
            "Kamala Devi Harris is an American politician and attorney who is the 49th and current vice president of the United States since 2021 under President Joe Biden. She is the first female vice president, making her the highest-ranking female official in U.S. history, as well as the first African American and first Asian American vice president.[3][4] A member of the Democratic Party, she served as a U.S. senator from California from 2017 to 2021, and earlier as the attorney general of California. Harris is the Democratic Party's presidential nominee in the 2024 United States presidential election.",
            return_tensors=True,
            return_text=False,
        )[0]["generated_token_ids"]
    ]
)

print(extracted_text[0])


# Function to parse the generated text and extract the triplets
def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = "", "", "", ""
    text = text.strip()
    current = "x"
    for token in (
        text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split()
    ):
        if token == "<triplet>":
            current = "t"
            if relation != "":
                triplets.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
                relation = ""
            subject = ""
        elif token == "<subj>":
            current = "s"
            if relation != "":
                triplets.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
            object_ = ""
        elif token == "<obj>":
            current = "o"
            relation = ""
        else:
            if current == "t":
                subject += " " + token
            elif current == "s":
                object_ += " " + token
            elif current == "o":
                relation += " " + token
    if subject != "" and relation != "" and object_ != "":
        triplets.append(
            {"head": subject.strip(), "type": relation.strip(), "tail": object_.strip()}
        )
    return triplets


extracted_triplets = extract_triplets(extracted_text[0])
print(extracted_triplets)
