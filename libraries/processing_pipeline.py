import libraries.image_preproccesing as ip
import libraries.ocr as ocr
import libraries.predict as ai
import libraries.translator as tr
import libraries.json_parser as jp
import json
import cv2



if __name__ == '__main__':
    print('Processing pipeline is running')
    pdf_path = 'factura69.pdf'
    image_chunks = ip.pdf_to_img_chunks(pdf_path)


    tokens = []
    labels = []
    for i, image in enumerate(image_chunks):
        text = ocr.ocr(image)
        current_tokens,current_labels = ai.predict(text)
        tokens.append(current_tokens)
        labels.append(current_labels)
        

    for i in range(len(tokens)):
        current_tokens, current_labels = tr.unify_tokens(tokens[i],labels[i])
        current_tokens, current_labels = tr.merge_same_labels(current_tokens, current_labels)
        tokens[i] = current_tokens
        labels[i] = current_labels


    json_result = jp.convert_words_and_labels_into_json(labels,tokens)

    ##Conver to json format the dictionary
    json_result = json.dumps(json_result, indent=4)
    
    
def process_pdf(pdf_path):
    image_chunks = ip.pdf_to_img_chunks(pdf_path)

    tokens = []
    labels = []
    for i, image in enumerate(image_chunks):
        text = ocr.ocr(image)
        current_tokens,current_labels = ai.predict(text)
        tokens.append(current_tokens)
        labels.append(current_labels)
        

    for i in range(len(tokens)):
        current_tokens, current_labels = tr.unify_tokens(tokens[i],labels[i])
        current_tokens, current_labels = tr.merge_same_labels(current_tokens, current_labels)
        tokens[i] = current_tokens
        labels[i] = current_labels


    json_result = jp.convert_words_and_labels_into_json(labels,tokens)

    ##Convert to json format the dictionary
    json_result = json.dumps(json_result, indent=4)
    return json_result