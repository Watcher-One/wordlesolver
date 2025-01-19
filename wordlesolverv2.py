import tkinter as tk

class WordleSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Solver")

        # Wczytanie bazy słów z pliku
        self.words = self.load_words("F:/pythonprojektwordle/slowa.txt")
        
        # Wczytanie częstości liter z pliku
        self.letter_frequencies = self.load_letter_frequencies("F:/pythonprojektwordle/procenty.txt")

        # Wprowadzenie liter do 5 okienek
        self.entries = []
        for i in range(5):
            entry = tk.Entry(self.root, width=2, font=('Arial', 24), justify='center', validate='key', validatecommand=(root.register(self.validate_input), "%P"))
            entry.grid(row=0, column=i, padx=5, pady=10)
            self.entries.append(entry)

        # Label z informacją o wykluczonych literach
        self.exclude_label = tk.Label(self.root, text="Excluded letters:", font=('Arial', 14))
        self.exclude_label.grid(row=1, column=0, columnspan=5, pady=5)

        # Okno tekstowe do wpisania wykluczonych liter
        self.exclude_entry = tk.Entry(self.root, font=('Arial', 14), width=20)
        self.exclude_entry.grid(row=2, column=0, columnspan=5, pady=5)

        # Label z informacją o literach żółtych
        self.yellow_label = tk.Label(self.root, text="Yellow letters (known, but not in position):", font=('Arial', 14))
        self.yellow_label.grid(row=3, column=0, columnspan=5, pady=5)

        # Okno tekstowe do wpisania liter żółtych
        self.yellow_entry = tk.Entry(self.root, font=('Arial', 14), width=20)
        self.yellow_entry.grid(row=4, column=0, columnspan=5, pady=5)

        # Przycisk do zapisania stanu
        self.submit_button = tk.Button(self.root, text="Submit", font=('Arial', 14), command=self.submit_data)
        self.submit_button.grid(row=5, column=0, columnspan=5, pady=20)

        # Label do wyników
        self.results_label = tk.Label(self.root, text="Possible words:", font=('Arial', 14))
        self.results_label.grid(row=6, column=0, columnspan=5, pady=5)

        # Tworzenie ramki dla pola tekstowego i paska przewijania
        results_frame = tk.Frame(self.root)
        results_frame.grid(row=7, column=0, columnspan=5, padx=10, pady=10)

        # Pole tekstowe do wyświetlania wyników
        self.results_text = tk.Text(results_frame, font=('Arial', 12), height=10, width=40, wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, padx=5, pady=5)

        # Scrollbar - pasek przewijania
        self.scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Powiązanie scrollbar z polem tekstowym
        self.results_text.config(yscrollcommand=self.scrollbar.set)

        # Przycisk do czyszczenia wyników
        self.clear_button = tk.Button(self.root, text="Clear Results", font=('Arial', 14), command=self.clear_results)
        self.clear_button.grid(row=8, column=0, columnspan=5, pady=10)

    def validate_input(self, value):
        """Funkcja do weryfikacji, aby w okienku można było wpisać tylko jedną literę."""
        if value == "" or (len(value) == 1 and value.isalpha()):
            return True
        return False

    def load_words(self, filepath):
        """Wczytuje listę słów z pliku."""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                words = [line.strip().upper() for line in file if len(line.strip()) == 5]
            return words
        except FileNotFoundError:
            print(f"Plik {filepath} nie został znaleziony.")
            return []

    def load_letter_frequencies(self, filepath):
        """Wczytuje częstości liter z pliku."""
        frequencies = {}
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    # Pomija puste linie oraz linie, które nie mają dokładnie 2 elementów
                    parts = line.strip().split()
                    if len(parts) == 2:
                        letter, freq = parts
                        frequencies[letter.upper()] = float(freq)
                    else:
                        print(f"Zignorowano linię: {line.strip()}")
            return frequencies
        except FileNotFoundError:
            print(f"Plik {filepath} nie został znaleziony.")
            return {}

    def submit_data(self):
        """Funkcja do przetwarzania danych po kliknięciu przycisku 'Submit'."""
        # Pobierz wartości z okienek
        entered_letters = [entry.get().upper() for entry in self.entries]
        excluded_letters = self.exclude_entry.get().upper().replace(" ", "").replace(",", "")
        yellow_letters = self.yellow_entry.get().upper().replace(" ", "").replace(",", "")
        
        print(f"Entered letters: {entered_letters}")
        print(f"Excluded letters: {excluded_letters}")
        print(f"Yellow letters: {yellow_letters}")

        # Filtrowanie słów na podstawie danych z interfejsu
        filtered_words = self.filter_words(entered_letters, excluded_letters, yellow_letters)
        
        # Posortuj słowa według sumy częstości liter
        filtered_words.sort(key=self.calculate_word_frequency, reverse=True)
        
        # Wyświetl przefiltrowane i posortowane słowa w polu tekstowym
        self.results_text.delete(1.0, tk.END)  # Wyczyść poprzednie wyniki
        if filtered_words:
            for word in filtered_words:
                self.results_text.insert(tk.END, word + "\n")
        else:
            self.results_text.insert(tk.END, "Brak możliwych słów.\n")

    def clear_results(self):
        """Funkcja do czyszczenia wyników w polu tekstowym."""
        self.results_text.delete(1.0, tk.END)

    def filter_words(self, entered_letters, excluded_letters, yellow_letters):
        """Filtruje słowa na podstawie wprowadzonych liter, wykluczonych liter oraz liter żółtych."""
        filtered_words = []

        for word in self.words:
            match = True

            # Sprawdzenie, czy słowo pasuje do wprowadzonych liter w odpowiednich pozycjach
            for i, letter in enumerate(entered_letters):
                if letter and word[i] != letter:
                    match = False
                    break

            # Sprawdzenie, czy słowo zawiera wykluczone litery
            if any(excluded in word for excluded in excluded_letters):
                match = False

            # Sprawdzenie, czy słowo zawiera wszystkie litery żółte
            if not all(letter in word for letter in yellow_letters):
                match = False

            if match:
                filtered_words.append(word)

        return filtered_words

    def calculate_word_frequency(self, word):
        """Oblicza sumę częstości liter w słowie."""
        return sum(self.letter_frequencies.get(letter, 0) for letter in word if letter in self.letter_frequencies)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordleSolverApp(root)
    root.mainloop()
