import pandas as pd
from tkinter import Toplevel, Scrollbar, Frame
from tkinter import ttk
from customtkinter import *

# Function to calculate the percentage of outliers in a specific column
def outliers_percentage(df, column):
    if column not in df.columns:
        return "NA"

    if not pd.api.types.is_numeric_dtype(df[column]):
        return "NA"

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outlier_count = df[(df[column] < lower_bound) | (df[column] > upper_bound)].shape[0]
    total_count = df.shape[0]
    outlier_percentage = (outlier_count / total_count) * 100

    return str(round(outlier_percentage)) + " %"

# Function to perform analysis and return output DataFrame
def ds(app, path):
    df = pd.read_csv(path, sep=',')

    def perform_analysis(option):
        try:
            if option == 1:
                rows = []

                # Descriptive statistics to calculate
                descriptive_stats = ["Mean", "Median", "Std", "Mode", "Null Values", "Outliers Percentage"]
                for stat in descriptive_stats:
                    row = {"Descriptive Stats": stat}
                    for col in df.columns:
                        try:
                            if pd.api.types.is_numeric_dtype(df[col]):
                                if stat == "Mean":
                                    row[col] = df[col].mean()
                                elif stat == "Median":
                                    row[col] = df[col].median()
                                elif stat == "Std":
                                    row[col] = df[col].std()
                                elif stat == "Mode":
                                    row[col] = df[col].mode()[0] if not df[col].mode().empty else "NA"
                                elif stat == "Null Values":
                                    row[col] = df[col].isnull().sum()
                                else:
                                    row[col] = outliers_percentage(df, col)
                            else:
                                if stat == "Mode":
                                    row[col] = df[col].mode()[0] if not df[col].mode().empty else "NA"
                                elif stat == "Null Values":
                                    row[col] = df[col].isnull().sum()
                                else:
                                    row[col] = "NA"  # Skip non-numeric statistics for categorical variables
                        except ValueError as e:
                            row[col] = "NA"  # Handle ValueError gracefully
                            print(f"Error processing column '{col}': {e}")

                    rows.append(row)

                # Combine rows into a DataFrame
                output_df = pd.concat([pd.DataFrame([row]) for row in rows], ignore_index=True)

                # Transpose the DataFrame
                output_df = output_df.set_index("Descriptive Stats").transpose().reset_index().rename(
                    columns={'index': 'Variables'})

            else:
                output_df = df.corr()

                # Add the first column with column names
                output_df.insert(0, "Variables", output_df.columns)

            return output_df

        except Exception as e:
            print(f"Error in perform_analysis function: {e}")
            return None

    def show_best_correlated():
        corr_matrix = df.corr()
        data = []
        for col in corr_matrix.columns:
            for idx in corr_matrix.index:
                if idx != col and abs(corr_matrix.loc[idx, col]) >= 0.3:
                    if [col, idx, corr_matrix.loc[col, idx]] not in data:
                      data.append([idx, col, corr_matrix.loc[idx, col]])

        popup = Toplevel()
        popup.title("Best Correlated Variables")
        popup.geometry("600x400")

        frame = Frame(popup)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("Variable 1", "Variable 2", "Correlation"), show="headings")
        tree.pack(side="left", fill="both", expand=True)

        yscrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
        yscrollbar.pack(side="right", fill="y")
        tree.config(yscrollcommand=yscrollbar.set)

        xscrollbar = Scrollbar(frame, orient="horizontal", command=tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        tree.config(xscrollcommand=xscrollbar.set)

        tree.heading("Variable 1", text="Variable 1")
        tree.heading("Variable 2", text="Variable 2")
        tree.heading("Correlation", text="Correlation Value")

        for row in data:
            tree.insert("", "end", values=row)

    def show_output(option):
        output_df = perform_analysis(option)

        popup = Toplevel()
        if option == 1:
            popup.title("Descriptive Statistics")
        else:
            popup.title("Correlation Matrix")
        popup.geometry("800x600")

        frame = Frame(popup)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=output_df.columns.tolist(), show="headings")
        tree.pack(side="left", fill="both", expand=True)

        yscrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
        yscrollbar.pack(side="right", fill="y")
        tree.config(yscrollcommand=yscrollbar.set)

        xscrollbar = Scrollbar(frame, orient="horizontal", command=tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        tree.config(xscrollcommand=xscrollbar.set)

        for col in output_df.columns.tolist():
            tree.heading(col, text=col)

        for index, row in output_df.iterrows():
            tree.insert("", "end", values=row.tolist())

    global general_button
    global correlation_button
    global best_correlated_button
    general_button = CTkButton(master=app, text="General", width=20, corner_radius=10, cursor="hand2", bg_color="#c5c8e2",
                               command=lambda: show_output(1))
    general_button.place(x=550, y=250)

    correlation_button = CTkButton(master=app, text="Correlation Matrix", width=20, corner_radius=10, cursor="hand2", bg_color="#c5c8e2",
                                   command=lambda: show_output(2))
    correlation_button.place(x=530, y=280)

    best_correlated_button = CTkButton(master=app, text="Best Correlated Variables", width=30, corner_radius=10, bg_color="#c5c8e2",
                                       cursor="hand2", command=show_best_correlated)
    best_correlated_button.place(x=510, y=310)

def dest():
    global general_button
    global correlation_button
    global best_correlated_button
    general_button.destroy()
    correlation_button.destroy()
    best_correlated_button.destroy()