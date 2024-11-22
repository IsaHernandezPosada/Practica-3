import sys
import random
import nltk
from nltk import CFG
from nltk.tree import Tree

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLineEdit, QLabel, QRadioButton, QGraphicsView,
    QGraphicsScene, QFileDialog, QGroupBox, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QTextCursor
from PyQt5.QtCore import Qt, QTimer, QPointF


class CFGDerivationTool:
    def _init_(self, grammar_text):
        """Initialize with a grammar in string format."""
        self.grammar_text = grammar_text
        self.grammar = None
        self.parser = None
        if grammar_text.strip():
            self.load_grammar(grammar_text)

    def load_grammar(self, grammar_text):
        """Load and parse the grammar from a string."""
        self.grammar_text = grammar_text
        self.grammar = CFG.fromstring(grammar_text)
        self.parser = nltk.ChartParser(self.grammar)

    def parse_expression(self, tokens):
        """Parse the given tokens to ensure they match the grammar."""
        if not self.parser:
            raise ValueError("Grammar is not defined.")
        try:
            parse_tree = next(self.parser.parse(tokens))
            return parse_tree
        except StopIteration:
            raise ValueError("Expression could not be parsed with the given grammar.")

    def construct_derivation_tree(self, tokens):
        """Construct the derivation tree for the given tokens."""
        return self.parse_expression(tokens)

    def convert_to_ast(self, derivation_tree):
        """Convert a derivation tree to an abstract syntax tree (AST)."""
        def simplify_tree(tree):
            if isinstance(tree, str):
                return tree
            if len(tree) == 1 and isinstance(tree[0], str):
                return tree[0]
            return Tree(tree.label(), [simplify_tree(child) for child in tree])
        return simplify_tree(derivation_tree)


class CFGDerivationToolGUI(QWidget):
    def _init_(self):
        super()._init_()
        self.cfg_tool = CFGDerivationTool("")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('CFG Derivation Tool')
        self.resize(1000, 800)

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Grammar input area
        grammar_layout = QVBoxLayout()
        main_layout.addLayout(grammar_layout, stretch=1)
        self.setup_grammar_input(grammar_layout)

        # Expression input area
        expression_layout = QHBoxLayout()
        main_layout.addLayout(expression_layout, stretch=0)
        self.setup_expression_input(expression_layout)

        # Derivation options and buttons
        derivation_layout = QHBoxLayout()
        main_layout.addLayout(derivation_layout, stretch=0)
        self.setup_derivation_options(derivation_layout)

        # Display area for the tree
        display_layout = QVBoxLayout()
        main_layout.addLayout(display_layout, stretch=4)
        self.setup_display_area(display_layout)

    def setup_grammar_input(self, layout):
        """Set up the grammar input area with label, text edit, and buttons."""
        controls_layout = QHBoxLayout()
        layout.addLayout(controls_layout)

        grammar_label = QLabel('Grammar (BNF-like format):')
        controls_layout.addWidget(grammar_label)

        load_grammar_button = QPushButton('Load Grammar from File')
        load_grammar_button.clicked.connect(self.load_grammar_from_file)
        controls_layout.addWidget(load_grammar_button)

        self.grammar_text_edit = QTextEdit()
        self.grammar_text_edit.setMaximumHeight(150)
        self.grammar_text_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(self.grammar_text_edit)

        # Quick-insert buttons for common grammar symbols
        symbols_layout = QHBoxLayout()
        layout.addLayout(symbols_layout)
        self.add_symbol_buttons(symbols_layout)

    def add_symbol_buttons(self, layout):
        """Add quick-insert buttons for common grammar symbols."""
        symbols = ['S', 'A', 'B', 'C', '->', '|', "''", "'a'", "'b'", "'c'"]
        for symbol in symbols:
            button = QPushButton(symbol)
            button.clicked.connect(lambda checked, s=symbol: self.insert_symbol(s))
            layout.addWidget(button)

    def insert_symbol(self, symbol):
        """Insert a symbol into the grammar text edit at the cursor position."""
        cursor = self.grammar_text_edit.textCursor()
        cursor.insertText(symbol + ' ')
        self.grammar_text_edit.setTextCursor(cursor)
        self.grammar_text_edit.setFocus()

    def load_grammar_from_file(self):
        """Load grammar from a file and display it in the text edit."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Grammar File", "", "Text Files (.txt);;All Files ()", options=options
        )
        if filename:
            with open(filename, 'r') as file:
                grammar_text = file.read()
                self.grammar_text_edit.setText(grammar_text)

    def setup_expression_input(self, layout):
        """Set up the expression input area with label and input field."""
        expression_label = QLabel('Expression to derive (tokens separated by spaces):')
        layout.addWidget(expression_label)

        self.expression_input = QLineEdit()
        layout.addWidget(self.expression_input)

    def setup_derivation_options(self, layout):
        """Set up derivation type options and action buttons."""
        derivation_group = QGroupBox("Derivation Type")
        derivation_options_layout = QHBoxLayout()
        derivation_group.setLayout(derivation_options_layout)
        layout.addWidget(derivation_group)

        self.left_derivation_radio = QRadioButton("Left Derivation")
        self.left_derivation_radio.setChecked(True)
        derivation_options_layout.addWidget(self.left_derivation_radio)

        self.right_derivation_radio = QRadioButton("Right Derivation")
        derivation_options_layout.addWidget(self.right_derivation_radio)

        generate_derivation_button = QPushButton('Generate Derivation')
        generate_derivation_button.clicked.connect(self.generate_derivation)
        layout.addWidget(generate_derivation_button)

        generate_ast_button = QPushButton('Generate AST')
        generate_ast_button.clicked.connect(self.generate_ast)
        layout.addWidget(generate_ast_button)

    def setup_display_area(self, layout):
        """Set up the display area for the derivation tree."""
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.graphics_view)

    def generate_derivation(self):
        """Generate and display the derivation tree."""
        grammar_text = self.grammar_text_edit.toPlainText()
        expression = self.expression_input.text().split()

        if not grammar_text.strip():
            self.show_error("Please input a grammar.")
            return

        if not expression:
            self.show_error("Please input an expression to derive.")
            return

        try:
            self.cfg_tool.load_grammar(grammar_text)
        except ValueError as error:
            self.show_error(f"Error in grammar:\n{error}")
            return

        try:
            derivation_tree = self.cfg_tool.construct_derivation_tree(expression)
            self.display_tree(derivation_tree)
        except ValueError as error:
            self.show_error(str(error))

    def generate_ast(self):
        """Generate and display the abstract syntax tree (AST)."""
        grammar_text = self.grammar_text_edit.toPlainText()
        expression = self.expression_input.text().split()

        if not grammar_text.strip():
            self.show_error("Please input a grammar.")
            return

        if not expression:
            self.show_error("Please input an expression to derive.")
            return

        try:
            self.cfg_tool.load_grammar(grammar_text)
        except ValueError as error:
            self.show_error(f"Error in grammar:\n{error}")
            return

        try:
            derivation_tree = self.cfg_tool.construct_derivation_tree(expression)
            ast_tree = self.cfg_tool.convert_to_ast(derivation_tree)
            self.display_tree(ast_tree)
        except ValueError as error:
            self.show_error(str(error))

    def display_tree(self, tree):
        """Display the given tree with animation."""
        self.graphics_scene.clear()
        self.node_items = []
        self.edge_items = []
        self.node_colors = {}
        self.collect_tree_nodes(tree)
        self.current_node_index = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.draw_next_node)
        self.animation_timer.start(500)
        self.graphics_view.fitInView(self.graphics_scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def collect_tree_nodes(self, tree, position=QPointF(0, 0), level=0, parent_position=None):
        """Recursively collect nodes and edges from the tree for drawing."""
        if isinstance(tree, str):
            self.node_items.append((tree, position, level))
            if parent_position is not None:
                self.edge_items.append((parent_position, position))
        else:
            self.node_items.append((tree.label(), position, level))
            if parent_position is not None:
                self.edge_items.append((parent_position, position))
            num_children = len(tree)
            x_offset = -75 * (num_children - 1)
            for i, child in enumerate(tree):
                child_position = QPointF(position.x() + x_offset + i * 150, position.y() + 150)
                self.collect_tree_nodes(child, child_position, level + 1, position)

    def draw_next_node(self):
        """Draw the next node and edge in the animation sequence."""
        if self.current_node_index >= len(self.node_items):
            self.animation_timer.stop()
            return

        label, position, level = self.node_items[self.current_node_index]
        self.draw_node(label, position)

        if self.current_node_index < len(self.edge_items):
            parent_position, child_position = self.edge_items[self.current_node_index]
            self.draw_edge(parent_position, child_position)

        self.current_node_index += 1

    def draw_node(self, label, position):
        """Draw a node with the given label at the specified position."""
        color = self.get_node_color(label)
        ellipse = self.graphics_scene.addEllipse(
            position.x(), position.y(), 40, 40, QPen(Qt.black), color
        )
        text = self.graphics_scene.addText(label)
        text.setPos(position.x() + 10, position.y() + 10)
        font = QFont()
        font.setPointSize(12)
        text.setFont(font)

    def get_node_color(self, label):
        """Get or assign a color for a node label."""
        if label in self.node_colors:
            return self.node_colors[label]
        else:
            colors = [
                QColor(255, 179, 186), QColor(255, 223, 186), QColor(255, 255, 186),
                QColor(186, 255, 201), QColor(186, 225, 255), QColor(219, 186, 255),
                QColor(255, 186, 248), QColor(255, 204, 229), QColor(204, 255, 229),
                QColor(255, 255, 204),
            ]
            color = random.choice(colors)
            self.node_colors[label] = color
            return color

    def draw_edge(self, start_position, end_position):
        """Draw an edge between two nodes."""
        self.graphics_scene.addLine(
            start_position.x() + 20, start_position.y() + 20,
            end_position.x() + 20, end_position.y() + 20, QPen(Qt.black)
        )

    def show_error(self, message):
        """Display an error message in a message box."""
        QMessageBox.critical(self, "Error", message)


if _name_ == '_main_':
    app = QApplication(sys.argv)
    window = CFGDerivationToolGUI()
    window.show()
    sys.exit(app.exec_())
