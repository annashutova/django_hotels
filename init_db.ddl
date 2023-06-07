CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS hotel(
    id uuid primary key default uuid_generate_v4(),
    company text,
    name text not null,
    star_rating int check (0 <= star_rating and star_rating <= 5),
    phone text,
    description text,
    country text not null,
    state text,
    city text not null,
    street text not null,
    building text not null,
    latitude float not null,
    longitude float not null
);

CREATE TABLE IF NOT EXISTS room(
    id uuid primary key default uuid_generate_v4(),
    hotel_id uuid NOT NULL REFERENCES hotel ON DELETE CASCADE,
    type text not null,
    name text NOT NULL,
    code text NOT NULL,
    price decimal NOT NULL CHECK (price > 0),
    capacity int NOT NULL CHECK (capacity > 0),
    double_bed int NOT NULL CHECK (double_bed >= 0),
    single_bed int NOT NULL CHECK (single_bed >= 0),
    area int CHECK (area > 0),
    safe boolean default False,
    tv boolean default False,
    soundproofing boolean default False,
    telephone boolean default False,
    heating boolean default False,
    wardrobe boolean default False,
    shower boolean default False,
    minibar boolean default False,
    air_conditioning boolean default False,
    bath boolean default False,
    desk boolean default False
);

CREATE TABLE IF NOT EXISTS amenity(
    id uuid primary key default uuid_generate_v4(),
    title text NOT NULL
);

CREATE TABLE IF NOT EXISTS hotel_amenity(
    id uuid primary key default uuid_generate_v4(),
    hotel_id uuid NOT NULL REFERENCES hotel ON DELETE CASCADE,
    amenity_id uuid NOT NULL REFERENCES amenity ON DELETE CASCADE,
    price decimal NOT NULL CHECK (price >= 0),
    UNIQUE (hotel_id, amenity_id)
);
