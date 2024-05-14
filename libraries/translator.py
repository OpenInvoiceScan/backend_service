def unify_tokens(tokens,labels):
    unified_tokens = []
    unified_labels = []
    current_token = ''
    current_label = ''
    for i in range(len(tokens)):
        if tokens[i].startswith('##'):
            current_token += tokens[i][2:]
        else:
            if current_token != '':
                unified_tokens.append(current_token)
                unified_labels.append(current_label)
                current_token = ''
                current_label = ''
            current_token = tokens[i]
            current_label = labels[i]
    if current_token != '':
        unified_tokens.append(current_token)
        unified_labels.append(current_label)
    
    return unified_tokens,unified_labels

def unify_by_labels(tokens,labels):
    unified_tokens = []
    unified_labels = []
    current_token = ''
    current_label = ''
    for i in range(len(tokens)):
        if labels[i].startswith('B-'):
            if current_token != '':
                unified_tokens.append(current_token)
                unified_labels.append(current_label)
                current_token = ''
                current_label = ''
            current_token = tokens[i]
            current_label = labels[i]
        elif labels[i].startswith('I-'):
            if current_token == '':
                current_token = tokens[i]
                current_label = labels[i]
            else:
                current_token += ' ' + tokens[i]
        else:
            if current_token != '':
                unified_tokens.append(current_token)
                unified_labels.append(current_label)
                current_token = ''
                current_label = ''
            unified_tokens.append(tokens[i])
            unified_labels.append(labels[i])

    
    return unified_tokens,unified_labels



def merge_same_labels(tokens, labels):
    merged_tokens = []
    merged_labels = []
    
    current_tokens = tokens[0]
    current_labels = labels[0]
    
    for i in range(1, len(tokens)):
        if labels[i] == current_labels:
            current_tokens += " " + tokens[i]
        elif labels[i].startswith('I-') and current_labels[2:] == labels[i][2:]:
            current_tokens += " " + tokens[i]
        else:
            merged_tokens.append(current_tokens)
            merged_labels.append(current_labels)
            current_tokens = tokens[i]
            current_labels = labels[i]
    
    return merged_tokens, merged_labels


