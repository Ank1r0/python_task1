IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'somedb') 
    CREATE DATABASE somedb;