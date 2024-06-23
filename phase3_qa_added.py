import sys
import pandas as pd
import google.generativeai as genai
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
)
def main(path):
# 1. Data Loading and Gemini Setup (Same as before)
    df = pd.read_csv(path)
    genai.configure(api_key="AIzaSyBpfnRGgdqdWK63fmOu-18kk_Y160-tk4g")

    # Get available text-based model
    available_models = genai.list_models()
    text_models = [
        model
        for model in available_models
        if model.supported_generation_methods and "generateText" in model.supported_generation_methods
    ]
    if not text_models:
        raise ValueError("No suitable text models found.")
    model_name = text_models[0].name


    class ChatWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.chat_history = []

            self.chat_area = QTextEdit()
            self.chat_area.setReadOnly(True)

            self.input_box = QTextEdit()

            send_button = QPushButton("Send")
            send_button.clicked.connect(self.send_message)

            layout = QVBoxLayout()
            layout.addWidget(self.chat_area)
            layout.addWidget(self.input_box)
            layout.addWidget(send_button)

            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

            self.setWindowTitle("DATA ANALYZER Chat")
            self.setGeometry(100, 100, 400, 600)
            self.show()

        def send_message(self):
            user_question = self.input_box.toPlainText().strip()
            if not user_question:
                return

            self.chat_area.append(f"You: {user_question}")
            self.input_box.clear()


            # Gemini Interaction (with DataFrame Context)

            prompt_with_instructions = f'''
    You are an AI assistant helping users analyze a DataFrame they have given you. 
    Analyze the DataFrame clearly.
    Use the following information about the DataFrame to answer the user's questions:
    DataFrame Columns: {list(df.columns)}
    DataFrame Description: {df.describe().values.tolist()}
    DataFrame correlation matrix:{df.corr().values.tolist()}
    complete DataFrame:
    {df.to_string}
    
    Chat History:
    {'n'.join(str(item) for item in self.chat_history)}
    
    Current Question:
    {user_question}
    
    If the question requires calculations or analysis on the DataFrame, perform those calculations and provide the result.
    If the question is not related to the DataFrame, say "Question is outside the scope of the provided data."
    You have to give an answer based on the history and DataFrame
    You have to answer in comprehensive and informative way..
    '''

            try:
                response = genai.generate_text(
                    model=model_name,
                    prompt=prompt_with_instructions,
                )
                answer = response.result
                self.chat_history.append(user_question)
                self.chat_history.append(answer)
                self.chat_area.append(f"<span style='color: green;'>DATA ANALYZER : {answer}</span>")


            except genai.ApiException as e:
                self.chat_area.append(f"Error from Viswa: {e}")




    sap = QApplication(sys.argv)
    window = ChatWindow()
    sap.exec_()

