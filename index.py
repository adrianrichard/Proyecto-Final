from tkinter import ttk
from tkinter import *

import sqlite3

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(BASE_DIR, "bdatos_contrato.db")
# Codium (commit)

class Teacher:
    # connection dir property
    
    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('DOCENTES')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo docente')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # CI Input
        Label(frame, text = 'CI: ').grid(row = 2, column = 0)
        self.ci = Entry(frame)
        self.ci.grid(row = 2, column = 1)

        # Profession Input
        Label(frame, text = 'Profesion: ').grid(row = 3, column = 0)
        self.profession = Entry(frame)
        self.profession.grid(row = 3, column = 1)

        # Career Input
        Label(frame, text = 'Carrera: ').grid(row = 4, column = 0)
        self.career = Entry(frame)
        self.career.grid(row = 4, column = 1)

        # Stuff Input
        Label(frame, text = 'Materia: ').grid(row = 5, column = 0)
        self.stuff = Entry(frame)
        self.stuff.grid(row = 5, column = 1)

        # Schedule Input
        Label(frame, text = 'Horario: ').grid(row = 6, column = 0)
        self.schedule = Entry(frame)
        self.schedule.grid(row = 6, column = 1)

        # Finish date input
        Label(frame, text = 'Fecha de Fin.: ').grid(row = 7, column = 0)
        self.fdate = Entry(frame)
        self.fdate.grid(row = 7, column = 1)

        # Category input
        Label(frame, text = 'Categoria: ').grid(row = 8, column = 0)
        self.category = Entry(frame)
        self.category.grid(row = 8, column = 1)

        # Literal input
        Label(frame, text = 'Literal: ').grid(row = 9, column = 0)
        self.literal = Entry(frame)
        self.literal.grid(row = 9, column = 1)

        # Button Add Teacher
        ttk.Button(frame, text = 'Guardar', command = self.add_teacher).grid(row = 10, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 10, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 11, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'CI', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'BORRAR', command = self.delete_teacher).grid(row = 12, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_teacher).grid(row = 12, column = 1, sticky = W + E)

        # Filling the Rows
        self.get_teacher()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_teacher(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM tcontrato ORDER BY iddocente DESC'
        db_rows = self.run_query(query)
        # filling data
       # for row in db_rows:
        #    self.tree.insert('', 0, text = row[1], values = row[2])

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.ci.get()) != 0 and len(self.profession.get()) != 0 and len(self.career.get()) != 0 and len(self.stuff.get()) != 0 and len(self.schedule.get()) != 0 and len(self.fdate.get()) != 0 and len(self.category.get()) != 0 and len(self.literal.get()) != 0

    def add_teacher(self):
        if self.validation():
            query = 'INSERT INTO tcontrato VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            parameters =  (self.name.get(), self.ci.get(), self.profession.get(), self.career.get(), self.stuff.get(), self.schedule.get(), self.fdate.get(), self.category.get(), self.literal.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Teacher {} added successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.ci.delete(0, END)
            self.profession.delete(0, END)
            self.career.delete(0, END)
            self.stuff.delete(0, END)
            self.schedule.delete(0, END)
            self.fdate.delete(0, END)
            self.category.delete(0, END)
            self.literal.delete(0, END)
        else:
            self.message['text'] = 'Dates is Required'
        self.get_teacher()

    def delete_teacher(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM tcontrato WHERE nombrecompleto = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_teacher()

    def edit_teacher(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        edit_reg = self.run_query('SELECT * FROM tcontrato WHERE nombrecompleto = ?', (name, ))
        old_dates = edit_reg.fetchone()
        old_ci = old_dates[2]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'
        # Name
        Label(self.edit_wind, text = 'Nombre:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[1]), state = 'readonly').grid(row = 0, column = 2)
        new_name = Entry(self.edit_wind)
        new_name.focus()
        new_name.grid(row = 0, column = 3)

        # CI
        Label(self.edit_wind, text = 'CI:').grid(row = 1, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[2]), state = 'readonly').grid(row = 1, column = 2)
        new_ci= Entry(self.edit_wind)
        new_ci.grid(row = 1, column = 3)

        # Profession
        Label(self.edit_wind, text = 'Profesion:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[3]), state = 'readonly').grid(row = 2, column = 2)
        new_profession= Entry(self.edit_wind)
        new_profession.grid(row = 2, column = 3)

        # Career
        Label(self.edit_wind, text = 'Carrera:').grid(row = 3, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[4]), state = 'readonly').grid(row = 3, column = 2)
        new_career= Entry(self.edit_wind)
        new_career.grid(row = 3, column = 3)

        # Stuff
        Label(self.edit_wind, text = 'Materia:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[5]), state = 'readonly').grid(row = 4, column = 2)
        new_stuff= Entry(self.edit_wind)
        new_stuff.grid(row = 4, column = 3)

        # Schedule
        Label(self.edit_wind, text = 'Horario:').grid(row = 5, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[6]), state = 'readonly').grid(row = 5, column = 2)
        new_schedule= Entry(self.edit_wind)
        new_schedule.grid(row = 5, column = 3)

        # FDate
        Label(self.edit_wind, text = 'Fecha de Fin.:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[7]), state = 'readonly').grid(row = 6, column = 2)
        new_fdate= Entry(self.edit_wind)
        new_fdate.grid(row = 6, column = 3)

        # Category
        Label(self.edit_wind, text = 'Categoria:').grid(row = 7, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[8]), state = 'readonly').grid(row = 7, column = 2)
        new_category= Entry(self.edit_wind)
        new_category.grid(row = 7, column = 3)

        # Literal
        Label(self.edit_wind, text = 'Literal:').grid(row = 8, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_dates[9]), state = 'readonly').grid(row = 8, column = 2)
        new_literal= Entry(self.edit_wind)
        new_literal.grid(row = 8, column = 3)

        Button(self.edit_wind, text = 'ACTUALIZAR', command = lambda: self.edit_records(name, new_name.get(), new_ci.get(), new_profession.get(), new_career.get(), new_stuff.get(), new_schedule.get(), new_fdate.get(), new_category.get(), new_literal.get())).grid(row = 9, columnspan = 4, sticky = W + E)
        self.edit_wind.mainloop()

    def edit_records(self, name, new_name, new_ci, new_profession, new_career, new_stuff, new_schudule, new_fdate, new_category, new_literal):
        query = 'UPDATE tcontrato SET nombrecompleto = ?, cedidentidad = ?, profesion = ?, carrera = ?, materias = ?, horario = ?, fechafin = ?, categoria = ?, literal = ? WHERE nombrecompleto = ?'
        parameters = (new_name, new_ci, new_profession, new_career, new_stuff, new_schudule, new_fdate, new_category, new_literal, name)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_teacher()

# App
if __name__ == '__main__':
    window = Tk()
    application = Teacher(window)
    window.mainloop()