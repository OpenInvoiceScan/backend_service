import libraries.image_preproccesing as ip
import libraries.ocr as ocr
import libraries.predict as ai
import libraries.translator as tr
import libraries.json_parser as jp
import libraries.pdf as pdf



import json



def test_pipeline():

    json_result = process_pdf('template2.pdf')

    print(json_result)
    
    
def process_pdf(pdf_path):
    image = pdf.pdf_to_img(pdf_path)
    text = ocr.ocr(image)

    tokens, labels = ai.predict(text)
    
    print(len(tokens))
    print(len(labels))


    current_tokens, current_labels = tr.unify_tokens(tokens,labels)
    current_tokens, current_labels = tr.merge_same_labels(current_tokens, current_labels)
    print(current_tokens)
    print(current_labels)

    for i in range(len(current_tokens)):
        print(current_tokens[i], current_labels[i])



    json_result = jp.convert_words_and_labels_into_json(current_labels,current_tokens)

    ##Convert to json format the dictionary
    json_result = json.dumps(json_result, indent=4)
    return json_result

