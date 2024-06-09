import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from tempfile import NamedTemporaryFile
from process_excel import process_excel
app = FastAPI()




@app.post("/process-excel/")
async def process_excel_api(file: UploadFile = File(...)):
    """
    Обрабатывает загруженный Excel файл.

    :param file: Загруженный Excel файл для обработки
    :return: Обработанный Excel файл в формате FileResponse
    """
    # Считываем содержимое загруженного файла
    contents = await file.read()

    # Обрабатываем Excel файл
    processed_data = process_excel(contents)

    # Выводим содержимое переменной processed_data для отладки
    print(processed_data)

    # Создаем временный файл и записываем в него содержимое обработанных данных
    with NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_file:
        processed_data.to_excel(tmp_file, index=False)

    # Возвращаем временный файл как FileResponse
    return FileResponse(tmp_file.name, filename="processed_data.xlsx")

if __name__ == '__main__':
    # Run server using given host and port
    uvicorn.run(app, host='127.0.0.1', port=8000)