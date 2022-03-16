import sys
import os
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from pathlib import *
from pathlib import Path

from PySide6 import QtCore

from PySide6.QtCore import *
from PySide6.QtCore import Qt , QModelIndex, QAbstractTableModel, QItemSelectionModel
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QTableWidgetItem

from PySide6.QtUiTools import QUiLoader

from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QMainWindow
from sqlite3 import *
from sqlite3 import connect
import sqlite3

 
class Registro_datos():

    def __init__(self):
        # Conectar la Base de Datos
        self.conn = sqlite3.connect('BD.db')

    #Select a la Tabla libreria    
    def buscar_libros(self):#Devuelve TODOS los datos de la tabla libreria
        self.conn = sqlite3.connect('BD.db')
        cursor = self.conn.cursor()
        sql = "SELECT * FROM libreria " 
        cursor.execute(sql)
        registro = cursor.fetchall() #Llamar a una única fila que coincide
        return registro

	#Select con Where a la Tabla libreria
    #Búsqueda según el título 
    def busca_libro(self, titulo_libro):
        cur = self.conn.cursor()
        sql = "SELECT * FROM libreria WHERE TITULO = {}".format(titulo_libro) #En esa posicion
        cur.execute(sql)
        tituloX = cur.fetchall() #Llamar a una única fila que coincide
        cur.close()     
        return tituloX


	#Delete a la Tabla libreria
    def elimina_libros(self,TITULO):
        cur = self.conn.cursor()
        sql='''DELETE FROM libreria WHERE TITULO = {}'''.format(TITULO) #En esa posicion
        cur.execute(sql)
        a = cur.rowcount #Obtener el número total de filas modificadas por una consulta (1 si ha borrado/ 0 si no ha borrado)
        self.conn.commit()    
        cur.close()
        return a


class Registro_datos2():
	def __init__(self):
		self.conn = sqlite3.connect('BD.db')

	#Insert a la Tabla libreria 
	def anadir_libro(self, TITULO, AUTOR, GENERO, EDITORIAL, PAGINAS, PRECIO, LEIDO):
		self.conn = sqlite3.connect('BD.db')
		cur = self.conn.cursor()
		sql='''INSERT INTO libreria (TITULO, AUTOR, GENERO, EDITORIAL, PAGINAS, PRECIO, LEIDO) 
    	VALUES('{}', '{}','{}', '{}','{}','{}','{}')'''.format(TITULO, AUTOR, GENERO, EDITORIAL, PAGINAS, PRECIO, LEIDO) #En esa posicion
		cur.execute(sql)
		self.conn.commit()    
		cur.close()


class Registro_datos3():
	def __init__(self):
		self.conn = sqlite3.connect('BD.db')

#Update a la Tabla libreria
	def actualiza_libros(self, TITULOA, AUTORA, GENEROA, EDITORIALA, PAGINASA, PRECIOA, LEIDOA, TITULOID):
		cur = self.conn.cursor()
		sql ='''UPDATE libreria SET TITULO = '{}', AUTOR = '{}', GENERO = '{}', EDITORIAL = '{}', PAGINAS = '{}', PRECIO = '{}', LEIDO = '{}'
		WHERE TITULO = '{}' '''.format(TITULOA, AUTORA, GENEROA, EDITORIALA, PAGINASA, PRECIOA, LEIDOA, TITULOID) #En esa posicion
		cur.execute(sql)
		a = cur.rowcount #Obtener el número total de filas modificadas por una consulta (1 si ha borrado/ 0 si no ha borrado)
		self.conn.commit()    
		cur.close()
		return a  

	def busca_libroA(self, titulo_libro):
		self.conn = sqlite3.connect('BD.db')
		cur = self.conn.cursor()
		sql = "SELECT * FROM libreria WHERE TITULO = {}".format(titulo_libro) #En esa posicion
		cur.execute(sql)
		tituloX = cur.fetchall() #Llamar a una única fila que coincide
		cur.close()     
		return tituloX
		

class MiApp(QtWidgets.QMainWindow,QtCore.QObject):
	def __init__(self):
		super().__init__()
		self.datosTotal = Registro_datos() #Class SQL LIBROS - BUSCADOR - BORRAR
		self.datosTotal2 = Registro_datos2() #Class SQL AÑADIR 
		self.datosTotal3 = Registro_datos3() #Class ACTUALIZAR
		loader = QUiLoader()
		current_dir = os.path.abspath(os.path.dirname(__file__))
		parent_dir = os.path.abspath(current_dir + "/../")
		os.chdir(os.path.join(parent_dir, "libreria"))
		self.ui = loader.load("GUI.ui", None)
		self.ui.show()
		self.ui.bt_cargar.clicked.connect(self.m_libros)#mostrar libros
		self.ui.bt_buscar.clicked.connect(self.buscar_libro)#buscar libro
		self.ui.bt_anadir.clicked.connect(self.anadir_libro)#Añade libro
		self.ui.bt_actualizar.clicked.connect(self.modificar_libros)#Actualiza libro
		self.ui.bt_borrar.clicked.connect(self.eliminar_libro)# Borra libro


	def m_libros(self):	#LIBROS 
		datos = self.datosTotal.buscar_libros()
		i = len(datos)

		self.ui.tabla_libros.setRowCount(i)
		tablerow = 0
		for row in datos:
			self.ui.tabla_libros.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[1]))
			self.ui.tabla_libros.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[2]))
			self.ui.tabla_libros.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[3]))
			self.ui.tabla_libros.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[4]))
			self.ui.tabla_libros.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[5])))
			self.ui.tabla_libros.setItem(tablerow,5,QtWidgets.QTableWidgetItem(str(row[6])))
			self.ui.tabla_libros.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[7]))
			
			tablerow +=1


	def buscar_libro(self): # BUSCADOR  
		titulo_libro = self.ui.tituloB.text()
		titulo_libro = str("'" + titulo_libro + "'")

		datosB = self.datosTotal.busca_libro(titulo_libro)
		i = len(datosB)

		self.ui.tabla_buscar.setRowCount(i)
		tablerow = 0
		for row in datosB:
			self.ui.tabla_buscar.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[1]))
			self.ui.tabla_buscar.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[2]))
			self.ui.tabla_buscar.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[3]))
			self.ui.tabla_buscar.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[4]))
			self.ui.tabla_buscar.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[5])))
			self.ui.tabla_buscar.setItem(tablerow,5,QtWidgets.QTableWidgetItem(str(row[6])))
			self.ui.tabla_buscar.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[7]))
			tablerow +=1


	def eliminar_libro(self): #BORRAR
		eliminar = self.ui.titulo_a_borrar.text()
		eliminar = str("'"+ eliminar + "'")

		self.datosTotal.elimina_libros(eliminar)
		datos = self.datosTotal.buscar_libros()
		i = len(datos)

		self.ui.tabla_borrar.setRowCount(i)
		tablerow = 0
		for row in datos:
			self.ui.tabla_borrar.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[1]))
			self.ui.tabla_borrar.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[2]))
			self.ui.tabla_borrar.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[3]))
			self.ui.tabla_borrar.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[4]))
			self.ui.tabla_borrar.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(row[5])))
			self.ui.tabla_borrar.setItem(tablerow,5,QtWidgets.QTableWidgetItem(str(row[6])))
			self.ui.tabla_borrar.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[7]))
			tablerow +=1


	def anadir_libro(self): #AÑADIR
		titulo = self.ui.tituloA.text() 
		autor = self.ui.autorA.text()
		genero = self.ui.generoA.text()
		editorial = self.ui.editorialA.text()
		paginas = self.ui.paginasA.text()
		precio = self.ui.precioA.text()
		leido = self.ui.leidoA.text()


		self.datosTotal2.anadir_libro(titulo, autor, genero, editorial, paginas, precio, leido)
		self.ui.tituloA.clear()
		self.ui.autorA.clear()
		self.ui.generoA.clear()
		self.ui.editorialA.clear()
		self.ui.paginasA.clear()
		self.ui.precioA.clear()
		self.ui.leidoA.clear()


	def modificar_libros(self):
		titulo_a_actualizar = self.ui.titulo_a_actualizar.text() 
		titulo_a_actualizar = str("'" + titulo_a_actualizar + "'")
		tituloXX = self.datosTotal3.busca_libroA(titulo_a_actualizar)

		if tituloXX != None: #Si no está vacío actualiza los datos 

			tituloM = self.ui.titulo_actualizar.text() 
			autorM = self.ui.autor_actualizar.text()
			generoM = self.ui.genero_actualizar.text()
			editorialM = self.ui.editorial_actualizar.text()
			paginasM = self.ui.paginas_actualizar.text()
			precioM = self.ui.precio_actualizar.text()
			leidoM = self.ui.leido_actualizar.text()
			tituloid = self.ui.titulo_a_actualizar.text()

			act = self.datosTotal3.actualiza_libros(tituloM, autorM, generoM, editorialM, paginasM, precioM, leidoM, tituloid)

			if act == 1: #Borrar el texto metido anteriormente
				self.ui.titulo_actualizar.clear()
				self.ui.autor_actualizar.clear()
				self.ui.genero_actualizar.clear()
				self.ui.editorial_actualizar.clear()
				self.ui.paginas_actualizar.clear()
				self.ui.precio_actualizar.clear()
				self.ui.leido_actualizar.clear()
				self.ui.titulo_a_actualizar.clear()
				
		else: #Vacío
			pass
	
		

	
#BAR CVRPR JN, WVGFHMNV FHEH!!!

appp = QtWidgets.QApplication(sys.argv)
window = MiApp()
appp.exec()




