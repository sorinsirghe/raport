#!/usr/bin/python3
import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.config import Config

Config.set('input', 'mouse', 'mouse, disable_multitouch')
Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 800)

def elapsed_time(seconds, flag):
    temp = str(datetime.timedelta(seconds = seconds)).split(':')
    time = ''

    if flag == 0:
        if int(temp[0]) != 0:
            if int(temp[0]) > 1:
                time += "{} hours and  ".format(temp[0])
            else:
                time += "1 hour and "
        if int(temp[1]) > 1:
            time += "{} minutes".format(temp[1])
        else:
            time += "1 minute"
        return time
    elif flag == 1:
        if int(temp[0]) != 0:
            time = time + temp[0].rjust(2, '0') + ":"
        else:
            time = "00:"
        if int(temp[1]) != 0:
            time = time + temp[1].rjust(2, '0')
        else:
            time += "00"
        return time

class Tehnician():
    def __init__(self, name):
        self.assigned_code = [None, None]
        self.name = name
        try:
            with open("Technicians/" + self.name) as a:
                pass
        except:
            self.refresh()

    def write(self, complaint_code, comment, code_assign, code_finish):
        with open('Technicians/' + self.name, 'a') as a:
            temp = datetime.datetime.now()
            if len(complaint_code.text) != 0 and code_assign.active:
                a.write('[{}:{}] Has been assigned to {}.'.format(str(temp.hour).rjust(2, '0'), str(temp.minute).rjust(2, '0'), complaint_code.text.strip('. ')))
                self.assigned_code.append([complaint_code.text, temp])
                code_assign.active = False
                if len(comment.text) != 0:
                    a.write(' {}.\n'.format(comment.text))
                    comment.text = ''
                else:
                    a.write('\n')
                self.assigned_code = [complaint_code.text, temp]
                complaint_code.text = ''
            elif (len(complaint_code.text) != 0 and complaint_code.text == self.assigned_code[0]) and code_finish.active:
                a.write('[{}:{}] Has finished at {}. It took him {}.'.format(str(temp.hour).rjust(2, '0'), str(temp.minute).rjust(2, '0'), complaint_code.text.strip(' '), elapsed_time((temp - self.assigned_code[1]).seconds, 0)))
                complaint_code.text = ''
                code_finish.active = False
                self.assigned_code = [None, None]
                if len(comment.text) != 0:
                    a.write(' {}.\n\n'.format(comment.text))
                    comment.text = ''
                else:
                    a.write('\n\n')
            elif len(comment.text) != 0:
                a.write('[{}:{}] {}.\n'.format(str(temp.hour).rjust(2, '0'), str(temp.minute).rjust(2, '0'), comment.text))
                comment.text = ''

    def refresh(self):
        with open('Technicians/' + str(self.name), 'w') as a:
            temp = datetime.datetime.now()
            a.write("The report for {} from {}-{}-{} ".format(self.name, temp.day, temp.month, temp.year))
            a.write("shift A\n\n\n") if temp.hour < 15 else a.write("shift B\n\n\n")

class Interface(GridLayout):
    def __init__(self, **kwargs):
        Builder.load_file('./Resources/raport.kv')
        super(Interface, self).__init__(**kwargs)
        self.technicians = []
        self.current = None
        with open("Resources/Readme.txt", 'r') as a:
            self.ids.text_area.text = a.read()
        Clock.schedule_interval(self.code_information, .6)

    def technician_shift(self):
        if self.ids.teh_start.active and self.ids.teh_name.text not in [x.name for x in self.technicians]:
            self.technicians.append(Tehnician(self.ids.teh_name.text))
            self.current = self.technicians[0]
        if self.ids.teh_finish.active:
            for x in self.technicians:
                if x.name == self.ids.teh_name.text:
                    self.technicians.remove(x)
        self.ids.teh_name.text = ''
        self.update_technicians()

    def update_technicians(self):
        self.ids.tech_avail.clear_widgets()
        for x in self.technicians:
            self.ids.tech_avail.add_widget(Button(text = x.name, on_press = self.read, size_hint = (.6, .3)))

    def read(self, instance):
        for x in self.technicians:
            if instance.text == x.name:
                self.current = x
        try:
            with open("Technicians/" + instance.text, 'r'):
                pass
        except:
            self.current.refresh()
        with open('Technicians/' + instance.text, 'r') as a:
            self.ids.text_area.text = a.read()

    def read2(self, instance, technician):
        for x in self.technicians:
            if technician == x.name:
                self.current = x
        try:
            with open('Technicians/' + technician.name, 'r') as a:
                self.ids.text_area.text = a.read()
        except:
            pass

    def code_information(self, x):
        if len(self.technicians) != 0:
            self.ids.tech_info.clear_widgets()
            temp = datetime.datetime.now()
            for x in self.technicians:
                if x.assigned_code[0] != None:
                    self.ids.tech_info.add_widget(Label(text = "{} {}".format(x.assigned_code[0], elapsed_time((temp - x.assigned_code[1]).seconds, 1)), size_hint = (.6, .3)))
                else:
                    self.ids.tech_info.add_widget(Label(text = "", size_hint = (.6, .3)))

    def write_to_file(self):
        if self.current != None:
            self.current.write(self.ids.complaint_code, self.ids.comment, self.ids.code_assign, self.ids.code_finish)
            self.read2(self, self.current)

    def update_file(self):
        if self.current != None:
            with open('Technicians/' + self.current.name, 'w') as a:
                a.write(self.ids.text_area.text + '\n')

    def generate_report(self):
        temp = datetime.datetime.now()
        with open('Report.txt', 'w') as a:
            a.write("Technician report for {}-{}-{} ".format(temp.day, temp.month, temp.year))
            a.write("Shift A\n") if (temp.hour < 16) else a.write("Shift B\n")
            a.write("Dispatcher: \nDispatcher helper: \n\n\n\n")
        with open("Report.txt", 'a') as report:
            for x in self.technicians:
                with open("Technicians/" + x.name, 'r') as a:
                    report.write(a.read() + "\n\n")
            report.write("Technician report for {}-{}-{} ".format(temp.day, temp.month, temp.year))
            report.write("Shift A") if (temp.hour < 16) else report.write("Shift B")
        with open("Report.txt", 'r') as a:
            self.ids.text_area.text = a.read()

    def refresh(self, flag):
        if flag == 0:
            if self.current != None:
                self.current.refresh()
        elif flag == 1:
            if len(self.technicians) != 0:
                for x in self.technicians:
                    x.refresh()
        self.read2(self, self.current)


class Raport(App):
    def build(self):
        return Interface()

def main():
    Raport().run()

if __name__  == "__main__":
    main()
