import numpy as np
import matplotlib.pyplot as plt
import math

class ConveyorSimulator:
    """
    Симулятор разъединения простейшего потока на конвейере
    """
    
    def __init__(self, lambd: float, k: int, probabilities: list, T: float):
        # Проверка интенсивности
        if lambd <= 0:
            raise ValueError(f"Интенсивность λ должна быть положительной, получено: {lambd}")
        
        # Проверка количества направлений
        if k < 1:
            raise ValueError(f"Количество направлений k должно быть не менее 1, получено: {k}")
        
        # Проверка времени моделирования
        if T <= 0:
            raise ValueError(f"Время моделирования T должно быть положительным, получено: {T}")
        
        # Проверка количества вероятностей
        if len(probabilities) != k:
            raise ValueError(f"Количество вероятностей ({len(probabilities)}) не совпадает с k ({k})")
        
        # ========== НОВЫЕ ПРОВЕРКИ ДЛЯ ВЕРОЯТНОСТЕЙ ==========
        # Проверка 1: Каждая вероятность не может быть меньше 0
        for i, p in enumerate(probabilities):
            if p < 0:
                raise ValueError(f"Вероятность p_{i+1} = {p} не может быть меньше 0")
        
        # Проверка 2: Каждая вероятность не может быть больше 1
        for i, p in enumerate(probabilities):
            if p > 1:
                raise ValueError(f"Вероятность p_{i+1} = {p} не может быть больше 1")
        
        # Проверка 3: Сумма вероятностей должна быть равна 1 (с допустимой погрешностью)
        prob_sum = sum(probabilities)
        if abs(prob_sum - 1.0) > 1e-6:
            raise ValueError(f"Сумма вероятностей должна быть равна 1, получено: {prob_sum}")
        
        self.lambd = lambd
        self.k = k
        self.probabilities = probabilities
        self.T = T
    
    def simulate(self):
        """Моделирование разъединения потока"""
        lambda_tau = self.lambd * self.T
        total_boxes = np.random.poisson(lambda_tau)
        
        if total_boxes > 0:
            arrival_times = np.sort(np.random.uniform(0, self.T, total_boxes))
        else:
            arrival_times = np.array([])
        
        direction_counts = [0] * self.k
        for _ in range(total_boxes):
            direction = np.random.choice(self.k, p=self.probabilities)
            direction_counts[direction] += 1
        
        intensities = [count / self.T for count in direction_counts]
        
        return arrival_times, intensities, direction_counts, total_boxes
    
    def theoretical_intensities(self):
        """Теоретическая формула: λ_i = λ * p_i"""
        return [self.lambd * p for p in self.probabilities]
    
    def plot_all(self, arrival_times, intensities, direction_counts, total_boxes):
        """Все графики для наглядности"""
        
        theor_intensities = self.theoretical_intensities()
        theor_counts = [self.lambd * p * self.T for p in self.probabilities]
        
        fig = plt.figure(figsize=(16, 12))
        
        # График 1: Моменты поступления
        ax1 = fig.add_subplot(2, 3, 1)
        if len(arrival_times) > 0:
            ax1.eventplot([arrival_times], colors='blue', linewidths=2)
        ax1.set_xlabel('Время t (мин)')
        ax1.set_title('Моменты появления коробок перед развилкой')
        ax1.set_ylim(0.5, 1.5)
        ax1.grid(True, alpha=0.3)
        
        # График 2: Гистограмма интервалов
        ax2 = fig.add_subplot(2, 3, 2)
        if len(arrival_times) > 1:
            intervals = np.diff(np.concatenate(([0], arrival_times)))
            ax2.hist(intervals, bins=min(20, len(intervals)), 
                    edgecolor='black', alpha=0.7, density=True)
            x = np.linspace(0, max(intervals), 100)
            ax2.plot(x, self.lambd * np.exp(-self.lambd * x), 
                    'r-', linewidth=2, label='Теор. эксп. кривая')
            ax2.legend()
        ax2.set_xlabel('Интервал между поступлениями (мин)')
        ax2.set_title('Распределение интервалов')
        ax2.grid(True, alpha=0.3)
        
        # График 3: Количество коробок по направлениям
        ax3 = fig.add_subplot(2, 3, 3)
        x = np.arange(self.k)
        width = 0.35
        ax3.bar(x - width/2, direction_counts, width, label='Эксперимент', alpha=0.7, color='steelblue')
        ax3.bar(x + width/2, theor_counts, width, label='Теория (λ·p_i·T)', alpha=0.7, color='orange')
        ax3.set_xlabel('Направление')
        ax3.set_ylabel('Количество коробок')
        ax3.set_title('Распределение коробок по направлениям')
        ax3.set_xticks(x)
        ax3.set_xticklabels([f'{i+1}' for i in range(self.k)])
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # График 4: Интенсивности по направлениям
        ax4 = fig.add_subplot(2, 3, 4)
        ax4.bar(x - width/2, intensities, width, label='Эксперимент (λ_i = кол-во/T)', 
                alpha=0.7, color='steelblue')
        ax4.bar(x + width/2, theor_intensities, width, label='Теория (λ_i = λ·p_i)', 
                alpha=0.7, color='orange')
        ax4.set_xlabel('Направление')
        ax4.set_ylabel('Интенсивность λ_i (шт/мин)')
        ax4.set_title('Интенсивность потока по направлениям')
        ax4.set_xticks(x)
        ax4.set_xticklabels([f'{i+1}' for i in range(self.k)])
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # График 5: Распределение Пуассона
        ax5 = fig.add_subplot(2, 3, 5)
        n_experiments = 1000
        event_counts = []
        for _ in range(n_experiments):
            lambda_tau = self.lambd * self.T
            event_counts.append(np.random.poisson(lambda_tau))
        
        ax5.hist(event_counts, bins=range(0, max(event_counts)+2), 
                edgecolor='black', alpha=0.7, density=True, label='Эксперимент')
        
        max_k = max(event_counts)
        x_poisson = np.arange(0, max_k + 1)
        theor_poisson = []
        for k_val in x_poisson:
            prob = (lambda_tau ** k_val) * math.exp(-lambda_tau) / math.factorial(k_val)
            theor_poisson.append(prob)
        ax5.plot(x_poisson, theor_poisson, 'r-', linewidth=2, label='Теория (Пуассон)')
        
        ax5.set_xlabel('Количество коробок за время T')
        ax5.set_ylabel('Вероятность')
        ax5.set_title(f'Распределение Пуассона\nP(k) = (λT)^k·e^(-λT)/k!')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # График 6: Накопленные события
        ax6 = fig.add_subplot(2, 3, 6)
        if len(arrival_times) > 0:
            cumulative = np.arange(1, len(arrival_times) + 1)
            ax6.plot(arrival_times, cumulative, 'b-', linewidth=2, label='Эксперимент')
            ax6.plot([0, self.T], [0, self.lambd * self.T], 'r--', 
                    linewidth=2, label=f'Теория: λT = {self.lambd * self.T:.1f}')
            ax6.legend()
        ax6.set_xlabel('Время t (мин)')
        ax6.set_ylabel('Накопленное количество коробок')
        ax6.set_title('Накопленное количество коробок во времени')
        ax6.grid(True, alpha=0.3)
        
        plt.suptitle(f'Моделирование разъединения простейшего потока\n'
                    f'λ = {self.lambd} шт/мин,  T = {self.T} мин,  '
                    f'p_i = {self.probabilities}', fontsize=14)
        plt.tight_layout()
        plt.show()
    
    def print_results(self, arrival_times, intensities, direction_counts, total_boxes):
        """Вывод результатов"""
        theor_intensities = self.theoretical_intensities()
        
        print("=" * 70)
        print("РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ РАЗЪЕДИНЕНИЯ ПРОСТЕЙШЕГО ПОТОКА")
        print("=" * 70)
        
        print(f"\n📊 ВХОДНЫЕ ПАРАМЕТРЫ:")
        print(f"   • Интенсивность входного потока:        λ = {self.lambd} шт/мин")
        print(f"   • Количество направлений:               k = {self.k}")
        print(f"   • Вероятности направлений:              p_i = {[round(p, 2) for p in self.probabilities]}")
        print(f"   • Сумма вероятностей:                   Σp_i = {sum(self.probabilities)}")
        print(f"   • Время моделирования:                  T = {self.T} мин")
        print(f"   • Теоретическое среднее количество:     λ·T = {self.lambd * self.T:.2f} шт")
        
        print(f"\n⏱️ МОМЕНТЫ ПОЯВЛЕНИЯ КОРОБОК ПЕРЕД РАЗВИЛКОЙ (первые 10 из {len(arrival_times)}):")
        for i, t in enumerate(arrival_times[:10], 1):
            print(f"   Коробка {i:3d}: t = {t:.4f} мин")
        if len(arrival_times) > 10:
            print(f"   ... и еще {len(arrival_times) - 10} коробок")
        
        print(f"\n📈 РЕЗУЛЬТАТЫ ПО НАПРАВЛЕНИЯМ:")
        print(f"   {'Напр.':<6} {'Теор. формула':<25} {'Эксп. λ_i':<12} {'Кол-во':<8}")
        print(f"   {'':6} {'λ_i = λ·p_i':<25} {'(шт/мин)':<12} {'(шт)':<8}")
        print("-" * 60)
        
        for i in range(self.k):
            print(f"   {i+1:^6} λ_{i+1} = {self.lambd}·{self.probabilities[i]} = {theor_intensities[i]:.3f}     "
                  f"{intensities[i]:<12.4f} {direction_counts[i]:<8}")
        
        print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
        print(f"   • Всего коробок на конвейере:           {total_boxes} шт")
        print(f"   • Теоретическое среднее (λT):           {self.lambd * self.T:.2f} шт")
        print(f"   • Сумма экспериментальных λ_i:          {sum(intensities):.4f} шт/мин (≈ λ = {self.lambd})")
        
        print(f"\n✅ ПРОВЕРКА ТЕОРЕТИЧЕСКИХ ФОРМУЛ:")
        for i in range(self.k):
            if theor_intensities[i] > 0:
                rel_error = abs(intensities[i] - theor_intensities[i]) / theor_intensities[i] * 100
            else:
                rel_error = abs(intensities[i] - theor_intensities[i]) * 100
            print(f"   Направление {i+1}: |λ_i(эксп) - λ·p_i| / (λ·p_i) = {rel_error:.2f}%")


# ===================== ЗАПУСК С РАЗНЫМИ ПРИМЕРАМИ =====================
if __name__ == "__main__":
    np.random.seed(42)
    
    print("=" * 70)
    print("ПРОВЕРКА КОРРЕКТНЫХ ДАННЫХ")
    print("=" * 70)
    
    # Пример 1: Корректные данные
    print("\n✅ Пример 1: Корректные данные")
    print("-" * 50)
    try:
        simulator = ConveyorSimulator(
            lambd=10.0, 
            k=3, 
            probabilities=[0.5, 0.3, 0.2], 
            T=10.0
        )
        arrival_times, intensities, direction_counts, total_boxes = simulator.simulate()
        simulator.print_results(arrival_times, intensities, direction_counts, total_boxes)
        simulator.plot_all(arrival_times, intensities, direction_counts, total_boxes)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Пример 2: Некорректные данные (отрицательная вероятность)
    print("\n" + "=" * 70)
    print("ПРОВЕРКА НЕКОРРЕКТНЫХ ДАННЫХ")
    print("=" * 70)
    
    print("\n❌ Пример 2: Отрицательная вероятность")
    print("-" * 50)
    try:
        simulator = ConveyorSimulator(
            lambd=10.0, 
            k=3, 
            probabilities=[0.5, -0.1, 0.6],  # p₂ = -0.1 < 0
            T=10.0
        )
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    print("\n❌ Пример 3: Вероятность больше 1")
    print("-" * 50)
    try:
        simulator = ConveyorSimulator(
            lambd=10.0, 
            k=3, 
            probabilities=[0.5, 1.5, -1.0],  # p₂ = 1.5 > 1
            T=10.0
        )
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    print("\n❌ Пример 4: Сумма вероятностей не равна 1")
    print("-" * 50)
    try:
        simulator = ConveyorSimulator(
            lambd=10.0, 
            k=3, 
            probabilities=[0.5, 0.3, 0.3],  # сумма = 1.1 ≠ 1
            T=10.0
        )
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    print("\n❌ Пример 5: Отрицательная интенсивность")
    print("-" * 50)
    try:
        simulator = ConveyorSimulator(
            lambd=-5.0,  # λ < 0
            k=3, 
            probabilities=[0.5, 0.3, 0.2], 
            T=10.0
        )
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    print("\n❌ Пример 6: Отрицательное время моделирования")
    print("-" * 50)
    try:
        simulator = ConveyorSimulator(
            lambd=10.0, 
            k=3, 
            probabilities=[0.5, 0.3, 0.2], 
            T=-10.0  # T < 0
        )
    except ValueError as e:
        print(f"Ошибка: {e}")
