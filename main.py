import os
from dotenv import load_dotenv
from pprint import pprint
from sqlalchemy import select, create_engine, func
from sqlalchemy.orm import Session


def get_info_farm(ses, type_location='нормальная', name_person='FuHuK', id_person=5):
    for row in ses.execute(query_farm(type_location, name_person, id_person)):
        out = (f"Хроники: {row[0]}\t"
               f"Имя: {row[1]}\t"
               f"Профессия: {row[2]}\t"
               f"Локация: {row[3]}\n"
               f"Средний опыт: {int(row[5])}\t"
               f"Средний фарм: {int(row[6])}\n")
        print(out)


def get_info_farm_dict(ses, type_location='нормальная'):
    farm_dict = {}
    for row in ses.execute(query_farm_dict(type_location)):
        if row[1] in farm_dict:
            farm_dict.get(row[1]).update({row[5]: [row[0], int(row[3]), int(row[4])]})
        else:
            farm_dict[row[1]] = {row[5]: [row[0], int(row[3]), int(row[4])]}
    return farm_dict


if __name__ == '__main__':

    load_dotenv()
    engine = create_engine(os.getenv('DSN'))
    create_tables(engine)

    with Session(engine) as session:
        # add_db.add_chronicle_person(session, 2, 1)

        # add_db.add_location(session, 'Каньон Горда', 'нормальная')

        # add_db.add_farm(session, 6, 2, 673, 298526, 468083399, 190000000)

        get_info_farm(session, type_location='нормальная', name_person='FuHuK', id_person=6)

