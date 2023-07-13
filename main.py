import os
from background import keep_alive
import pip
import parsing_site
import data
import requests
import json
from data import information

pip.main(['install', 'pytelegrambotapi'])
import telebot
import time
from telebot import types
from dotmap import DotMap

bot = telebot.TeleBot('6002793356:AAGDf_TUAZPfO8q05nu_6VsdwQb9wHkWunM')

vacancie = ''
experience = ''
employment = ''


@bot.message_handler(commands=['start'])
def menu(message):
   start_menu = types.ReplyKeyboardMarkup(True, True)
   start_menu.row('Найти вакансию', 'Рассылка уведомлений')
   bot.send_message(message.chat.id, 'Стартовое меню', reply_markup=start_menu)


@bot.message_handler(content_types=['text'])
def handle_text(message):
  if message.text == 'Найти вакансию':
     source_vacancie_menu = types.ReplyKeyboardMarkup(True, True)
     source_vacancie_menu.row('Поиск вакансии', 'Параметры поиска')
     source_vacancie_menu.row('Главное меню')
     bot.send_message(message.chat.id,
                      'Выберите режим для поиска вакансии',
                      reply_markup=source_vacancie_menu)

  elif message.text == 'Рассылка уведомлений':
    notification_menu = types.ReplyKeyboardMarkup(True, True)
    notification_menu.row('Уведомления')
    notification_menu.row('Отключить все уведомления')
    notification_menu.row('Главное меню')
    bot.send_message(message.chat.id,
                     'Уведмоления(Данное окно находится в разработке)',
                     reply_markup=notification_menu)

  elif message.text == 'Поиск вакансии':
    if vacancie and experience and employment != '':
      #parsing(vacancie, experience, employment)
      vacancy_one = parsing_site.parsing(vacancie, experience, employment)
      print(vacancy_one)
      bot.send_message(message.chat.id, str(vacancy_one))

    else:
      bot.send_message(message.chat.id,
                       'Ошибка вы не ввели параметры для поиска')
      message.text = 'Найти вакансию'
      handle_text(message)

  elif message.text == 'Параметры поиска':
    source_vacancieparam_menu = types.ReplyKeyboardMarkup(
      True, True, True, True)
    source_vacancieparam_menu.row('Название вакансии')
    source_vacancieparam_menu.row('Стаж работы')
    source_vacancieparam_menu.row('Занятость')
    source_vacancieparam_menu.row('Текущие параметры')
    source_vacancieparam_menu.row('Назад')
    bot.send_message(message.chat.id,
                     'Введите или выберите параметры для поиска вакансии',
                     reply_markup=source_vacancieparam_menu)

  elif message.text == 'Название вакансии':
    bot.send_message(message.chat.id, 'Введите название вакансии')
    bot.register_next_step_handler(message, params_vac)
  elif message.text == 'Стаж работы':
    staj_menu = types.ReplyKeyboardMarkup(True, True, True, True)
    staj_menu.row("Нет опыта")
    staj_menu.row("От 1 года до 3 лет")
    staj_menu.row("От 3 до 6 лет")
    staj_menu.row("Более 6 лет")
    bot.send_message(message.chat.id,
                     'Выберите стаж работы:',
                     reply_markup=staj_menu)
    bot.register_next_step_handler(message, params_staj)
  elif message.text == 'Занятость':
    zan_menu = types.ReplyKeyboardMarkup(True, True, True, True)
    zan_menu.row("Полная занятость")
    zan_menu.row("Частичная занятость")
    zan_menu.row("Проектная работа")
    zan_menu.row("Волонтерство")
    zan_menu.row("Стажировка")
    bot.send_message(message.chat.id,
                     'Выберите тип занятости:',
                     reply_markup=zan_menu)
    bot.register_next_step_handler(message, params_Zanyat)
  elif message.text == 'Текущие параметры':
    bot.send_message(
      message.chat.id, 'Текущие параметры:' + ' ' + vacancie + '' +
      employment + ' ' + experience)
    message.text = 'Найти вакансию'
    handle_text(message)
  elif message.text == 'Назад':
    message.text = 'Найти вакансию'
    handle_text(message)
  elif message.text == 'Главное меню':
    menu(message)


def params_vac(message):
  global vacancie
  vacancie = message.text
  bot.reply_to(message, 'Я сохранил это сообщение: ' + vacancie)

  message.text = 'Параметры поиска'
  handle_text(message)


def params_staj(message):
  global experience
  experience = message.text
  bot.reply_to(message, 'Я сохранил это сообщение: ' + experience)
  for i in information["experience"]:
    if (experience == i.name):
      experience = i.id

  message.text = 'Параметры поиска'
  handle_text(message)


def params_Zanyat(message):
  global employment
  employment = message.text
  bot.reply_to(message, 'Я сохранил это сообщение: ' + employment)
  for i in information["employment"]:
    if (employment == i.name):
      employment = i.id

  message.text = 'Параметры поиска'
  handle_text(message)

# echo-функция, которая отвечает на любое текстовое сообщение таким же текстом

keep_alive()  #запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0)  #запуск бота
