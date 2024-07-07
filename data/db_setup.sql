CREATE DATABASE arosaje;
USE arosaje;

CREATE TABLE Role (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE User (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    disabled BOOLEAN DEFAULT FALSE,
    id_role INT REFERENCES Role(id)
);

CREATE TABLE Listing (
    id SERIAL PRIMARY KEY,
    id_user INT REFERENCES User(id),
    name VARCHAR(255) NOT NULL,
    photo VARCHAR(255),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    description TEXT
);

CREATE TABLE Address (
    id SERIAL PRIMARY KEY,
    street VARCHAR(255) NOT NULL,
    zipcode VARCHAR(20) NOT NULL,
    city VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    listing_id INT REFERENCES Listing(id)
);

CREATE TABLE Proposal (
    id SERIAL PRIMARY KEY,
    id_listing INT REFERENCES Listing(id),
    proposer_id INT REFERENCES User(id),
    proposal_msg TEXT NOT NULL
);

CREATE TABLE Conversation (
    id SERIAL PRIMARY KEY,
    proposal_id INT REFERENCES Proposal(id)
);

CREATE TABLE ConversationMessage (
    id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES Conversation(id),
    sender_id INT REFERENCES User(id),
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Plante (
    id SERIAL PRIMARY KEY,
    photo VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE Post (
    id SERIAL PRIMARY KEY,
    plante_id INT REFERENCES Plante(id),
    user_id INT REFERENCES User(id),
    content TEXT NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
