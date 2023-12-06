from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    """Переменные с фразами."""
    TRAINING_TYPE: str = 'Тип тренировки: {}; '
    DURATION: str = 'Длительность: {:.3f}; '
    DISTANCE: str = 'Дистанция: {:.3f} км: '
    MEAN_SPEAD: str = 'Ср. скорость: {:.3f} км/ч; '
    SPENT_CAL: str = 'Потрачено ккал: {:.3f}.'

    def get_message(self) -> tuple:
        """Возвращает кортеж с данными о тренировке."""
        return (self.TRAINING_TYPE.format(self.training_type),
                self.DURATION.format(self.duration),
                self.DISTANCE.format(self.distance),
                self.MEAN_SPEAD.format(self.speed),
                self.SPENT_CAL.format(self.calories))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # длина одного шага в м
    M_IN_KM: int = 1000  # константа для перевода метррв в км
    H_IN_MIN: int = 60  # константа для перевода часы в мин

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = self.__class__.__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()

        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.H_IN_MIN * self.duration))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_ACCELERATION_MULTIPLIER: float = 0.029
    SPEED_IN_M_PER_SEC: float = 0.278
    SM_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.SPEED_IN_M_PER_SEC) ** 2
                    / (self.height / self.SM_M))
                * self.CALORIES_ACCELERATION_MULTIPLIER * self.weight)
                * self.duration * self.H_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    MEAN_SPEED_SHIFT: float = 1.1
    SHIFTED_MEAN_SPEED_MULTIPLIER: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.MEAN_SPEED_SHIFT)
                * self.SHIFTED_MEAN_SPEED_MULTIPLIER
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_dict = {  # словарь для создания объекта класса Training
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    training: Training = class_dict[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    my_message: str = ''  # создаём строку из пришедших кортежей
    for s in info.get_message():
        my_message += s
    print(my_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
