import pyodbc
import time
import pandas as pd
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import shutil

# Carga variables desde el archivo .env
load_dotenv()
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DRIVER = os.getenv("DRIVER")

# Directorio de los archivos a monitorear
DIRECTORY= 'C:/Users/Desktop/Desktop/Proyecto final Henry/csv'
#PROCESADOS_DIR = os.path.join(DIRECTORY, 'archivos_procesados')

# Asegura que la carpeta 'archivos_procesados' exista
#os.makedirs(PROCESADOS_DIR, exist_ok=True)

# conexion y carga a la base de datos
def get_connection():
    print(f"🗄️ 🟢 Estableciendo Conexión a la Base de Datos")
    connection_string = f"mssql+pyodbc://{USER}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}"
    engine = create_engine(connection_string)
    return engine

def verificar_datos_nuevos(df, nombre_tabla):
    engine = get_connection()
    # Filtrando el df para cargar solamente datos nuevos
    ids_existentes = pd.read_sql(f"SELECT id FROM {nombre_tabla}", engine)
    ids_set = set(ids_existentes['id'])
    df_nuevos = df[~df['id'].isin(ids_set)]
    return df_nuevos

def cargar_a_sql(df, nombre_archivo):
    try:
        nombre_tabla = nombre_archivo.split('.')[0]
        nombre_tabla = nombre_tabla.capitalize()
        engine = get_connection()
        # Verificar si existen nuevos registros
        df_nuevos = verificar_datos_nuevos(df, nombre_tabla)
        if len(df_nuevos) > 0:
            df_nuevos.to_sql(nombre_tabla, con=engine, if_exists='append', index=False)
            print(f"🗄️ ✅ Datos cargados a la tabla {nombre_tabla}")
        else:
            print(f"🗄️ ✅ No hay nuevos registros para agregar en la tabla {nombre_tabla}")
    except SQLAlchemyError as e:
        print(f'Error en la Base de datos: {e}')

# def mover_archivo_procesado(file_name, file_path):
#     nuevo_path = os.path.join(PROCESADOS_DIR, file_name)
#     shutil.move(file_path, nuevo_path)
#     print(f"➡️📦 Archivo movido a {nuevo_path}") 
    
    
    
# Transformacion y limpieza
def procesar_player(file_path):
    player = pd.read_csv(file_path)
    return player

def procesar_team(file_path):
    team = pd.read_csv(file_path)
    return team

def procesar_game(file_path):
    game = pd.read_csv(file_path)
    engine = get_connection()
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    game_team_id = game[game['team_id_home'].isin(team["id"]) & game['team_id_away'].isin(team["id"])]
    game_2000 = game_team_id[game_team_id['game_date'] >= "2000-01-01"].copy()
    game_2000 = game_2000.fillna(0)
    return game_2000

def procesar_common_player_info(file_path):
    common_player_info = pd.read_csv(file_path)
    engine = get_connection()
    player = pd.read_sql("SELECT * FROM Player", con=engine)
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    common_player_info = common_player_info[common_player_info['team_id'].isin(team["id"]) 
                                & common_player_info['person_id'].isin(player["id"])]
    common_player_info = common_player_info[common_player_info["to_year"] >= 2000]
    delete_columns = ["first_name", "last_name", "display_first_last", "display_last_comma_first", 
                      "player_slug","jersey", "team_name", "team_abbreviation", "team_code", "team_city",
                      "games_played_current_season_flag"]
    common_player_info.drop(delete_columns, axis=1, inplace=True)
    common_player_info = common_player_info.dropna(subset=['height', 'weight', 'draft_number', 
                                                           'draft_number', 'position'])
    common_player_info[['school', 'country']] = common_player_info['last_affiliation'].str.split('/', n=1, expand=True)
    return common_player_info

def procesar_draft_combine_stats(file_path):
    draft_combine_stats = pd.read_csv(file_path)
    null_draft_combine_stats = draft_combine_stats.isnull().sum()
    total_register = len(draft_combine_stats)
    null_result = null_draft_combine_stats[null_draft_combine_stats > 0]
    df_null_draft_combine_stats = pd.DataFrame({
    "Valores nulos": null_result,
    "Total registros": total_register,
    "Porcentaje": (null_result / total_register * 100).round(2) })
    null_75 = df_null_draft_combine_stats[df_null_draft_combine_stats["Porcentaje"] > 75]
    delete_columns = list(null_75.index)
    draft_combine_stats.drop(columns=delete_columns, inplace=True)     
    delete_columns = ["height_w_shoes", "height_w_shoes_ft_in", "height_wo_shoes_ft_in", "modified_lane_agility_time",
                      "standing_reach_ft_in", "wingspan_ft_in", "hand_length", "hand_width"]
    draft_combine_stats.drop(delete_columns, axis=1, inplace=True)     
    draft_combine_stats = draft_combine_stats.dropna(subset=['height_wo_shoes', 'weight', 'wingspan', 'standing_reach', 
                                                             'body_fat_pct', 'standing_vertical_leap', 'max_vertical_leap', 'lane_agility_time', 
                                                             'three_quarter_sprint', 'bench_press'])
    engine = get_connection()
    player = pd.read_sql("SELECT * FROM Player", con=engine)
    draft_combine_stats = draft_combine_stats[draft_combine_stats['player_id'].isin(player['id'])]
    draft_combine_stats.drop_duplicates(subset='player_id', inplace=True)
    return draft_combine_stats

def procesar_draft_history(file_path):
    draft_history = pd.read_csv(file_path)
    draft_history = draft_history[draft_history["season"] >= 2000]
    draft_history = draft_history.dropna(subset=['organization', 'organization_type'])
    engine = get_connection()
    player = pd.read_sql("SELECT * FROM Player", con=engine)
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    draft_history = draft_history[draft_history['team_id'].isin(team['id']) & 
                                  draft_history['person_id'].isin(player['id'])]
    return draft_history

def procesar_team_details(file_path):
    team_details = pd.read_csv(file_path)
    delete_columns = ['facebook', 'instagram', 'twitter']
    team_details.drop(columns=delete_columns, inplace=True)
    team_details["arenacapacity"].fillna(team_details["arenacapacity"].median(), inplace=True)
    team_details.dropna(subset=['headcoach'], inplace=True)
    engine = get_connection()
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    team_details = team_details[team_details['team_id'].isin(team['id'])]
    return team_details

def procesar_team_history(file_path):
    team_history= pd.read_csv(file_path)
    engine = get_connection()
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    team_history = team_history[team_history['team_id'].isin(team['id'])]
    return team_history

def procesar_game_info(file_path):
    game_info = pd.read_csv(file_path)
    game_info_2000 = game_info[game_info["game_date"] >= "2000-01-01"].copy()
    delete_columns = ['attendance', 'game_time']
    game_info_2000.drop(delete_columns, axis=1, inplace=True)
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM Game", con=engine)
    game_info_2000 = game_info_2000[game_info_2000['game_id'].isin(game['game_id'])]
    return game_info_2000

def procesar_game_summary(file_path):
    game_summary = pd.read_csv(file_path)
    game_summary = game_summary[game_summary["game_date_est"] >= "2000-01-01"].copy()
    null_game_summary = game_summary.isnull().sum()
    total_register = len(game_summary)
    null_result = null_game_summary[null_game_summary > 0]

    df_null_game_summary = pd.DataFrame({
        "Valores nulos": null_result,
        "Total registros": total_register,
        "Porcentaje": (null_result / total_register * 100).round(2)
    })
    
    null_75 = df_null_game_summary[df_null_game_summary["Porcentaje"] > 75]
    delete_columns = list(null_75.index)
    game_summary.drop(columns=delete_columns, inplace=True)
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM Game", con=engine)
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    game_summary = game_summary[game_summary['game_id'].isin(game['game_id']) &
                                game_summary['home_team_id'].isin(team['id']) & 
                                game_summary['visitor_team_id'].isin(team['id'])]
    game_summary.drop_duplicates(subset=["game_id"], inplace=True)
    return game_summary

def procesar_other_stats(file_path):
    other_stats = pd.read_csv(file_path)
    delete_columns = ['league_id']
    other_stats.drop(delete_columns, axis=1, inplace=True)
    other_stats.dropna(subset=['team_turnovers_home', 'total_turnovers_home', 
                               'team_rebounds_home', 'pts_off_to_home', 
                               'team_turnovers_away', 'total_turnovers_away', 
                               'team_rebounds_away', 'pts_off_to_away'], inplace=True)
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM Game", con=engine)
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    other_stats = other_stats[other_stats['game_id'].isin(game['game_id']) 
                              & other_stats['team_id_home'].isin(team['id']) 
                              & other_stats['team_id_away'].isin(team['id'])]
    return other_stats

def procesar_officials(file_path):
    officials = pd.read_csv(file_path)
    officials.drop(['jersey_num'], axis=1, inplace=True)
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM Game", con=engine)
    officials = officials[officials['game_id'].isin(game['game_id'])]
    return officials

def procesar_inactive_players(file_path):
    inactive_players = pd.read_csv(file_path)
    inactive_players.dropna(subset=['first_name', 'last_name'], inplace=True)
    delete_columns = ['jersey_num']
    inactive_players.drop(delete_columns, axis=1, inplace=True)
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM Game", con=engine)
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    player = pd.read_sql("SELECT * FROM Player", con=engine)
    inactive_players = inactive_players[inactive_players['game_id'].isin(game['game_id']) &
                                        inactive_players['team_id'].isin(team['id']) & 
                                        inactive_players['player_id'].isin(player['id'])]
    return inactive_players


def procesar_play_by_play(file_path):
    play_by_play = pd.read_csv(file_path)
    play_by_play.drop(["video_available_flag"], axis=1, inplace=True)
    play_by_play_qt4 = play_by_play[play_by_play["period"].isin([4])]
    # Convertir "pctimestring" a segundos para facilitar la comparación
    play_by_play_qt4 = play_by_play_qt4.copy()  # Create a copy to avoid the warning
    play_by_play_qt4["pctimestring"] = play_by_play_qt4["pctimestring"].astype(str).apply(
        lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1]) if ":" in x else None
    )
    # Filtrar las jugadas en los últimos 5 minutos (300 segundos)
    play_by_play_clutch = play_by_play_qt4[play_by_play_qt4["pctimestring"] <= 300].copy()
    # Convertir de vuelta "pctimestring" a formato m:ss
    play_by_play_clutch["pctimestring"] = play_by_play_clutch["pctimestring"].apply(
        lambda x: f"{x // 60}:{x % 60:02d}" if pd.notnull(x) else None
    )
    delete_columns = ["person1type", "player1_name", "player1_team_city", "player1_team_nickname", 
                      "player1_team_abbreviation", "person2type", "player2_name", "player2_team_city", 
                      "player2_team_nickname", "player2_team_abbreviation", "person3type", "player3_name", 
                      "player3_team_city", "player3_team_nickname", "player3_team_abbreviation","eventnum",
                      "period", "wctimestring"]
    play_by_play_clutch.drop(delete_columns, axis=1, inplace=True) 
    play_by_play_clutch[['player1_id', 'player2_id', 'player3_id']] = play_by_play_clutch[['player1_id', 
                                         'player2_id', 'player3_id']].replace(0, np.nan)
    
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM Game", con=engine)
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    player = pd.read_sql("SELECT * FROM Player", con=engine)
    play_by_play_clutch_final = play_by_play_clutch[
    play_by_play_clutch['game_id'].isin(game['game_id']) &

    (play_by_play_clutch['player1_id'].isna() | play_by_play_clutch['player1_id'].isin(player['id'])) &
    (play_by_play_clutch['player2_id'].isna() | play_by_play_clutch['player2_id'].isin(player['id'])) &
    (play_by_play_clutch['player3_id'].isna() | play_by_play_clutch['player3_id'].isin(player['id'])) &

    (play_by_play_clutch['player1_team_id'].isna() | play_by_play_clutch['player1_team_id'].isin(team['id'])) &
    (play_by_play_clutch['player2_team_id'].isna() | play_by_play_clutch['player2_team_id'].isin(team['id'])) &
    (play_by_play_clutch['player3_team_id'].isna() | play_by_play_clutch['player3_team_id'].isin(team['id']))
]
    return play_by_play_clutch_final
    
def procesar_line_score(file_path):
    line_score = pd.read_csv(file_path)
    line_score = line_score[line_score['game_date_est'] >= "2000-01-01"].copy()
    null_line_score = line_score.isnull().sum()
    total_register = len(line_score)
    null_result = null_line_score[null_line_score > 0]
    df_null_line_score = pd.DataFrame(
        {
            "Valores nulos": null_result,
            "Total registros": total_register,
            "Porcentaje": (null_result / total_register * 100).round(2),
        }
    )
    null_50 = df_null_line_score[df_null_line_score["Porcentaje"] > 50]
    delete_columns = list(null_50.index)
    line_score.drop(columns=delete_columns, inplace=True)
    line_score.fillna(0, inplace=True)
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM Game", con=engine)
    team = pd.read_sql("SELECT * FROM Team", con=engine)
    line_score = line_score[line_score['game_id'].isin(game['game_id']) 
                            & line_score['team_id_home'].isin(team['id']) 
                            & line_score['team_id_away'].isin(team['id'])]
    return line_score



# Monitoreo de archivos
class Watcher:
    directory_to_watch = DIRECTORY
    
    def __init__(self):
        self.observer = Observer()
        
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        # Inicio del observador
        self.observer.start()
        try:
            # Bucle infinito para mantener el programa en ejecución
            while True:
                # Pausa de 1 segundo para evitar un uso excesivo de la CPU
                time.sleep(5)
        except KeyboardInterrupt:
            # Detener el observador si se detecta una interrupción del teclado (Ctrl + C)
            self.observer.stop()
        # Esperar a que el observador termine antes de salir del programa
        self.observer.join()
        
class Handler(FileSystemEventHandler):
    processed_files = {}
    
    @staticmethod
    def on_modified(event):
        # Verificar si el evento corresponde a un directorio
        if event.is_directory:
            return None
        # Verificar si el evento es una modificación de archivo
        elif event.event_type == 'modified' and event.src_path.endswith('.csv'):
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            current_time = time.time()
            print(f'⚠️ Monitoreando archivos en el directorio: {DIRECTORY}')
            
             # Si fue procesado hace menos de 10 segundos, lo ignoramos
            if file_name in Handler.processed_files:
                last_time = Handler.processed_files[file_name]
                if current_time - last_time < 10:
                    return
            
            # Llama a la función de limpieza/carga correspondiente
            if file_name == 'common_player_info.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_common_player_info(file_path)
            elif file_name == 'draft_combine_stats.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_draft_combine_stats(file_path)
            elif file_name == 'draft_history.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_draft_history(file_path)
            elif file_name == 'game_info.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_game_info(file_path)
            elif file_name == 'game_summary.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_game_summary(file_path)
            elif file_name == 'game.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_game(file_path)
            elif file_name == 'inactive_players.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_inactive_players(file_path)
            elif file_name == 'line_score.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_line_score(file_path)
            elif file_name == 'officials.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_officials(file_path)
            elif file_name == 'other_stats.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_other_stats(file_path)
            elif file_name == 'play_by_play.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_play_by_play(file_path)
            elif file_name == 'player.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_player(file_path)
            elif file_name == 'team_details.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_team_details(file_path)
            elif file_name == 'team_history.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_team_history(file_path)
            elif file_name == 'team.csv':
                print(f'👀 Modificación en archivo: {file_name}')
                print(f'📦🔺 Procesando archivo: {file_name}')
                df = procesar_team(file_path)
           
            
            if df is not None:
                # Cargar el df a SQL Server
                cargar_a_sql(df, file_name)
                current_time = time.time()
                Handler.processed_files[file_name] = current_time
                # Mover el archivo procesado
                #mover_archivo_procesado(file_name, file_path)
                 
        
if __name__ == '__main__':
    # Crear una instancia de la clase Watcher y ejecutar el método run()
    w = Watcher()
    w.run()
    
