'''
Первая, сырая, версия самозополняемого словаря.
Весь необходимый функционал работоспособен,
но необходим рефакторинг кода

28.09.2018
'''

from tkinter import Tk, Entry, Button, Text, Label
import shelve

class Application(Tk):
    '''Дочерний класс Tk, создающий оконное приложение'''
    def __init__(self, title, geometry):
        super(Application, self).__init__(title, geometry)
        self.title(title)
        self.geometry(geometry)
        self.file_name = 'lib/dict'
        self.resizable(width = False, height = False)

    def create_entry_field(self, first_row):
        '''Создаем строку для ввода текста'''
        self.textfield = Entry(self)
        self.textfield.grid(row = first_row, columnspan = 1, sticky = 'W, E, N, S')

    def create_stack_of_buttons(self, first_row, buttons):
        '''Создаем в цикле столбик из кнопок. В передаваемом словаре ключи содержат названия кнопок, а значения - функции при нажатии'''
        i = first_row
        for purpose in buttons:
            i += 1
            Button(self, text = purpose, command = buttons[purpose]).grid(row = i, column = 0, sticky = 'W, E, N, S')

    def create_status_bar(self, columnspan):
        '''Создаем надпись, которая будет оповещать о выполненных операциях'''
        self.status_bar = Label(text = "Готов к работе!")
        self.status_bar.grid(row = 6, column = 1, columnspan = columnspan, sticky = 'E, S')

    def overwrite_label(self, text):
        '''Изменяем надпись'''
        self.status_bar.config(text = text)

    def create_textbox(self, width, height, rowspan):
        '''Создаем текстовое поле'''
        self.textbox = Text(self, width = width, height = height, wrap = 'word', state = 'normal')
        self.textbox.grid(row = 0, column = 1, rowspan = rowspan, sticky = 'W, E, N, S')

    def overwrite_textbox(self, text):
        '''Перезаписываем содержимое текстового поля'''
        self.textbox.delete('0.0', 'end')
        self.textbox.insert('0.0', text)

    def find_word(self):
        '''Функция поиска слов в словаре'''
        word = self.textfield.get()
        if ' ' in word:
            self.overwrite_label('Введено больше одного слова')
        else:
            word = word.capitalize()
            with shelve.open(self.file_name) as dictionary:
                try:
                    self.overwrite_textbox(dictionary[word])
                except KeyError:
                    self.overwrite_label('Слова \'' + word + '\' нет в словаре')

    def add_word(self):
        '''Функция добавления нового слова в словарь'''
        word = self.textfield.get()
        if ' ' in word:
            self.overwrite_label('Введено больше одного слова')
        else:
            word = word.capitalize()
            with shelve.open(self.file_name) as dictionary:
                dictionary[word] = self.textbox.get('0.0', 'end')
                dictionary.sync()
                self.overwrite_label(word + ' - добавлено в словарь')

    def remove_word(self):
        '''Функция удаления уже имеющегося слова'''
        word = self.textfield.get()
        if ' ' in word:
            self.overwrite_label('Введено больше одного слова')
        else:
            word = word.capitalize()
            with shelve.open(self.file_name) as dictionary:
                try:
                    del dictionary[word]
                    self.overwrite_label(word + ' - удалено')
                except KeyError:
                    self.overwrite_label('Слова \'' + word + '\' нет в словаре')

    def start_application(self):
        '''Запустить цикл обработки сообщений окна'''
        self.mainloop()

if __name__ == "__main__":

    def main():
        '''Функция, задающая приложению нужные параметры'''
        root = Application(geometry = '450x120', title = 'Словарь сложных английских слов')
        root.create_entry_field(first_row = 0)
        buttons = {'Найти слово' : root.find_word, 'Добавить слово' : root.add_word, 'Удалить слово' : root.remove_word}
        root.create_stack_of_buttons(first_row = 1, buttons = buttons)
        root.create_textbox(width = 40, height = 5, rowspan = len(buttons) + 2)
        root.create_status_bar(columnspan = 6)

        root.start_application()

    main()

#В планах:
# 1) Изменить методы __input__ и __exit__, чтобы первый открывал файл, а второй - закрывал (дабы не открывать-закрывать файл при каждой операции)
# 2) Добавить в GUI надписи рядом с полями ввода искомого слова и его определения
# 3) Расформировать класс Application, чтобы он не содержал классов кнопок, полей ввода и т.п.
# 3.1) Создать отдельные дочерние классы кнопки, текстового поля и т.п. с кастомными свойствами, которые сейчас объединены в свойствах Application
# 3.2) В функции main() создать их экземпляры, назначив корневым экземпляр дочернего от Tk() класса
# 3.3) Скорее всего, функции найти-записать-удалить нужно сделать отдельными, вне каких-либо классов
# 3.4) Объекты должны быть созданы так, чтобы этот файл можно было импортировать для приложения-тренажера
# 4) Приложение-тренажер, которое проверяет, насколько закрепилось знание каждого из слов
# 4.1) Ведется статистика слов по частоте правильности ответа на них. Для этого будет храниться свой shelve-файл с количеством правильно угаданных переводов каждого слова
# 4.2) При каждом запуске приложение просматривает записи в shelve-базе словаря. Если есть новые, то она переносит их в свой счетчик, присваивая значение 0
# 4.3) Приложение делает случайный выбор из наименее угадываемых слов (можно использовать нормальное распределение)
# 4.4) Внешний вид: текстовое поле или надпись с запрашиваемым словом; текстовая строка для ввода ответа; текстовое поле для вывода ответа из словаря
# 4.5) На правильность/неправильность проверка производится с помощью конструкции if <ответ_пользователя> in <определение_по_словарю>
# 4.5.1) Привести все буквы описания к нижнему регистру; удалить знаки препинания и английские буквы; разбить по пробелу. Привести к нижнему регистру введенный ответ. Искать совпадение
# 5) Совместить словарь-накопитель с тренажером словарного запаса