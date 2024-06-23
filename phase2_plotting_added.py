import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QRadioButton, QScrollArea, QGridLayout, QLabel, QButtonGroup, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
def main(path):
# Sample dataset
    df = pd.read_csv(path)

    # Function to calculate correlation matrix and identify columns
    def calculate_correlation_matrix(dataframe):
        corr_matrix = dataframe.corr()
        categorical_cols = dataframe.select_dtypes(include=['object', 'category']).columns.tolist()
        continuous_cols = dataframe.select_dtypes(include=['number']).columns.tolist()
        return corr_matrix, categorical_cols, continuous_cols

    # Function to get correlated pairs based on threshold
    def get_correlated_pairs(corr_matrix, threshold=0.29):
        correlated_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) >= threshold:
                    correlated_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j]))
        return correlated_pairs

    # Create correlation matrix and identify columns
    correlation_matrix, categorical_cols, continuous_cols = calculate_correlation_matrix(df)

    # Get correlated pairs with threshold 0.1
    correlated_pairs = get_correlated_pairs(correlation_matrix)


    class PlotWindow(QMainWindow):
        def __init__(self, plot_method):
            super().__init__()
            self.setWindowTitle("Correlation Plots")
            self.setGeometry(100, 100, 1200, 800)

            main_layout = QVBoxLayout()
            self.setCentralWidget(QWidget())

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            plot_widget = QWidget()
            scroll_area.setWidget(plot_widget)

            plot_layout = QVBoxLayout()
            plot_widget.setLayout(plot_layout)

            main_layout.addWidget(scroll_area)
            self.centralWidget().setLayout(main_layout)

            self.create_plots(plot_layout, plot_method)

        def create_plots(self, layout, plot_method):
            for idx, (col1, col2) in enumerate(correlated_pairs, start=1):
                fig = Figure(figsize=(3.75, 3.75))  # Adjusted for 300x300 pixels at 80 DPI
                ax = fig.add_subplot(111)

                if plot_method == 'scatter':
                    ax.scatter(df[col1], df[col2])
                    ax.set_title(f'Scatter Plot: {col1} vs {col2}')
                elif plot_method == 'line':
                    ax.plot(df[col1], df[col2], marker='o')
                    ax.set_title(f'Line Plot: {col1} vs {col2}')
                elif plot_method == 'histogram':
                    ax.hist2d(df[col1], df[col2], bins=30)
                    ax.set_title(f'2D Histogram: {col1} vs {col2}')
                elif plot_method == 'bar':
                    categories = df[col1].unique() if col1 in categorical_cols else df[col2].unique()
                    means = df.groupby(col1)[col2].mean() if col1 in categorical_cols else df.groupby(col2)[col1].mean()
                    ax.bar(categories, means)
                    ax.set_title(f'Bar Plot: {col1} vs {col2}')
                elif plot_method == 'box':
                    df.boxplot(column=col2, by=col1, ax=ax)
                    ax.set_title(f'Box Plot: {col1} vs {col2}')
                    fig.suptitle('')
                elif plot_method == 'violin':
                    sns.violinplot(x=col1, y=col2, data=df, ax=ax)
                    ax.set_title(f'Violin Plot: {col1} vs {col2}')
                elif plot_method == 'heatmap':
                    sns.heatmap(df[[col1, col2]].corr(), annot=True, ax=ax)
                    ax.set_title(f'Heatmap: {col1} vs {col2}')

                ax.set_xlabel(col1)
                ax.set_ylabel(col2)
                fig.tight_layout()

                canvas = FigureCanvas(fig)
                canvas.setMinimumSize(300, 300)  # Set minimum size for each plot
                layout.addWidget(canvas)


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Correlation Plotter")
            self.setGeometry(100, 100, 300, 200)

            layout = QVBoxLayout()

            label = QLabel("Select Plot Method:")
            layout.addWidget(label)

            self.plot_method_group = QButtonGroup()
            plot_methods = ["scatter", "line", "histogram", "bar", "box", "violin", "heatmap"]

            for method in plot_methods:
                radio_button = QRadioButton(method.capitalize())
                self.plot_method_group.addButton(radio_button)
                layout.addWidget(radio_button)

            button = QPushButton("Show Plot")
            button.clicked.connect(self.show_plot)
            layout.addWidget(button)

            container = QWidget()
            container.setLayout(layout)

            self.setCentralWidget(container)

        def show_plot(self):
            selected_button = self.plot_method_group.checkedButton()
            if not selected_button:
                QMessageBox.warning(self, "Warning", "Please select a plot method.")
                return

            selected_plot_method = selected_button.text().lower()
            self.plot_window = PlotWindow(selected_plot_method)
            self.plot_window.show()


    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
