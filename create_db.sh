docker run -d --name hotel_project -p 5400:5432 \
-v $HOME/postgresql/hotels_pr:/var/lib/postgresql/libhotels_prrary_7_1 \
-e POSTGRES_PASSWORD=12345 \
-e POSTGRES_USER=app \
-e POSTGRES_DB=hotels_db \
postgres

psql -h 127.0.0.1 -p 5400 -U app hotels_db -f init_db.ddl
