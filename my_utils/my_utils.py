# Manejo de Archivos
import urllib.request
from pathlib import Path

# Analítica de datos
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Matemáticas
from math import ceil


def descargarData():

    FILE_NAME = 'taylor_swift_spotify.json'
    PATH = 'data/'
    jsonPath = Path(f'{PATH}{FILE_NAME}')

    if not jsonPath.is_file():
        Path(PATH).mkdir(parents=True, exist_ok=True)
        print(f'Directorio "{PATH}" creado')

        URL = 'https://drive.google.com/u/0/uc?id=1O-z8fCDXy5IleKfU6wRAJZjyz_FIGv9F&export=download'
        print('Descargando...')

        urllib.request.urlretrieve(URL, jsonPath)
        print(f'El archivo "{FILE_NAME}" ha sido descargado en: "{PATH}"')
    else:
        print(f'El archivo "{FILE_NAME}" ya existe en el directorio: "{PATH}"')


def null_review(df):

    mi_dict = {"Column": [], "dType": [], "No_Null_%": [], "No_Null_Qty": [], "Null_%": [], "Null_Qty": []}
    duplicated_rows = df[df.duplicated()]
    count_duplicated_rows = len(duplicated_rows)

    for columna in df.columns:
        no_null = df[columna].dropna()
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        mi_dict["Column"].append(columna)

        if no_null.empty:
            mi_dict["dType"].append([None])
        else:
            mi_dict["dType"].append(no_null.apply(type).unique())

        mi_dict["No_Null_%"].append(round(porcentaje_no_nulos, 2))
        mi_dict["No_Null_Qty"].append(df[columna].count())
        mi_dict["Null_%"].append(round(100-porcentaje_no_nulos, 2))
        mi_dict["Null_Qty"].append(df[columna].isnull().sum())

    df_info = pd.DataFrame(mi_dict)
    
    print("\nTotal rows: ", len(df))
    print("\nTotal full null rows: ", df.isna().all(axis=1).sum())
    print("\nTotal duplicated rows:", count_duplicated_rows)
    
    return df_info


def saveGraph(graph_id, tight_layout=True, graph_extension='png', resolution=300):

    imagesPath = Path('images')
    imagesPath.mkdir(parents=True, exist_ok=True)

    graphPath = imagesPath/f'{graph_id}.{graph_extension}'

    if tight_layout:
        plt.tight_layout()
    
    plt.savefig(graphPath, format=graph_extension, dpi=resolution)


def multiHist(filename, df, bins=50, kde=True, bar_color='#329D9C', kde_color='#472F7D'):

    df = df.select_dtypes(include='number')

    numCols = len(df.columns)
    numRows = (numCols + 1) // 2

    height = ceil(numCols/2)*3
    figsize = (15, height)

    fig, axes = plt.subplots(nrows=numRows, ncols=2, figsize=figsize)

    fig.subplots_adjust(hspace=0.5)
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        ax = axes[i]

        sns.histplot(df[column], bins=bins, color=bar_color, alpha=1, kde=kde, line_kws={'lw': 1.5}, ax=ax) #type: ignore
        
        try:
            ax.lines[0].set_color(kde_color)
        except IndexError:
            continue

        ax.grid(True, color='grey', linewidth='0.5', axis='y', alpha=0.3)
        ax.set_axisbelow(True)

        ax.set_xlabel('')
        ax.set_ylabel('')

        ax.set_title(column, loc='center', pad=15, weight='bold', fontsize=12, fontfamily='arial')

        ax.tick_params(axis='x', labelsize=8, labelfontfamily='arial')
        ax.tick_params(axis='y', labelsize=8, labelfontfamily='arial')

    if numCols % 2 != 0:
        fig.delaxes(axes[-1])

    saveGraph(filename, tight_layout=False)