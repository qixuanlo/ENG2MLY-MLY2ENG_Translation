import sys
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtGui import QIcon
from transformers import MarianMTModel, MarianTokenizer

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.load_resources()

    def initUI(self):
        self.setWindowTitle('Malay - English Translator')
        self.setGeometry(100, 100, 400, 300)

        self.setWindowIcon(QIcon('final\icon\icon.png'))

        layout = QVBoxLayout()

        self.input_label = QLabel('Enter Sentence to translate:')
        layout.addWidget(self.input_label)

        self.input_text = QLineEdit(self)
        layout.addWidget(self.input_text)

        self.translate_button = QPushButton('Translate', self)
        self.translate_button.clicked.connect(self.translate)
        layout.addWidget(self.translate_button)

        self.output_label = QLabel('Translation:')
        layout.addWidget(self.output_label)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.model_label = QLabel('Select :')
        layout.addWidget(self.model_label)

        self.model_selector = QComboBox(self)
        self.model_selector.addItems(['Maly2Eng', 'Eng2Maly'])  # Add your model names here
        self.model_selector.currentIndexChanged.connect(self.load_resources)
        layout.addWidget(self.model_selector)

        self.setLayout(layout)

        self.model_labels = {
            'Maly2Eng': {
                'input': 'Enter Malay sentence: ',
                'output': 'English Translation: '
            },
            'Eng2Maly': {
                'input': 'Enter English sentence: ',
                'output': 'Malay Translation: '
            }
        }

    def load_resources(self):
        # 加载分词器和模型
        selected_model = self.model_selector.currentText()
        if selected_model == "Maly2Eng":
            self.tokenizer = MarianTokenizer.from_pretrained('final\Maly2EngTranslator')
            self.model = MarianMTModel.from_pretrained('final\Maly2EngTranslator')
            self.update_labels(selected_model)
        elif selected_model == "Eng2Maly":
            self.tokenizer = MarianTokenizer.from_pretrained('final\Eng2MalyTranslator')
            self.model = MarianMTModel.from_pretrained('final\Eng2MalyTranslator')
            self.update_labels(selected_model)

    def update_labels(self, model_name):
        self.input_label.setText(self.model_labels[model_name]['input'])
        self.output_label.setText(self.model_labels[model_name]['output'])

    def translate(self):
        # 获取输入句子
        input_sentence = self.input_text.text()
        if not input_sentence:
            self.output_text.setText("Please enter a sentence.")
            return
        
        # 预处理输入句子
        inputs = self.tokenizer(input_sentence, return_tensors="pt", padding=True, truncation=True, max_length=70)
        
        # 预测翻译
        translated = self.model.generate(**inputs)
        translated_sentence = [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        
        # 显示翻译结果
        self.output_text.setText(translated_sentence[0])

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec_())
