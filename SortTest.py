import time
import random
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)


# Реализации алгоритмов сортировки
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Функция для тестирования производительности
def test_algorithm(algorithm, data, name):
    arr = data.copy()
    start_time = time.time()

    sorted_arr = algorithm(arr)

    end_time = time.time()
    execution_time = end_time - start_time

    # Проверка корректности сортировки
    assert sorted_arr == sorted(data.copy()), f"Ошибка в алгоритме {name}"

    return execution_time


# Генерация тестовых данных
def generate_test_data(size, data_type):
    if data_type == "random":
        return [random.randint(1, 10000) for _ in range(size)]
    elif data_type == "partially_sorted":
        sorted_part = sorted([random.randint(1, 10000) for _ in range(int(size * 0.7))])
        random_part = [random.randint(1, 10000) for _ in range(size - len(sorted_part))]
        return sorted_part + random_part
    elif data_type == "reversed":
        return list(range(size, 0, -1))
    elif data_type == "almost_sorted":
        arr = list(range(size))
        for _ in range(size // 20):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr


# Основная функция тестирования
def run_comprehensive_test():
    sizes = [100, 1000, 5000, 10000, 20000]
    data_types = {
        "random": "Случайные данные",
        "partially_sorted": "Частично отсортированные",
        "reversed": "Обратно отсортированные",
        "almost_sorted": "Почти отсортированные"
    }

    algorithms = [
        (bubble_sort, "Bubble Sort"),
        (insertion_sort, "Insertion Sort"),
        (quicksort, "Quicksort"),
        (merge_sort, "Merge Sort"),
    ]

    # Словарь для хранения результатов
    results = {alg_name: {data_type: [] for data_type in data_types}
               for _, alg_name in algorithms}

    # Проведение тестов
    for data_type, data_name in data_types.items():
        print(f"\n=== Тестирование на {data_name} ===")

        for size in sizes:
            test_data = generate_test_data(size, data_type)
            print(f"\nРазмер массива: {size}")

            for algorithm, alg_name in algorithms:
                try:
                    time_taken = test_algorithm(algorithm, test_data, alg_name)
                    results[alg_name][data_type].append((size, time_taken))
                    print(f"{alg_name}: {time_taken:.4f} сек")
                except RecursionError:
                    print(f"{alg_name}: RecursionError на размере {size}")
                    results[alg_name][data_type].append((size, float('inf')))
                except Exception as e:
                    print(f"{alg_name}: Ошибка {e} на размере {size}")
                    results[alg_name][data_type].append((size, float('inf')))

    return results, sizes, data_types


# Функция для построения графиков
def plot_results(results, sizes, data_types):
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()

    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']
    markers = ['o', 's', '^', 'D', 'v', '<']

    # Построение графиков для каждого типа данных
    for idx, (data_type, data_name) in enumerate(data_types.items()):
        ax = axes[idx]

        for color_idx, (alg_name, data_results) in enumerate(results.items()):
            if data_type in data_results:
                sizes_alg = [point[0] for point in data_results[data_type]]
                times_alg = [point[1] for point in data_results[data_type]]

                ax.plot(sizes_alg, times_alg,
                        marker=markers[color_idx % len(markers)],
                        linewidth=2,
                        markersize=6,
                        color=colors[color_idx % len(colors)],
                        label=alg_name)

        ax.set_title(f'{data_name}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Размер массива', fontsize=12)
        ax.set_ylabel('Время выполнения (сек)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Логарифмическая шкала для лучшей визуализации
        ax.set_yscale('log')
        ax.set_xscale('log')

    plt.tight_layout()
    plt.show()


# Функция для создания итоговой таблицы результатов
def print_results_table(results, sizes):
    print("\n" + "=" * 80)
    print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("=" * 80)

    data_types = ["random", "partially_sorted", "reversed", "almost_sorted"]
    data_names = {
        "random": "Случайные",
        "partially_sorted": "Частично отсорт.",
        "reversed": "Обратные",
        "almost_sorted": "Почти отсорт."
    }

    for data_type in data_types:
        print(f"\n--- {data_names[data_type]} данные ---")
        print(f"{'Алгоритм':<15} {'n=100':<10} {'n=1000':<10} {'n=5000':<10} {'n=10000':<10} {'n=20000':<10}")
        print("-" * 70)

        for alg_name in results.keys():
            if data_type in results[alg_name]:
                times = [f"{point[1]:.4f}" if point[1] != float('inf') else "FAIL"
                         for point in results[alg_name][data_type]]
                print(f"{alg_name:<15} {times[0]:<10} {times[1]:<10} {times[2]:<10} {times[3]:<10} {times[4]:<10}")


if __name__ == "__main__":
    print("Начало комплексного тестирования алгоритмов сортировки...")
    print("Это может занять несколько минут...")

    results, sizes, data_types = run_comprehensive_test()

    print("\nПостроение графиков...")
    plot_results(results, sizes, data_types)

    print_results_table(results, sizes)

    print("\nТестирование завершено!")