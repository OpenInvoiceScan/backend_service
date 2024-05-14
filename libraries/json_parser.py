labels = [
    "O",  # Para tokens que no son parte de ninguna entidad nombrada
    "B-invoice_id", 
    "B-issue_date",
    "B-due_date",
    "B-issuer_name",
    "B-issuer_address", 
    "B-issuer_phone",
    "B-issuer_email",
    "B-issuer_tax_id",
    "B-recipient_name",
    "B-recipient_address", 
    "B-recipient_phone",
    "B-recipient_email",
    "B-recipient_tax_id",
    "B-item_description",
    "B-item_quantity",
    "B-item_unit_price",
    "B-item_total",
    "B-subtotal",
    "B-tax_description",
    "B-tax_percentage",
    "B-tax_amount",
    "B-total",
    "B-payment_method",
    "UNK"
]

json_example = {
  "invoice_id": 639759,
  "issue_date": "2024-03-21",
  "due_date": "2024-05-05",
  "issuer": {
    "name": "Rodriguez, Brown and Lewis",
    "address": "31217 Ian Throughway\nSharonhaven, DE 45188",
    "phone": "(808)212-5827",
    "email": "ubrown@vazquez-kelly.com",
    "tax_id": "sUZ892jNn684"
  },
  "recipient": {
    "name": "Ashley Watkins",
    "address": "48121 Orr Light\nRichardport, WI 04499",
    "phone": "(312)684-3707x308",
    "email": "petersonashley@yahoo.com",
    "tax_id": "uBT515oVi983"
  },
  "items": [
    {
      "description": "orchestrate integrated e-markets",
      "quantity": 7,
      "unit_price": 22.78,
      "total": 159.46
    }
  ],
  "subtotal": 159.46,
  "taxes": [
    {
      "description": "VAT",
      "percentage": 16,
      "amount": 25.51
    }
  ],
  "total": 184.97,
  "payment_method": "Credit Card",
  "currency": "EUR"
}


def convert_words_and_labels_into_json(labels_chunks, tokens_chunks):
    result = {}
    result['issuer'] = {}
    result['recipient'] = {}
    result['items'] = []
    result['taxes'] = []
    
    current_item = {}
    current_tax = {}
    
    for i in range(len(labels_chunks)):
        for j in range(len(labels_chunks[i])):
            if labels_chunks[i][j].startswith('B-issuer'):
                issuer_key = parse_issuer(tokens_chunks[i][j],labels_chunks[i][j])
                if issuer_key:
                    result['issuer'][issuer_key] = tokens_chunks[i][j]
            elif labels_chunks[i][j].startswith('B-recipient'):
                recipient_key = parse_recipient(tokens_chunks[i][j],labels_chunks[i][j])
                if recipient_key:
                    result['recipient'][recipient_key] = tokens_chunks[i][j]
            elif labels_chunks[i][j].startswith('B-item'):
                item_key = parse_item(tokens_chunks[i][j],labels_chunks[i][j])
                if item_key:
                    if item_key == 'description' and current_item:
                        result['items'].append(current_item)
                        current_item = {}
                    current_item[item_key] = tokens_chunks[i][j]
            elif labels_chunks[i][j].startswith('B-tax'):
                tax_key = parse_tax(tokens_chunks[i][j],labels_chunks[i][j])
                if tax_key:
                    if tax_key == 'description' and current_tax:
                        result['taxes'].append(current_tax)
                        current_tax = {}
                    current_tax[tax_key] = tokens_chunks[i][j]
            elif labels_chunks[i][j].startswith('B-'):
                generic_key = parse_generic(tokens_chunks[i][j], labels_chunks[i][j])
                if generic_key:
                    result[generic_key] = tokens_chunks[i][j]
    
    if current_item:
        result['items'].append(current_item)
    if current_tax:
        result['taxes'].append(current_tax)
    
    return result

def parse_generic(token, label):
    if label == 'B-invoice_id':
        return 'invoice_id'
    elif label == 'B-issue_date':
        return 'issue_date'
    elif label == 'B-due_date':
        return 'due_date'
    elif label == 'B-subtotal':
        return 'subtotal'
    elif label == 'B-total':
        return 'total'
    elif label == 'B-payment_method':
        return 'payment_method'
    elif label == 'B-currency':
        return 'currency'
    else:
        return None

def parse_issuer(token,label):
    if label == 'B-issuer_name':
        return 'name'
    elif label == 'B-issuer_address':
        return 'address'
    elif label == 'B-issuer_phone':
        return 'phone'
    elif label == 'B-issuer_email':
        return 'email'
    elif label == 'B-issuer_tax_id':
        return 'tax_id'
    else:
        return None

def parse_recipient(token,label):
    if label == 'B-recipient_name':
        return 'name'
    elif label == 'B-recipient_address':
        return 'address'
    elif label == 'B-recipient_phone':
        return 'phone'
    elif label == 'B-recipient_email':
        return 'email'
    elif label == 'B-recipient_tax_id':
        return 'tax_id'
    else:
        return None

def parse_item(token,label):
    if label == 'B-item_description':
        return 'description'
    elif label == 'B-item_quantity':
        return 'quantity'
    elif label == 'B-item_unit_price':
        return 'unit_price'
    elif label == 'B-item_total':
        return 'total'
    else:
        return None

def parse_tax(token,label):
    if label == 'B-tax_description':
        return 'description'
    elif label == 'B-tax_percentage':
        return 'percentage'
    elif label == 'B-tax_amount':
        return 'amount'
    else:
        return None
