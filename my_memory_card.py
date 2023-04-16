from PyQt5.QtCore import Qt
from random import shuffle
from PyQt5.QtWidgets import (
    QApplication, QWidget, 
    QHBoxLayout, QVBoxLayout,
    QGroupBox, QButtonGroup,
    QRadioButton, QPushButton, 
    QLabel)

class Question():
    #содержит вопрос, 1 правильный и 3 неправильных ответа
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        #все строки надо задать при создании объекта, они запоминаются в свойства
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2 
        self.wrong3 = wrong3

questions_list = []
questions_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Бразильский', 'Испанский', 'Итальянский'))
questions_list.append(Question('Какого цвета нет на флаге России?', 'Зелёный', 'Красный', 'Белый', 'Синий'))
questions_list.append(Question('Национальная хижина Якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата'))
app = QApplication([])

window = QWidget()
window.setWindowTitle('Memory Card')
#создаём панель вопроса
btn_OK = QPushButton('Ответить') #кнопка ответа
lb_Question = QLabel('Какой национальности не существует?')  #текст вопроса

RadioGroupBox = QGroupBox('Варианты ответов') #групппа переключателей ответов
rbtn_1 = QRadioButton('Энцы')
rbtn_2 = QRadioButton('Смурфы')
rbtn_3 = QRadioButton('Чулымцы')
rbtn_4 = QRadioButton('Алеуты')

RadioGroup = QButtonGroup()
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout() #вертикальные внутри горизонтальной линии
layout_ans3 = QVBoxLayout()

layout_ans2.addWidget(rbtn_1) #2 ответа в 1 столбец
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) #2 ответа во 2 столбец
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) #разместили столбцы в 1 строке

RadioGroupBox.setLayout(layout_ans1) #панель с вариантами ответов готова

#создаём панель результата
AnsGroupBox = QGroupBox('Результат теста')
lb_Result = QLabel('Правильно/Неправильно') #здесь размещается надпись "правильно/неправильно"
lb_Correct = QLabel('Правильный ответ')  #здесь текст правильного ответа

layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment = (Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment = Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)
#размещаем все виджеты в окне
layout_line1 = QHBoxLayout() #вопрос
layout_line2 = QHBoxLayout() #варианты ответов или результат текста
layout_line3 = QHBoxLayout() #кнопка 'Ответить'

layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter )) 
#размещаем в одной строке обе панели, они будут скрываться и показываться по очереди
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
RadioGroupBox.hide() #эту панель видели, скроем её
#AnsGroupBox.hide()

layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch = 2) #Кнопка должна быть большой
layout_line3.addStretch(1)

#созданные строки разместим друг под другом
layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch = 2)
layout_card.addLayout(layout_line2, stretch = 8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch = 1)
layout_card.addStretch(1)
layout_card.setSpacing(5) #Пробелы между содержимым
#Виджеты и макеты созданы, создаём функции:
def show_result():
    '''Показать панель ответа'''
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Следующий вопрос')

def show_question():
    '''Показать панель вопросов'''
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')
    RadioGroup.setExclusive(False) #Ограничения сняты для сброса выбора флага
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True) #Здесь может быть выбран только 1 флаг, т.к. ограничения вернулись

answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]

def ask(q: Question):
    #функция записывает значения вопросов и ответов, соответствующие виджеты 
    #при этом варианты ответов распределяются случайным образом
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question)
    lb_Correct.setText(q.right_answer)
    show_question()

def show_correct(res):
    #показать результат, установить переданный в надпись "результат" и показать нужную нам панель
    lb_Result.setText(res)
    show_result()
'''
def start_test():
    #временная функция, позволяющая вызвать def show_result() и def show_question()
    if 'ответить' == btn_OK.text():
        show_result()
    else:
        show_question()
'''
def check_answer():
    #если выбран какой-то вариант ответа, то проверить и показать панель ответов
    if answers[0].isChecked():
        #правильный ответ
        show_correct('Правильно!')
        window.score += 1
        print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
        print('Рейтинг: ', (window.score/window.total*100), '%')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            #неправильный ответ 
            show_correct('Неверно!')
            print('Рейтинг: ', (window.score/window.total*100), '%')

def next_question():
    #задаёт последующие вопросы из списка
    #этой функции нужна переменная, в которой будет указываться номер текущего вопроса
    #эту переменную нужно сделать глобальной, либо же сделать свойством глобального объекта (app или window)
    #мы заведём (ниже) свойствo window.cur_question
    #window.cur_question += 1 #переход к следующему вопросу
    window.total += 1
    print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
    #if window.cur_question >= len(questions_list):
        #window.cur_question = 0 #если список вопросов закончился, идём сначала
    cur_question = randint(0, len(questions_list) - 1)  #здесь нам не нужно старое значение 
    #поэтому можно использовать локальную переменную
    #случайно взяли вопрос в пределах списка
    #если внести около сотни слов, то они редко будут повторяться
    q = questions_list[window.cur_question] #взяли вопрос
    ask(q) #спросили

def click_OK():
    #определяет, надо ли показывать следующий вопрос, либо же ответить на этот
    if btn_OK.text() == 'Ответить':
        check_answer() #проверка ответа
    else:
        next_question() #следующий вопрос


window = QWidget()
window.setLayout(layout_card)
window.setWindowTitle('Memory Card')
#текущий вопрос из списка сделаем свойством объекта 'окно', так мы можем спокойно менять его функции
#window.cur_question = -1 #по-хорошему такие переменные должны быть свойствами 
#только надо написать класс, экземпляр которого получит такие свойства
#но python позволяет создать свойство отдельно взятого экземпляра  
#q=Question('Государственный язык Бразилии', 'Португальский', 'Бразильский', 'Испанский', 'Итальянский')
#ask(q)
#btn_OK.clicked.connect(check_answer) #(start_test) #по нажатии на кнопку выбираем кнопку, что конкретно происходит
#всё построено, осталось задать вопрос и показать окно
btn_OK.clicked.connect(click_OK)  #по нажатии на кнопку выбираем, что конкретно происходит
window.score = 0
window.total = 0
next_question()
window.resize(400, 300)
window.show()
app.exec()