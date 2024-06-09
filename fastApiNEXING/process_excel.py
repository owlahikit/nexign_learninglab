import requests
import uvicorn
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO
from model import res  # Подключаем вашу функцию обработки изображения

def process_excel(file_contents: bytes):
    # Считываем Excel файл в DataFrame
    df = pd.read_excel(BytesIO(file_contents))

    # Применяем вашу функцию к данным
    data = df[['Наименование ТТ', 'Ссылка на фото', 'Оценка']]
    data = data.dropna()
    data['Наименование ТТ'] = data['Наименование ТТ'].str.split().str[0]
    data['Ссылка на фото'] = data['Ссылка на фото'].astype(str)
    data = data.groupby('Наименование ТТ')['Ссылка на фото'].apply(lambda x: ', '.join(x)).reset_index()
    data = data.head(10)
    end_dict = {}
    for i in data['Наименование ТТ']:
        filtered_links = data[data['Наименование ТТ'] == i]['Ссылка на фото'].str.split(', ').tolist()[0]
        score = 0
        status = ""
        for j in filtered_links:
            response = requests.get(f'{j}')
            img = Image.open(BytesIO(response.content))
            try:
                score += res(img)
            except AttributeError:
                ...
        if len(filtered_links) == 1:
            if score <= 2:
                status = 'Диспаритет'
            elif score <= 5:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 2:
            if score <= 4:
                status = 'Диспаритет'
            elif score <= 8:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 3:
            if score <= 5:
                status = 'Диспаритет'
            elif score <= 11:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 4:
            if score <= 6:
                status = 'Диспаритет'
            elif score <= 14:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 5:
            if score <= 7:
                status = 'Диспаритет'
            elif score <= 16:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 6:
            if score <= 8:
                status = 'Диспаритет'
            elif score <= 18:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 7:
            if score <= 9:
                status = 'Диспаритет'
            elif score <= 20:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 8:
            if score <= 10:
                status = 'Диспаритет'
            elif score <= 22:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 9:
            if score <= 11:
                status = 'Диспаритет'
            elif score <= 24:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 10:
            if score <= 12:
                status = 'Диспаритет'
            elif score <= 26:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 11:
            if score <= 13:
                status = 'Диспаритет'
            elif score <= 28:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 12:
            if score <= 14:
                status = 'Диспаритет'
            elif score <= 30:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 13:
            if score <= 15:
                status = 'Диспаритет'
            elif score <= 32:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 14:
            if score <= 16:
                status = 'Диспаритет'
            elif score <= 34:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 15:
            if score <= 17:
                status = 'Диспаритет'
            elif score <= 36:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 16:
            if score <= 18:
                status = 'Диспаритет'
            elif score <= 38:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 17:
            if score <= 19:
                status = 'Диспаритет'
            elif score <= 40:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 18:
            if score <= 20:
                status = 'Диспаритет'
            elif score <= 42:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 19:
            if score <= 21:
                status = 'Диспаритет'
            elif score <= 44:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) == 20:
            if score <= 22:
                status = 'Диспаритет'
            elif score <= 46:
                status = "Паритет"
            else:
                status = "Приоритет"
        if len(filtered_links) > 4:
            end_dict[i] = (score, status, '>4', 'актуально')
        else:
            end_dict[i] = (score, status, '<=4', 'актуально')
        print(score, status)

    data_dict = pd.DataFrame.from_dict(end_dict, orient='index',
                                       columns=['Оценка', 'Статус', 'Кол-во фото', 'Актуальность'])
    data_dict.reset_index(inplace=True)
    data_dict.rename(columns={'index': 'Наименование ТТ'}, inplace=True)

    # Объединяем исходные данные с результатами обработки
    result = pd.merge(data, data_dict, on='Наименование ТТ', how='left')

    # Возвращаем DataFrame с результатом
    return result
