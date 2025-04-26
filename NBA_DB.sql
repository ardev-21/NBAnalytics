CREATE TABLE Player (
id INT PRIMARY KEY,
full_name varchar(101),
first_name varchar(50),
last_name varchar(50)
)


CREATE TABLE Team (
id INT PRIMARY KEY,
full_name varchar(50),
abbreviation char(3),
nickname varchar(25),
city varchar(25),
state varchar (30),
year_founded int
)


CREATE TABLE Game (
season_id int,
team_id_home int FOREIGN KEY REFERENCES Team(id) NOT NULL,
team_abbreviation_home char(3),
team_name_home varchar(50),
game_id int PRIMARY KEY,
game_date DATETIME,
matchup_home varchar(12),
wl_home char(1),
min int,
fgm_home int,
fga_home int,
fg_pct_home DECIMAL(5,3),
fg3m_home int,
fg3a_home int,
fg3_pct_home DECIMAL(5,3),
ftm_home INT,
fta_home INT,
ft_pct_home DECIMAL(5,3),
oreb_home int,
dreb_home int,
reb_home int,
ast_home int,
stl_home int,
blk_home int,
tov_home int,
pf_home int,
pts_home int,
plus_minus_home int,
team_id_away int FOREIGN KEY REFERENCES Team(id) NOT NULL,
team_abbreviation_away char(3),
team_name_away varchar(50),
matchup_away varchar(12),
wl_away char(1),
fgm_away int,
fga_away int,
fg_pct_away DECIMAL(5,3),
fg3m_away int,
fg3a_away int,
fg3_pct_away DECIMAL(5,3),
ftm_away INT,
fta_away INT,
ft_pct_away DECIMAL(5,3),
oreb_away int,
dreb_away int,
reb_away int,
ast_away int,
stl_away int,
blk_away int,
tov_away int,
pf_away int,
pts_away int,
plus_minus_away int,
video_available_away char(1),
season_type varchar(25)
)


CREATE TABLE Common_player_info (

person_id INT PRIMARY KEY FOREIGN KEY REFERENCES Player(id),
first_name varchar(50),
last_name varchar(50),
display_first_last varchar(101),
display_last_comma_first varchar(101),
display_fi_last varchar(53),
player_slug varchar(101),
birthdate DATETIME,
school varchar(45),
country varchar(45),
last_affiliation varchar(45),
height varchar(5),
weight INT,
season_exp INT,
jersey INT,
position varchar(20),
rosterstatus varchar(9),
games_played_current_season_flag INT,
team_id INT FOREIGN KEY REFERENCES Team(id),
team_name varchar(25),
team_abbreviation char(3),
team_code varchar(20),
team_city varchar(25),
player_code varchar(50),
from_year INT,
to_year INT,
dleague_flag CHAR(1),
nba_flag CHAR(1),
games_played_flag CHAR(1),
draft_year VARCHAR(10),
draft_round VARCHAR(10),
draft_number VARCHAR(10),
greatest_75_flag CHAR(1)
)


CREATE TABLE Draft_combine_stats (

season INT,
player_id INT PRIMARY KEY FOREIGN KEY REFERENCES Player(id),
first_name varchar(50),
last_name varchar(50),
player_name varchar(101),
position varchar(5),
height_wo_shoes DECIMAL(6,2),
height_wo_shoes_ft_in varchar(15),
height_w_shoes DECIMAL (6,2),
height_w_shoes_ft_in varchar(15),
weight DECIMAL(5,1),
wingspan DECIMAL(5,2),
wingspan_ft_in varchar(15),
standing_reach DECIMAL (5,1),
standing_reach_ft_in varchar(15),
body_fat_pct DECIMAL(5,2),
hand_lenght DECIMAL(3,1),
hand_width DECIMAL(3,1),
standing_vertical_leap DECIMAL(5,2),
max_vertical_leap DECIMAL(5,2),
lane_agility_time DECIMAL(5,2),
modified_lane_agility_time DECIMAL(5,2),
three_quarter_sprint DECIMAL(4,2),
bench_press INT,
spot_fifteen_corner_left varchar(5),
spot_fifteen_break_left varchar(5),
spot_fifteen_top_key varchar(5),
spot_fifteen_break_right varchar(5),
spot_fifteen_corner_right varchar(5),
spot_college_corner_left varchar(5),
spot_college_break_left varchar(5),
spot_college_top_key varchar(5),
spot_college_break_right varchar(5),
spot_college_corner_right varchar(5),
spot_nba_break_left varchar(5),
spot_nba_top_key varchar(5),
spot_nba_break_right varchar(5),
spot_nba_corner_right varchar(5),
off_drib_fifteen_break_left varchar(5),
off_drib_fifteen_top_key varchar(5),
off_drib_fifteen_break_right varchar(5),
off_drib_college_break_left varchar(5),
off_drib_college_top_key varchar(5),
off_drib_college_break_right varchar(5),
on_move_fifteen varchar(7),
on_move_college varchar(7)
)


CREATE TABLE Draft_history (
person_id INT PRIMARY KEY FOREIGN KEY REFERENCES Player(id),
player_name varchar(51),
season int,
round_number int,
round_pick int,
overall_pick int,
draft_type varchar(12),
team_id int FOREIGN KEY REFERENCES Team(id),
team_city varchar(25),
team_name varchar(25),
team_abbreviation char(3),
organization varchar(50),
organization_type varchar(50),
player_profile_flag int
)


CREATE TABLE Team_details (
team_id INT PRIMARY KEY FOREIGN KEY REFERENCES Team(id),
abbreviation char(3),
nickname varchar(25),
yearfounded INT,
city varchar(25),
arena varchar(50),
arenacapacity INT,
owner varchar(50),
generalmanager varchar(50),
headcoach varchar(50),
dleagueaffiliation varchar(65),
facebook nvarchar(255),
instagram nvarchar(255),
twitter nvarchar(255),
)


CREATE TABLE Team_history(
id_log INT IDENTITY (1,1) PRIMARY KEY,
team_id INT FOREIGN KEY REFERENCES Team(id),
city varchar(50),
nickname varchar(25),
year_founded INT,
year_active_till INT
)


CREATE TABLE Team_info_common(
team_id INT PRIMARY KEY FOREIGN KEY REFERENCES Team(id),
season_year INT,
team_city varchar(25),
team_name varchar(25),
team_abbreviation char(3),
team_conference varchar(15),
team_division varchar(25),
team_code varchar(40),
team_slug varchar(40),
w INT,
l INT,
pct INT,
conf_rank INT,
div_rank INT,
min_year INT,
max_year INT,
league_id INT,
season_id INT,
pts_rank INT,
pts_pg INT,
reb_rank INT,
reb_pg INT,
ast_rank INT,
ast_pg INT,
opp_pts_rank INT,
opp_pts_pg INT
)


CREATE TABLE Game_info (
game_id INT PRIMARY KEY FOREIGN KEY REFERENCES Game(game_id),
game_date DATETIME,
attendance INT,
game_time VARCHAR (25) --NO SE SI ES HORARIO DE PARTIDO O UNA MEDICINO DE TIEMPO ASI QUE NOSE SI DEBERIA IR VARCHAR O TIME
)


CREATE TABLE Game_summary(
game_date_est DATETIME,
game_sequence INT,
game_id INT FOREIGN KEY REFERENCES Game(game_id),
game_status_id INT,
game_status_text varchar(30),
gamecode varchar(25) PRIMARY KEY NOT NULL,
home_team_id INT FOREIGN KEY REFERENCES Team(id),
visitor_team_id INT FOREIGN KEY REFERENCES Team(id),
season INT,
live_period INT,
live_pc_time varchar (10),
natl_tv_broadcaster_abbreviation varchar(15),
live_period_time_bcast varchar(20),
wh_status char(1)
)


CREATE TABLE Other_stats(
game_id INT PRIMARY KEY FOREIGN KEY REFERENCES Game(game_id),
league_id INT,
team_id_home INT FOREIGN KEY REFERENCES Team(id),
team_abbreviation_home char(3),
team_city_home varchar(25),
pts_paint_home INT,
pts_2nd_chance_home INT,
pts_fb_home INT,
largest_lead_home INT,
lead_changes INT,
times_tied INT,
team_turnovers_home INT,
total_turnovers_home INT,
team_rebounds_home INT,
pts_off_to_home INT,
team_id_away INT FOREIGN KEY REFERENCES Team(id),
team_abbreviation_away char(3),
team_city_away varchar(25),
pts_paint_away INT,
pts_2nd_chance_away INT,
pts_fb_away INT,
largest_lead_away INT,
team_turnovers_away INT,
total_turnovers_away INT,
team_rebounds_away INT,
pts_off_to_away INT,
)


CREATE TABLE Officials(
game_id INT PRIMARY KEY FOREIGN KEY REFERENCES Game(game_id),
official_id INT,
first_name varchar(20),
last_name varchar(35),
jersey_num INT
)


CREATE TABLE Inactive_players(
log_id INT PRIMARY KEY IDENTITY(1,1),
player_id INT FOREIGN KEY REFERENCES Player(id),
first_name varchar(25),
last_name varchar(25),
jersey_num INT,
team_id INT FOREIGN KEY REFERENCES Team(id),
team_city varchar(25),
team_name varchar(25),
team_abbreviation char(3)
)


CREATE TABLE Play_by_play(
play_id INT IDENTITY(1,1) PRIMARY KEY,
game_id INT FOREIGN KEY REFERENCES Game(game_id),
eventnum INT,
eventmsgtype INT,
eventmsgactiontype INT,
period INT,
wctimestring TIME,
pctimestring varchar(10),
homedescription varchar(140),
neutraldescription varchar(140),
visitordescription varchar(140),
score varchar(10),
scoremargin INT,
person1type DECIMAL(10,2),
player1_id INT FOREIGN KEY REFERENCES Player(id),
player1_name varchar(25),
player1_team_id INT FOREIGN KEY REFERENCES Team(id),
player1_team_city varchar(25),
player1_team_nickname varchar(25),
player1_team_abbreviation char(3),
person2type DECIMAL(10,2),
player2_id INT FOREIGN KEY REFERENCES Player(id),
player2_name varchar(25),
player2_team_id INT FOREIGN KEY REFERENCES Team(id),
player2_team_city varchar(25),
player2_team_nickname varchar(25),
player2_team_abbreviation char(3),
person3type DECIMAL(10,2),
player3_id INT FOREIGN KEY REFERENCES Player(id),
player3_name varchar(25),
player3_team_id INT FOREIGN KEY REFERENCES Team(id),
player3_team_city varchar(25),
player3_team_nickname varchar(25),
player3_team_abbreviation char(3),
video_available_flag char(1)
)

