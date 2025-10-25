# Используем официальный образ Node.js
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install --only=production

# Копируем исходный код
COPY . .

# Собираем приложение
RUN npm run build

# Устанавливаем serve для запуска статических файлов
RUN npm install -g serve

# Открываем порт
EXPOSE 3000

# Команда для запуска приложения
CMD ["serve", "-s", "build", "-l", "3000"]