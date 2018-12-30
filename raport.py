#!/usr/bin/python3
#version 1.0.0
#TO DO:
#Inlocuieste declararile de widgets cu un .kv
import datetime

from kivy.app import App 
from kivy.clock import Clock

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
#Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 800)

class Tehnician():
    def __init__(self, nume):
        self.deranjamente = [None, None]
        self.nume = nume
        with open('tehnicieni/' + str(nume), 'w') as a:
            temp = datetime.datetime.now()
            a.write("Raportul pentru {} din data de {}-{}-{} ".format(nume, temp.day, temp.month, temp.year))
            a.write("tura A\n\n") if (temp.hour > 5 and temp.hour < 15) else a.write("tura B\n\n")
    
    def scrie(self, locatie, comentariu, asign, term):
        with open('tehnicieni/' + str(self.nume), 'a') as a:
            temp = datetime.datetime.now()
            if len(locatie.text) != 0 and asign.active:
                a.write('[{}:{}] A fost asignat la {}.'.format(str(temp.hour).rjust(2, '0'), str(temp.minute).rjust(2, '0'), locatie.text.strip(' ')))
                self.deranjamente.append([locatie.text, temp])
                asign.active = False
                if len(comentariu.text) != 0:
                    a.write(' {}.\n'.format(comentariu.text))
                    comentariu.text = ''
                else:
                    a.write('\n')
                self.deranjamente = [locatie.text, temp] #alternativa cu self.deranjamente sa fie o lista de liste si sa fac append pentru locatie data None. Daca are None inseamna ca nu a terminat si sa parcurga fiecare lista din lista
                locatie.text = ''
            elif (len(locatie.text) != 0 and locatie.text == self.deranjamente[0]) and term.active:
                a.write('[{}:{}] A terminat la {}. A stat {}.'.format(str(temp.hour).rjust(2, '0'), str(temp.minute).rjust(2, '0'), locatie.text.strip(' '), self.calculeaza((temp - self.deranjamente[1]).seconds)))
                locatie.text = ''
                term.active = False
                self.deranjamente = [None, None]
                if len(comentariu.text) != 0:
                    a.write(' {}.\n\n'.format(comentariu.text))
                    comentariu.text = ''
                else:
                    a.write('\n\n')
            elif len(comentariu.text) != 0:
                a.write('[{}:{}] {}.\n'.format(str(temp.hour).rjust(2, '0'), str(temp.minute).rjust(2, '0'), comentariu.text))
                comentariu.text = ''

    def calculeaza(self, x):
        minute = x // 60
        ore = minute // 60
        minute %= 60

        timp = ''

        if ore != 0:
            if ore > 1:
                timp += "{} ore si ".format(ore)
            else:
                timp += "1 ora si "
        if minute > 1:
            timp += "{} minute".format(minute)
        else:
            timp += "1 minut"

        return timp

class Raport(App):
    def build(self):
        self.tehnicieni = []
        self.curent = None

        root = GridLayout(cols = 1)
        
        grid2 = BoxLayout(orientation = 'horizontal')
        root.add_widget(grid2)
        
        self.box = BoxLayout(orientation = 'vertical', size_hint = (None, None), width = 150, height = 300)
        butoane = RelativeLayout(size_hint = (None, None), width = 800, height = 300)
        self.informatii = BoxLayout(orientation = 'vertical', size_hint = (None, None), width = 200, height = 300)
        grid2.add_widget(self.box)
        grid2.add_widget(self.informatii)
        grid2.add_widget(butoane)

        self.text = TextInput(text = "PLACEHOLDER", multiline = True, height = 500, size_hint_y = None)
        with open("Readme.txt", 'r') as a:
            self.text.text = a.read()
        root.add_widget(self.text)

        butoane.add_widget(Label(text = "ID tehnician", pos = (123 ,255), height = 30, width = 50, size_hint = (None, None)))
        butoane.add_widget(Label(text = "Start shift", pos = (11, 255), height = 30, width = 50, size_hint = (None, None)))
        butoane.add_widget(Label(text = "End shift", pos = (12, 190), height = 30, width = 50, size_hint = (None, None)))
        butoane.add_widget(Label(text = "Cod Locatie", pos = (150, 120), height = 30, width = 50, size_hint = (None, None)))
        butoane.add_widget(Label(text = "Comentariu", pos = (430, 120), height = 30, width = 50, size_hint = (None, None)))
        butoane.add_widget(Label(text = "Asignat", pos = (13, 120), height = 30, width = 50, size_hint = (None, None)))
        butoane.add_widget(Label(text = "Terminat", pos = (13, 60), height = 30, width = 50, size_hint = (None, None)))

        teh_id = TextInput(multiline = False, pos = (100, 225), height = 30, width = 100, size_hint = (None, None), write_tab = False, on_text_validate = self.tehnician_shift)
        butoane.add_widget(teh_id)
        self.teh_start = CheckBox(group = "tehnicieni", pos = (0, 200), height = 80, width = 80, size_hint = (None, None))
        butoane.add_widget(self.teh_start)
        self.teh_finish = CheckBox(group = "tehnicieni",  pos = (0, 135), height = 80, width = 80, size_hint = (None, None))
        butoane.add_widget(self.teh_finish)
        self.locatie = TextInput(multiline = False, pos = (105, 90), height = 30, width = 150, size_hint = (None, None), write_tab = False, on_text_validate = self.scrie)
        butoane.add_widget(self.locatie)
        self.comentariu = TextInput(multiline = False, pos = (280, 90), height = 30, width = 400, size_hint = (None, None), write_tab = False, on_text_validate = self.scrie)
        butoane.add_widget(self.comentariu)
        self.cod_asign = CheckBox(group = "cod", pos = (0, 65), height = 80, width = 80, size_hint = (None, None))
        butoane.add_widget(self.cod_asign)
        self.cod_term = CheckBox(group = "cod", pos = (0, 5), height = 80, width = 80, size_hint = (None, None))
        butoane.add_widget(self.cod_term)
        scrie = Button(text = "Scrie", pos = (105, 30), height = 30, width = 50, size_hint = (None, None), on_press = self.scrie)
        butoane.add_widget(scrie)
        update = Button(text = "Update", pos = (200, 30), height = 30, width = 60, size_hint = (None, None), on_press = self.update)
        butoane.add_widget(update)
        gen_raport = Button(text = "Genereaza raport", pos = (500, 250), height = 30, width = 130, size_hint = (None, None), on_press = self.genereaza_raport)
        butoane.add_widget(gen_raport)

        Clock.schedule_interval(self.label_inform, 1)

        return root

    def tehnician_shift(self, instance):
        if self.teh_start.active and instance.text not in [x.nume for x in self.tehnicieni]:
            self.tehnicieni.append(Tehnician(instance.text))
            self.curent = self.tehnicieni[0]
        if self.teh_finish.active:
            for x in self.tehnicieni:
                if x.nume == instance.text:
                    self.tehnicieni.remove(x)
        instance.text = ''
        self.update_tehnicieni()

    def update_tehnicieni(self):
        self.box.clear_widgets()
        for x in self.tehnicieni:
            self.box.add_widget(Button(text = x.nume, on_press = self.citeste))

    def citeste(self, instance):
        for x in self.tehnicieni:
            if instance.text == x.nume:
                self.curent = x

        with open('tehnicieni/' + instance.text, 'r') as a:
            self.text.text = a.read()

    def label_inform(self, x):
        if len(self.tehnicieni) != 0:
            self.informatii.clear_widgets()
            temp = datetime.datetime.now()
            for x in self.tehnicieni:
                if x.deranjamente[0] != None:
                    self.informatii.add_widget(Label(text = "{} {}".format(x.deranjamente[0], self.ceas((temp - x.deranjamente[1]).seconds))))
                else:
                    self.informatii.add_widget(Label(text = ""))

    def ceas(self, x):
        minute = x // 60
        ore = minute // 60
        minute %= 60

        timp = ''

        if ore != 0:
            timp = timp + str(ore).rjust(2, '0') + ":"
        else:
            timp = "00:"
        if minute != 0:
            timp = timp + str(minute).rjust(2, '0')
        else:
            timp += "00"

        return timp

    def citeste_update(self, instance, tehnician):
        for x in self.tehnicieni:
            if tehnician == x.nume:
                self.curent = x

        with open('tehnicieni/' + tehnician, 'r') as a:
            self.text.text = a.read()

    def scrie(self, instance):
        if self.curent != None:
            self.curent.scrie(self.locatie, self.comentariu, self.cod_asign, self.cod_term)
            self.citeste_update(self, self.curent.nume)

    def update(self, instance):
        if self.curent != None:
            with open('tehnicieni/' + self.curent.nume, 'w') as a:
                self.text.text += '\n'
                a.write(self.text.text)

    def genereaza_raport(self, instance):
        temp = datetime.datetime.now()
        with open('Raport', 'w') as a:
            a.write("Situatie tehnicieni {}-{}-{} ".format(temp.day, temp.month, temp.year))
            a.write("tura A\n\n") if (temp.hour > 5 and temp.hour < 15) else a.write("tura B\n\n")
        with open("Raport", 'a') as raport:
            for x in self.tehnicieni:
                with open("tehnicieni/" + x.nume, 'r') as a:
                    raport.write(a.read())
            raport.write("Situatie tehnicieni {}-{}-{} ".format(temp.day, temp.month, temp.year))
            raport.write("tura A") if (temp.hour > 5 and temp.hour < 15) else raport.write("tura B")
        self.text.text = "Raportul a fost generat cu succes pentru toti cei {} tehnicieni!".format(len(self.tehnicieni))
                
def main():
    a = Raport()
    a.run()

if __name__  == "__main__":
    main()