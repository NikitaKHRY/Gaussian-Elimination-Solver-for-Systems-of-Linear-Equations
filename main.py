import copy

def input_from_keyboard():
    while True:
        try:
            n = int(input("Введіть розмірність системи (кількість рівнянь): "))
            if n <= 0:
                print("Розмірність має бути додатнім цілим числом.")
                continue
            break
        except ValueError:
            print("Некоректне значення. Введіть ціле число.")

    print(f"Введіть коефіцієнти та вільні члени для {n} рівнянь (через пробіл):")
    A = []
    b = []
    for i in range(n):
        while True:
            try:
                row_input = input(f"Рівняння {i + 1} (формат: a1 a2 ... an): ").strip()
                parts = list(map(float, row_input.split()))
                if len(parts) != n:
                    raise ValueError(f"Потрібно ввести рівно {n} коефіцієнтів.")
                A.append(parts)

                free = float(input(f"Вільний член {i + 1}: "))
                b.append(free)
                break
            except ValueError as e:
                print(f"Помилка: {e}. Повторіть ввод.")
    return A, b


def input_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            n = len(lines)
            if n == 0:
                raise ValueError("Файл порожній.")
            A = []
            b = []
            for line_num, line in enumerate(lines):
                parts = list(map(float, line.split()))
                if len(parts) != n + 1:
                    raise ValueError(f"У рядку {line_num + 1} має бути рівно {n + 1} чисел.")
                A.append(parts[:-1])
                b.append(parts[-1])
        return A, b
    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено.")
        exit()
    except ValueError as e:
        print(f"Помилка формату у файлі: {e}")
        exit()


def is_zero_row(row):
    return all(abs(x) < 1e-12 for x in row)


def gauss_method(A, b):
    n = len(A)
    A = copy.deepcopy(A)
    b = copy.deepcopy(b)

    for i in range(n):
        # Перевірка на нульовий елемент по діагоналі
        if abs(A[i][i]) < 1e-12:
            # Якщо елемент 0, намагаємось поміняти рядок з нижнім
            swapped = False
            for k in range(i+1, n):
                if abs(A[k][i]) > 1e-12:
                    A[i], A[k] = A[k], A[i]
                    b[i], b[k] = b[k], b[i]
                    swapped = True
                    break
            if not swapped:
                raise ValueError(f"Неможливо розв'язати систему: нульовий елемент у діагоналі на позиції {i+1}, перестановка неможлива.")

        # Ділимо i-й рядок на елемент по діагоналі
        pivot = A[i][i]
        if abs(pivot) < 1e-12:
            raise ValueError(f"Неможливо розв'язати систему: ділення на нуль у рядку {i+1}.")
        for j in range(n):
            A[i][j] /= pivot
        b[i] /= pivot

        # Віднімаємо i-й рядок, помножений на коефіцієнти i-го стовпця інших рядків
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]

    # Перевірка сумісності та визначеність системи
    for i in range(n):
        if is_zero_row(A[i]):
            if abs(b[i]) > 1e-12:
                raise ValueError("Система несумісна: рядок з нульовими коефіцієнтами і ненульовим вільним членом.")
            # Якщо і рядок і вільний член 0 — рядок можна ігнорувати (можлива безліч розв'язків)

    return b  # Після приведення матриці до одиничної, вектор b — розв'язок


def verify_solution(A, b, x):
    n = len(A)
    for i in range(n):
        lhs = sum(A[i][j] * x[j] for j in range(n))
        if abs(lhs - b[i]) > 1e-6:
            return False
    return True

if __name__ == "__main__":
    while True:
        print("\nОберіть спосіб введення:")
        print("1 - Через екранну форму")
        print("2 - Із файлу data.txt")
        print("3 - Вихід з програми")
        choice = input("Ваш вибір: ")

        if choice == '1':
            try:
                A, b = input_from_keyboard()
                result = gauss_method(A, b)
                if verify_solution(A, b, result):
                    print("\nРозв'язок:")
                    for i, val in enumerate(result):
                        print(f"x{i+1} = {val:.6f}")
                else:
                    print("Перевірка розв'язку не пройдена.")
            except ValueError as e:
                print(f"\nПомилка: {e}")

        elif choice == '2':
            try:
                A, b = input_from_file("data.txt")
                result = gauss_method(A, b)
                if verify_solution(A, b, result):
                    print("\nРозв'язок:")
                    for i, val in enumerate(result):
                        print(f"x{i+1} = {val:.6f}")
                else:
                    print("Перевірка розв'язку не пройдена.")
            except ValueError as e:
                print(f"\nПомилка: {e}")

        elif choice == '3':
            print("Завершення програми. Дякую за використання!")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")
