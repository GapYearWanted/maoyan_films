headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/81.0.4044.138 '
                  'Safari/537.36 '
}

sql1 = """
    CREATE TABLE maoyanfilms(
    films_id int(16) NOT NULL ,
    films_name VARCHAR (100) NOT NULL,
    films_type VARCHAR (20),
    films_area VARCHAR (20),
    films_duration VARCHAR (30),
    film_first_time VARCHAR (30),
    films_score VARCHAR (15),
    films_comment_num VARCHAR (15),
    films_box_office VARCHAR (15),
    films_director VARCHAR (50),
    films_actor VARCHAR (100),
    films_introduction VARCHAR (1000),
    films_comment VARCHAR (3000),
    PRIMARY KEY (films_id)
    )
"""

sql2 = """
    INSERT INTO maoyanfilms(films_id,films_name,films_type,films_area,films_duration,film_first_time,
                films_score,films_comment_num,films_box_office,films_director,films_actor,films_introduction,films_comment)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

reError = '403 很抱歉，您的访问请求由于过于频繁而被禁止。'