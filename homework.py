from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    TIME_IN_MINUTES = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определить get_spent_calories()'
                                  ' в классах наследниках Running'
                                  ' SportsWalking, Swimming')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN1 = 18
    COEFF_CALORIE_RUN2 = 20

    def get_spent_calories(self) -> float:
        calories: float = ((self.COEFF_CALORIE_RUN1 * self.get_mean_speed()
                           - self.COEFF_CALORIE_RUN2) * self.weight
                           / self.M_IN_KM * self.duration
                           * self.TIME_IN_MINUTES)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WLK1 = 0.035
    COEFF_CALORIE_WLK2 = 2
    COEFF_CALORIE_WLK3 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченный калорий при спортивной хотьбе."""
        calories: float = ((self.COEFF_CALORIE_WLK1 * self.weight
                           + self.get_mean_speed()**self.COEFF_CALORIE_WLK2
                           // self.height * self.COEFF_CALORIE_WLK3
                           * self.weight) * self.duration
                           * self.TIME_IN_MINUTES)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_SWM1 = 1.1
    COEFF_CALORIE_SWM2 = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавание."""
        self.speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченный калорий при плавание."""
        calories: float = ((self.get_mean_speed() + self.COEFF_CALORIE_SWM1)
                           * self.COEFF_CALORIE_SWM2 * self.weight)
        return calories


def read_package(workout_type: str, data: Union[int, float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainig_types: Dict[str, List[Union[float, str]]] = {'RUN': Running,
                                                         'WLK': SportsWalking,
                                                         'SWM': Swimming}
    return trainig_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: str = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
