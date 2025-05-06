# Imagem do python
FROM python:3.13

# Criar o diretorio do App
RUN mkdir /App

# Setar o diretório de trabalho dentro do container
WORKDIR /app

# Setar as variaveis de Desenvolvimento
# Prevenir o Python de Escrever arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents python from buffering stdout and stderr
ENV PYTHONBUFFERED=1

# Atualiza o PIP
RUN pip install --upgrade pip

# Copia o projeto em django e instala as dependencias
COPY requirements.txt /app/

# Instalar todas as dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto para o container
COPY . /app/

# Expõe a porta de rede
EXPOSE 8000

# Rodar em servidor de Desenvolvimento
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]




