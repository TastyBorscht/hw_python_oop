from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    """Переменная с фразой."""
    STR_PHRASE: str = ('Тип тренировки: {}; Длительность: {:.3f} ч.;'
                       ' Дистанция: {:.3f} км; '
                       'Ср. скорость: {:.3f} км/ч; Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Возвращает строку с данными о тренировке."""
        return self.STR_PHRASE.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Длина одного шага в м.
    M_IN_KM: int = 1000  # Константа для перевода метррв в км.
    H_IN_MIN: int = 60  # Константа для перевода часы в мин.

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
        raise NotImplementedError('Метод не был переопределен у подкласса.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = self.__class__.__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()

        return InfoMessage(training_type,
                           duration,
                           distance,
                           speed,
                           calories)


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
    class_dict: dict[str, type[Training]] = {  # Cловарь для создания
        'SWM': Swimming,                       # объекта класса Training.
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type not in class_dict:
        raise ValueError('Передан неизвестный тип данных.')
    return class_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
