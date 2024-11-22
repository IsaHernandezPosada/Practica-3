# CFG Derivation Tool

## Descripción

*CFG Derivation Tool* es una aplicación interactiva para trabajar con gramáticas libres de contexto (CFG, por sus siglas en inglés). Permite a los usuarios:

- Cargar una gramática en formato similar a BNF.
- Derivar expresiones siguiendo la gramática especificada.
- Generar y visualizar árboles de derivación y árboles de sintaxis abstracta (AST).
- Realizar derivaciones de forma visual con animaciones de los nodos del árbol.

La interfaz está construida utilizando *PyQt5* y la lógica del análisis de gramáticas se basa en *NLTK*.

## Características principales

- *Entrada de gramática*: Introduce la gramática manualmente o cárgala desde un archivo.
- *Derivación de expresiones*: Deriva expresiones a partir de la gramática especificada.
- *Visualización del árbol*: Representación gráfica y animada de los árboles de derivación o AST.
- *Interfaz amigable*: Controles intuitivos para personalizar y generar derivaciones.

## Requisitos

- *Python 3.8+*
- Librerías necesarias (instalar con pip):
  - nltk
  - PyQt5

## Instalación

1. Clona este repositorio o descarga los archivos:
   bash
   git clone <URL del repositorio>
   cd <directorio>
   

2. Instala las dependencias:
   bash
   pip install -r requirements.txt
   

3. Asegúrate de que *NLTK* esté configurado correctamente. Si es la primera vez que lo usas:
   python
   import nltk
   nltk.download('punkt')
   

## Uso

1. Ejecuta la aplicación:
   bash
   python <nombre_del_archivo>.py
   

2. Carga o escribe una gramática en formato similar a BNF. Ejemplo:
   
   S -> 'a' S 'b' | 'c'
   

3. Introduce una expresión de entrada (tokens separados por espacios). Ejemplo:
   
   a c b
   

4. Haz clic en:
   - *Generate Derivation* para generar el árbol de derivación.
   - *Generate AST* para generar el árbol de sintaxis abstracta.

5. Visualiza el árbol derivado en la pantalla principal.

## Controles rápidos

- *Botones de símbolos*: Inserta rápidamente símbolos comunes en la gramática.
- *Cargar gramática: Utiliza el botón *Load Grammar from File para cargar una gramática desde un archivo de texto.
- *Opciones de derivación*: Selecciona entre derivación por la izquierda o por la derecha.

## Estructura del código

- CFGDerivationTool: Lógica principal para manejar gramáticas y derivaciones.
- CFGDerivationToolGUI: Interfaz gráfica y manejo de eventos.
- Métodos clave:
  - load_grammar: Carga la gramática desde un texto.
  - construct_derivation_tree: Genera el árbol de derivación.
  - convert_to_ast: Convierte un árbol de derivación en un AST.
  - display_tree: Dibuja y anima el árbol derivado.

## Ejemplo de gramática y derivación

### Gramática

S -> 'a' S 'b' | 'c'


### Entrada

a c b


### Salida esperada
Un árbol de derivación con S como raíz, derivando los tokens de la entrada según las reglas especificadas.

## Problemas conocidos

- La gramática debe estar bien formada; un error en su formato puede generar excepciones.
- Las expresiones que no coincidan con la gramática no podrán ser derivadas.

