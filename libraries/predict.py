import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForTokenClassification, BertTokenizerFast
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()


MODEL_NAME = 'google-bert/bert-base-multilingual-cased'
tokenizer = BertTokenizerFast.from_pretrained(MODEL_NAME)
label_encoder = LabelEncoder()
labels = [
    "O", 
    "B-invoice_id", "I-invoice_id",
    "B-issue_date", "I-issue_date",
    "B-due_date", "I-due_date",
    "B-issuer_name", "I-issuer_name",
    "B-issuer_address", "I-issuer_address",
    "B-issuer_phone",
    "B-issuer_email",
    "B-issuer_tax_id",
    "B-recipient_name", "I-recipient_name",
    "B-recipient_address", "I-recipient_address",
    "B-recipient_phone",
    "B-recipient_email",
    "B-recipient_tax_id",
    "B-item_description", "I-item_description",
    "B-item_quantity",
    "B-item_unit_price",
    "B-item_total",
    "B-subtotal",
    "B-tax_description", "I-tax_description",
    "B-tax_percentage",
    "B-tax_amount",
    "B-total",
    "B-payment_method",
    "UNK"
]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

label_encoder.fit(labels)
NUM_LABELS = len(labels)

def load_model(model_path):
    model = BertForTokenClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=False)
    model.to(device)
    model.eval()  
    return model

model = load_model('pretrained/model_state_dict.pth')
print('Model loaded')
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

def predict(text):
    encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    input_ids = encoded_input['input_ids'].to(device)
    attention_mask = encoded_input['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=-1)

    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    predicted_labels = [label_encoder.inverse_transform([label.item()])[0] for label in predictions[0]]

    
    return tokens, predicted_labels

