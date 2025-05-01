import pyodbc
import time
import pandas as pd
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sqlalchemy
from sqlalchemy import create_engine
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
DIRECTORY= 'C:/Users/Desktop/Desktop/Proyecto final Henry/prueba'
PROCESADOS_DIR = os.path.join(DIRECTORY, 'archivos_procesados')

# Asegura que la carpeta 'archivos_procesados' exista
os.makedirs(PROCESADOS_DIR, exist_ok=True)

# conexion y carga a la base de datos
def get_connection():
    connection_string = f"mssql+pyodbc://{USER}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}"
    engine = create_engine(connection_string)
    return engine

def cargar_a_sql(df, nombre_archivo):
    nombre_tabla = nombre_archivo.split('.')[0]
    engine = get_connection()
    df.to_sql(nombre_tabla, con=engine, if_exists='append', index=False)
    print(f"✅ Datos cargados a la tabla {nombre_tabla}")

# Transformacion y limpieza
def procesar_common_player_info(file_path):
    common_player_info = pd.read_csv(file_path)
    common_player_info = common_player_info[common_player_info["to_year"] >= 2000]
    delete_columns = ["first_name", "last_name", "display_first_last", "display_last_comma_first", "player_slug","jersey", "team_name", "team_abbreviation", "team_code", "team_city", "games_played_current_season_flag"]
    common_player_info.drop(delete_columns, axis=1, inplace=True)
    common_player_info = common_player_info.dropna(subset=['height', 'weight', 'draft_number', 'draft_number', 'position'])
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
    delete_columns = ["height_w_shoes", "height_w_shoes_ft_in", "height_wo_shoes_ft_in", "modified_lane_agility_time", "standing_reach_ft_in", "wingspan_ft_in", "hand_length", "hand_width"]
    draft_combine_stats.drop(delete_columns, axis=1, inplace=True)     
    draft_combine_stats = draft_combine_stats.dropna(subset=['height_wo_shoes', 'weight', 'wingspan', 'standing_reach', 'body_fat_pct', 'standing_vertical_leap', 'max_vertical_leap', 'lane_agility_time', 'three_quarter_sprint', 'bench_press'])
    return draft_combine_stats

def procesar_draft_history(file_path):
    draft_history = pd.read_csv(file_path)
    draft_history = draft_history[draft_history["season"] >= 2000]
    draft_history = draft_history.dropna(subset=['organization', 'organization_type'])
    return draft_history
    
def procesar_game_info(file_path):
    game_info = pd.read_csv(file_path)
    game_info_2000_plus = game_info[game_info["game_date"] >= "2000-01-01"]
    delete_columns = ['attendance', 'game_time']
    game_info_2000_plus.drop(delete_columns, axis=1, inplace=True)
    return game_info_2000_plus

def procesar_game_summary(file_path):
    game_summary = pd.read_csv(file_path)
    game_summary = game_summary[game_summary["game_date_est"] >= "2000-01-01"]
    null_game_summary = game_summary.isnull().sum()
    total_register = len(game_summary)
    null_result = null_game_summary[null_game_summary > 0]

    df_null_game_summary = pd.DataFrame({
        "Valores nulos": null_result,
        "Total registros": total_register,
        "Porcentaje": (null_result / total_register * 100).round(2)
    })

    df_null_game_summary
    null_75 = df_null_game_summary[df_null_game_summary["Porcentaje"] > 75]
    delete_columns = list(null_75.index)
    game_summary.drop(columns=delete_columns, inplace=True)
    return game_summary

def procesar_game(file_path):
    game = pd.read_csv(file_path)
    game = game[game['game_date'] >= "2000-01-01"]
    game.fillna(0, inplace=True)
    return game

def procesar_inactive_players(file_path):
    inactive_players = pd.read_csv(file_path)
    engine = get_connection()
    game = pd.read_sql("SELECT * FROM game_info", con=engine)
    inactive_players = inactive_players[inactive_players['game_id'].isin(game['game_id'])]
    inactive_players.dropna(subset=['first_name', 'last_name'], inplace=True)
    delete_columns = ['jersey_num']
    inactive_players.drop(delete_columns, axis=1, inplace=True)
    return inactive_players

def procesar_line_score(file_path):
    line_score = pd.read_csv(file_path)
    line_score = line_score[line_score['game_date_est'] >= "2000-01-01"]
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
    return line_score

def procesar_officials(file_path):
    officials = pd.read_csv(file_path)
    officials.drop(['jersey_num'], axis=1, inplace=True)
    return officials

def procesar_other_stats(file_path):
    other_stats = pd.read_csv(file_path)
    delete_columns = ['league_id']
    other_stats.drop(delete_columns, axis=1, inplace=True)
    other_stats.dropna(subset=['team_turnovers_home', 'total_turnovers_home', 
                               'team_rebounds_home', 'pts_off_to_home', 
                               'team_turnovers_away', 'total_turnovers_away', 
                               'team_rebounds_away', 'pts_off_to_away'], inplace=True)
    return other_stats

def procesar_player(file_path):
    player = pd.read_csv(file_path)
    return player

def procesar_team_details(file_path):
    team_details = pd.read_csv(file_path)
    delete_columns = ['facebook', 'instagram', 'twitter']
    team_details.drop(columns=delete_columns, inplace=True)
    team_details["arenacapacity"].fillna(team_details["arenacapacity"].median(), inplace=True)
    team_details.dropna(subset=['headcoach'], inplace=True)
    return team_details

def procesar_team_history(file_path):
    team_history= pd.read_csv(file_path)
    return team_history

def procesar_team_info_common(file_path):
    team_info_common = pd.read_csv(file_path)
    return team_info_common

def procesar_team(file_path):
    team = pd.read_csv(file_path)
    return team

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
    delete_columns = ["person1type", "player1_name", "player1_team_city", "player1_team_nickname", "player1_team_abbreviation", "person2type", "player2_name", "player2_team_city", "player2_team_nickname", "player2_team_abbreviation", "person3type", "player3_name", "player3_team_city", "player3_team_nickname", "player3_team_abbreviation"]
    play_by_play_clutch.drop(delete_columns, axis=1, inplace=True) 
    delete_columns = ["eventnum", "period", "wctimestring"]
    play_by_play_clutch.drop(delete_columns, axis=1, inplace=True)
    return play_by_play_clutch
    
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
                time.sleep(1)
        except KeyboardInterrupt:
            # Detener el observador si se detecta una interrupción del teclado (Ctrl + C)
            self.observer.stop()
        # Esperar a que el observador termine antes de salir del programa
        self.observer.join()
        
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        # Verificar si el evento corresponde a un directorio
        if event.is_directory:
            return None
        # Verificar si el evento es una modificación de archivo
        elif event.event_type == 'modified' and event.src_path.endswith('.csv'):
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            
            # Llama a la función de limpieza/carga correspondiente
            if file_name == 'common_player_info.csv':
                df = procesar_common_player_info(file_path)
            elif file_name == 'draft_combine_stats.csv':
                df = procesar_draft_combine_stats(file_path)
            elif file_name == 'draft_history.csv':
                df = procesar_draft_history(file_path)
            elif file_name == 'game_info.csv':
                df = procesar_game_info(file_path)
            elif file_name == 'game_summary.csv':
                df = procesar_game_summary(file_path)
            elif file_name == 'game.csv':
                df = procesar_game(file_path)
            elif file_name == 'inactive_players.csv':
                df = procesar_inactive_players(file_path)
            elif file_name == 'line_score.csv':
                df = procesar_line_score(file_path)
            elif file_name == 'officials.csv':
                df = procesar_officials(file_path)
            elif file_name == 'other_stats.csv':
                df = procesar_other_stats(file_path)
            elif file_name == 'play_by_play.csv':
                df = procesar_play_by_play(file_path)
            elif file_name == 'player.csv':
                df = procesar_player(file_path)
            elif file_name == 'team_details.csv':
                df = procesar_team_details(file_path)
            elif file_name == 'team_history.csv':
                df = procesar_team_history(file_path)
            elif file_name == 'team_info_common.csv':
                df = procesar_team_info_common(file_path)
            elif file_name == 'team.csv':
                df = procesar_team(file_path)
           
            
            if df is not None:
                # Cargar el df a SQL Server
                cargar_a_sql(df, file_name)
                # Mover el archivo procesado
                nuevo_path = os.path.join(PROCESADOS_DIR, file_name)
                shutil.move(file_path, nuevo_path)
                print(f"📦 Archivo movido a {nuevo_path}")   
        
if __name__ == '__main__':
    # Crear una instancia de la clase Watcher y ejecutar el método run()
    w = Watcher()
    w.run()