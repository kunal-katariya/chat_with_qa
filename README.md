# chat_with_qa
1. Postgresql Database  :-
    I.	Download and install  Postgresql using this link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
    
    II.	Open Postgres pgAdmin and create server:
    Right-click on the Servers, select Register -> Server 
    
    III.	Configure Following details in server
    In General Tab: 	Name-> chat_with_qa
    In Connection Tab: 	Hostname-> localhost
    			Port->5432
    			Username-> postgres
    
    IV.	Click on Save


2. Backend End - FastAPI:-
    I.	Download and nstall VsCode editor using this link:
    https://code.visualstudio.com/download
    
    II.	Open chat_with_qa folder in vscode
    
    III.	Activate virtual environment using this cmd:
    venv\Scripts\activate
    
    IV.	Install required dependencies using this cmd:
    pip install requirement.txt
    
    V.	Setup dependencies for PostgreSQL: Execute following cmd in terminal
    a.	alembic init alembic
    b.	alembic revision --autogenerate -m "first_migration" 
    c.	alembic upgrade head
    
    VI.	To run the project, give command in terminal
    a.	Python main.py
    
    VII.	To access all API, use this url:
           http://localhost:7000/docs

       
3.	Front End - React:-
    i.	Download and install Nodejs using this link:
    https://nodejs.org/en/download
    
    ii.	Open chatwithqa-frontend folder in Vscode editor 
    
    iii.	Install all the required dependencies follow:-
    a.	npm install react-bootstrap bootstrap
    b.	npm install @mui/material
    c.	npm install react-icons --save
    d.	npm install react-router-dom
    e.	npm install axios
    f.	npm install react-toastify
    
    iv.	To run project, give command in terminal: npm start
