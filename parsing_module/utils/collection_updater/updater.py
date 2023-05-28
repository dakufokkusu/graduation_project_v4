from pymongo import MongoClient
from parsing_module.utils.collection_updater.interface import UpdaterInterface


class Updater(UpdaterInterface):
    def __init__(self):
        self._client = MongoClient()
        self._collection = self._client["data_cars"]["cars"]
        self._new_collection = self._client["data_cars"]["update_cars"]

    def _collect_all_the_keys(self):
        keys = []
        for car in self._collection.find():
            for key in car:
                if key not in keys:
                    keys.append(key)
        keys.append("Года поколения")
        return keys

    def _update_price(self, car):
        new_price = ''
        for el in car["Цена"]:
            if el.isdigit():
                new_price += el
        car["Цена"] = int(new_price)
        # print(car.items())

    def _update_year(self, car):
        new_year = ''
        for key in car:
            if key == "Год выпуска":
                for el in car.get(key):
                    if el.isdigit():
                        new_year += el
                car[key] = int(new_year)
                # print(car.items())

    def _update_mileage(self, car):
        new_mileage = ''
        for key in car:
            if key == "Пробег":
                for el in car.get(key):
                    if el.isdigit():
                        new_mileage += el
                car[key] = int(new_mileage)
                # print(car.items())

    def _update_breed(self, car):
        update_car = ''
        for key in car:
            if key == "Поколение":
                data = car.get(key)
                data = str(data).split('(')
                car[key] = data[0]
                update_car = data[1].replace(')', '')
        car["Года поколения"] = update_car
        # print(car.items())

    def _update_record(self, car, keys):
        new_car = {}
        for key in keys:
            if key in car:
                new_car[key] = car[key]
            else:
                new_car[key] = None
        return new_car

    def _start_update(self):
        records = []
        keys = self._collect_all_the_keys()
        keys.remove("VIN или номер кузова")
        for car in self._collection.find():
            self._update_price(car)
            self._update_year(car)
            self._update_mileage(car)
            self._update_breed(car)
            car = self._update_record(car, keys)
            records.append(car)
        return records

    def update(self):
        old_car = self._start_update()
        for car in old_car:
            self._new_collection.insert_one(car)

    def update_record(self, record):
        processed_record = dict()
        processed_record['price'] = record['Цена']
        processed_record['brand'] = record['Автомобиль'].split(',')[0].split()[0]
        processed_record['model'] = record['Автомобиль'].split(',')[0].split()[1]
        processed_record['year'] = record['Год выпуска']
        processed_record['breed'] = record['Поколение']
        processed_record['milage'] = record['Пробег']
        processed_record['milage_history'] = record['История пробега']
        processed_record['pts'] = record['ПТС']
        processed_record['n_owners'] = record['Владельцев по ПТС']
        processed_record['condition'] = record['Состояние']
        processed_record['modification'] = record['Модификация']
        if record['Объём двигателя'] is not None:
            processed_record['engine_capacity'] = float(record['Объём двигателя'].replace(' л', ''))
        else: processed_record['engine_capacity'] = record['Объём двигателя']
        processed_record['engine_type'] = record['Тип двигателя']
        processed_record['transmission'] = record['Коробка передач']
        processed_record['drive_unit'] = record['Привод']
        processed_record['equipment'] = record['Комплектация']
        processed_record['body_type'] = record['Тип кузова']
        processed_record['color'] = record['Цвет']
        processed_record['steering_wheel'] = record['Руль']
        processed_record['description'] = record['Описание']
        processed_record['link'] = record['Ссылка']
        return record


# if __name__ == '__main__':
#     updater = Updater()
#     updater.update()