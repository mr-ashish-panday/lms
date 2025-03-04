-- database.sql

-- Create the database
CREATE DATABASE IF NOT EXISTS library_db;

-- Use the database
USE library_db;

-- Create the Author table
CREATE TABLE Author (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    AuthorName VARCHAR(255) NOT NULL,
    AuthorBio TEXT
);

-- Create the Book table
CREATE TABLE Book (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    ISBN VARCHAR(255) UNIQUE NOT NULL,
    Title VARCHAR(255) NOT NULL,
    PublicationYear INT,
    Genre VARCHAR(50),
    Publisher VARCHAR(100),
    Edition VARCHAR(50),
    NumberOfCopies INT DEFAULT 1
);

-- Create the Member table
CREATE TABLE Member (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    ContactNumber VARCHAR(20),
    Email VARCHAR(255)
);

-- Create the Book_Author linking table
CREATE TABLE Book_Author (
    BookID INT,
    AuthorID INT,
    PRIMARY KEY (BookID, AuthorID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID)
);

-- Create the Borrowing table
CREATE TABLE Borrowing (
    BorrowingID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    MemberID INT,
    BorrowDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FineAmount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
);

-- Show tables (for verification)
SHOW TABLES;

-- Insert Authors
INSERT INTO Author (AuthorName, AuthorBio) VALUES
('Jane Austen', 'English novelist known for her romantic fiction.'),
('George Orwell', 'English novelist and essayist, known for his dystopian works.'),
('J.R.R. Tolkien', 'English writer, poet, philologist, and academic, best known as the author of The Hobbit and The Lord of the Rings.'),
('Agatha Christie', 'English crime novelist, short story writer and playwright.'),
('Stephen King', 'American author of horror, supernatural fiction, suspense, crime, science-fiction, and fantasy novels.'),
('Gabriel Garcia Marquez', 'Colombian novelist, short story writer, screenwriter and journalist.'),
('Haruki Murakami', 'Japanese writer. His novels, essays, and short stories have been bestsellers in Japan as well as internationally.');

-- Insert Books
INSERT INTO Book (ISBN, Title, PublicationYear, Genre, Publisher, Edition, NumberOfCopies, AuthorID) VALUES
('978-0141439518', 'Pride and Prejudice', 1813, 'Romance', 'Penguin Classics', 'Revised', 5, 1),
('978-0451524935', '1984', 1949, 'Dystopian', 'Signet Classics', 'New', 3, 2),
('978-0547928227', 'The Hobbit', 1937, 'Fantasy', 'Houghton Mifflin Harcourt', '75th Anniversary', 7, 3),
('978-0062347970', 'And Then There Were None', 1939, 'Mystery', 'William Morrow', 'First', 4, 4),
('978-1501142970', 'The Shining', 1977, 'Horror', 'Anchor Books', 'Reprint', 2, 5),
('978-0061120084', 'One Hundred Years of Solitude', 1967, 'Magical Realism', 'Harper Perennial', 'Reprint', 5, 6),
('978-0307947711', 'Kafka on the Shore', 2002, 'Magical Realism', 'Vintage', 'First', 3, 7),
('978-0743273565', 'The Da Vinci Code', 2003, 'Thriller', 'Doubleday', 'First', 6, NULL),
('978-0307277671', 'The Girl with the Dragon Tattoo', 2005, 'Thriller', 'Knopf', 'First', 4, NULL);

-- Insert Members
INSERT INTO Member (Name, Address, ContactNumber, Email) VALUES
('John Smith', '123 Main St, Anytown', '555-1234', 'john.smith@example.com'),
('Alice Johnson', '456 Oak Ave, Anytown', '555-5678', 'alice.johnson@example.com'),
('Bob Williams', '789 Pine Ln, Anytown', '555-9012', 'bob.williams@example.com'),
('Carol Davis', '101 Elm St, Anytown', '555-3456', 'carol.davis@example.com'),
('David Lee', '222 Maple Ave, Anytown', '555-7890', 'david.lee@example.com'),
('Emily Brown', '333 Oak St, Anytown', '555-2345', 'emily.brown@example.com');

-- Insert Borrowing Records (PLACEHOLDER BookID and MemberID values - update after running)
INSERT INTO Borrowing (BookID, MemberID, BorrowDate, DueDate, ReturnDate) VALUES
(1, 1, '2024-02-01', '2024-02-15', '2024-02-14'),
(2, 2, '2024-02-05', '2024-02-19', NULL),
(3, 1, '2024-02-08', '2024-02-22', NULL),
(4, 3, '2024-01-25', '2024-02-08', '2024-02-07'),
(5, 4, '2024-01-20', '2024-02-03', '2024-02-10'),
(1, 3, '2024-02-10', '2024-02-24', NULL),
(6, 5, '2024-02-12', '2024-02-26', NULL),
(7, 6, '2024-02-15', '2024-03-01', '2024-02-28');