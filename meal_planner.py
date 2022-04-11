import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    recipes_df = pd.read_csv('RECIPES.csv')

    for i in range(len(recipes_df)):
        recipes_df.at[i, 'ingredients'] = recipes_df.at[i, 'ingredients'].split(', ')

    pastas_df = recipes_df[recipes_df['type'] == 'Pasta']
    milanesas_df = recipes_df[recipes_df['type'] == 'Milanesas']
    medallones_df = recipes_df[recipes_df['type'] == 'Medallones']
    arroz_df = recipes_df[recipes_df['type'] == 'Arroz']
    elaborados_df = recipes_df[recipes_df['type'] == 'Elaborado']

    comidas = [elaborados_df.sample(2), arroz_df.sample(2), pastas_df.sample(3),
               medallones_df.sample(4), milanesas_df.sample(3)]
    comidas_df = pd.concat(comidas)
    comidas_df = comidas_df.sample(frac=1).reset_index(drop=True)


    def to_1d(series):
        return pd.Series([x for _list in series for x in _list])


    compras = to_1d(comidas_df['ingredients']).value_counts().to_string()

    menu = {
        'Lunes': [],
        'Martes': [],
        'Miércoles': [],
        'Jueves': [],
        'Viernes': [],
        'Sábado': [],
        'Domingo': [],
    }

    week = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    for day in week:
        comidas_temp = comidas_df

        comidas_validas_A = comidas_temp[comidas_temp['type'] != 'Elaborado']

        meal_A = comidas_validas_A.sample()
        comidas_temp.drop(meal_A.index, inplace=True)
        menu[day].append(meal_A['name'].to_string(index=False))

        comidas_validas_C = comidas_temp[comidas_temp['type'] != meal_A['type'].to_string(index=False)]
        comidas_validas_C = comidas_validas_C[(comidas_validas_C['highlight'] == 'None') |
                                              (comidas_validas_C['highlight'] !=
                                               meal_A['highlight'].to_string(index=False))]

        if len(comidas_validas_C) != 0:
            meal_C = comidas_validas_C.sample()
            comidas_temp.drop(meal_C.index, inplace=True)
            menu[day].append(meal_C['name'].to_string(index=False))
        else:
            print('No se encontró combinación de comidas válida')

    menu_df = pd.DataFrame.from_dict(menu)

    menu_str = menu_df.transpose().rename({0: 'Almuerzo', 1: 'Cena'}, axis=1).to_string()

    with open('menu_y_compras-' + datetime.now().strftime("%d-%m-%Y@%H:%M:%S") + '.txt', 'w') as f:
        print('###### MENU SEMANAL ######', file=f)
        print(menu_str, file=f)
        print('', file=f)
        print('###### LISTA DE COMPRAS ######', file=f)
        print(compras, file=f)
