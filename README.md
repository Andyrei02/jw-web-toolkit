# JW Web Toolkit
Web version for [JW Ministry Toolkit](https://github.com/Andyrei02/jw-ministry-toolkit)
**The JW Ministry Toolkit** is an application designed to make it easier for Jehovah's Witnesses to create forms and spreadsheets. It provides a user-friendly interface to streamline the form creation process and other related tasks.

## Clone this repository to your local machine
```bash
git clone https://github.com/Andyrei02/jw-web-toolkit
cd jw-web-toolkit
```
## Usage
- Build / Run docker container
```bash
docker build -t jw-web-toolkit .
docker run -p 5000:5000 -e DATABASE_URL="sqlite:///app.db" jw-web-toolkit
```
- Stop docker container:
```bash
docker stop jw-web-toolkit
docker rm jw-web-toolkit
```
- See active containers:
```bash
docker ps
```

## Create the database
```bash
flask shell
>>> from app.extensions import db
>>> db.create_all()
```

## Migration Commands
```bash
flask db init  # Run this only if you haven't initialized migrations
flask db migrate -m "comment"
flask db upgrade
```

## To Do
- resolve bug with incorect show style
- show selected tabs
- add table in db for save curent sesion
- Admin panel
- Login / Signin 

## Author

(2025) Andrei Cenusa


## License

[MIT](https://choosealicense.com/licenses/mit/)
