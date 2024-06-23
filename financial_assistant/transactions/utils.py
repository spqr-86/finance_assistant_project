import re
from datetime import datetime

import fitz  # PyMuPDF


START_PATTERN = re.compile(r'Номер\sкарты\n')
TRANSACTION_PATTERN = re.compile(r'''
    (\d{2}\.\d{2}\.\d{4})    # Дата операции
    \n
    (\d{2}:\d{2})            # Время операции
    \n
    (\d{2}\.\d{2}\.\d{4})    # Дата списания
    \n
    (\d{2}:\d{2})            # Время списания
    \n
    ([-+]\d{1,3}(?:\s\d{3})*(?:\.\d{2})?)\s₽  # Сумма операции с пробелами для тысяч
    \n
    ([-+]\d{1,3}(?:\s\d{3})*(?:\.\d{2})?)\s₽  # Повтор суммы операции
    \n
    ([^\n]+)                 # Описание операции (одна строка)
    (?:\n([^\n]+))?          # Дополнительная информация (необязательная строка)
    \n
    (\d{4})                  # Номер карты (любые 4 цифры)
    ''', re.VERBOSE | re.MULTILINE)


def extract_text_from_pdf(pdf_data):
    document = fitz.open("pdf", pdf_data)
    return ''.join(page.get_text() for page in document)


def parse_amount(amount_str):
    return float(amount_str.replace(' ', '').replace(',', '.').replace('₽', ''))


def parse_transactions(text):
    transactions_list = []

    start_match = START_PATTERN.search(text)
    if not start_match:
        return transactions_list

    text = text[start_match.end():]
    matches = TRANSACTION_PATTERN.findall(text)

    for match in matches:
        date_time_op = datetime.strptime(f"{match[0]} {match[1]}", '%d.%m.%Y %H:%M')
        date_time_sp = datetime.strptime(f"{match[2]} {match[3]}", '%d.%m.%Y %H:%M')
        amount = parse_amount(match[4])
        amount_card = parse_amount(match[5])
        description = match[6].strip()
        additional_info = match[7].strip() if match[7] else ""
        card_number = match[8]

        transaction = {
            'date_time_operation': date_time_op,
            'date_time_splitting': date_time_sp,
            'amount': amount,
            'amount_card': amount_card,
            'description': description,
            'additional_info': additional_info,
            'card_number': card_number
        }
        transactions_list.append(transaction)

    return transactions_list


def parse_pdf(uploaded_file):
    try:
        with uploaded_file.open('rb') as file:
            pdf_data = file.read()
        text = extract_text_from_pdf(pdf_data)
        transactions_list = parse_transactions(text)
        return transactions_list
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return []
