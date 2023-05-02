CREATE TABLE DayStats (
	id int NOT NULL auto_increment,
    day_and_time date,
    total_steps int,
    calories_burnt int,
    resting_heartrate int,
    active_heartrate int,
    PRIMARY KEY(id)
);



CREATE TABLE Food (
	id int NOT NULL auto_increment,
    day_key int,
    food_name TEXT,
    caloric_value INT,
    protein_value INT,
    fiber_value INT,
    carb_value INT,
    total_fat_value INT,
    PRIMARY KEY(id),
    Foreign key (day_key) references DayStats(id)
    );
    
    