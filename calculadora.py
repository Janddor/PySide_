from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget,
                               QVBoxLayout, QLineEdit, QGridLayout,
                               QPushButton)


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculadora')
        self.setFixedSize(235,235)
        self.componente_general = QWidget()
        self.setCentralWidget(self.componente_general)
        # Crear un layout principal
        self.layout_principal = QVBoxLayout()
        self.componente_general.setLayout(self.layout_principal)
        # Métodos para crear la parte visual de la calculadora
        self._crear_area_captura()
        # Agregar los botones
        self._crear_botones()
        # Conectar las señales con los slots
        self._conectar_botones()


    def _crear_area_captura(self):
        self.linea_entrada = QLineEdit()
        # Propiedades de QLineEdit
        self.linea_entrada.setFixedHeight(35)
        self.linea_entrada.setAlignment(Qt.AlignRight)
        self.linea_entrada.setReadOnly(True)
        self.layout_principal.addWidget(self.linea_entrada)

    def  _crear_botones(self):
        # Los crearemos con un diccionario (texto : posicion)
        self.botones = {}
        layout_botones = QGridLayout()
        # Texto | Posición en el grid layout
        self.botones = {
            '7' : (0, 0),'8' : (0, 1),'9' : (0, 2),'/' : (0, 3),
            '4' : (1, 0),'5' : (1, 1),'6' : (1, 2),'*' : (1, 3),
            '1' : (2, 0),'2' : (2, 1),'3' : (2, 2),'-' : (2, 3),
            '0' : (3, 0),'.' : (3, 1),'C' : (3, 2),'+' : (3, 3),'=' : (3, 4)
        }

        # Crear los botones y se agregan al grid layout
        # La posición es una tupla de dos valores (row-column)
        for texto_boton, posicion in self.botones.items():
            self.botones[texto_boton] = QPushButton(texto_boton)
            self.botones[texto_boton].setFixedSize(40, 40)
            # Publicar el boton en el grid layout
            layout_botones.addWidget(self.botones[texto_boton], posicion[0], posicion[1])
        # Agregar el layout de botones al layout principal
        self.layout_principal.addLayout(layout_botones)

    def _conectar_botones(self):
        # Recorrer cada botón del diccionario (key:value) (texto:PushButton)
        for texto_boton, boton in self.botones.items():
            if texto_boton not in {'=', 'C'}:
                # boton.clicked.connect(lambda: self._construir_expresion(texto_boton)) # no funca
                boton.clicked.connect(partial(self._construir_expresion, texto_boton))
            # Conectar el boton limpiar texto
            self.botones['C'].clicked.connect(self._limpiar_linea_entrada)
            # Conectar el botón de igual (=)
            self.botones['='].clicked.connect(self._calcular_resultado)
            self.linea_entrada.returnPressed.connect(self._calcular_resultado)


    def _construir_expresion(self, texto_boton):
        expresion = self.obtener_texto() + texto_boton
        # Actualizar la expresión
        self.actualizar_texto(expresion)

    def obtener_texto(self):
        return self.linea_entrada.text()

    def actualizar_texto(self, texto):
        self.linea_entrada.setText(texto)
        self.linea_entrada.setFocus()

    def _limpiar_linea_entrada(self):
        self.actualizar_texto('')

    def _calcular_resultado(self):
        resultado = self._evaluar_expresion(self.obtener_texto())
        self.actualizar_texto(resultado)

    def _evaluar_expresion(self, expresion):
        try:
            # Utilizar eval para evaluar expresion str
            resultado = str(eval(expresion))
        except Exception as e:
            resultado = f'Ocurrió un error'
        return resultado

if __name__ == '__main__':
    app = QApplication()
    calculadora = Calculadora()
    calculadora.show()
    app.exec()