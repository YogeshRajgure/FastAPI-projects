# Commands to run the project
1. you should be outside the todoapp folder\
e.g. this folder contain our project -> "D:\\FastAPI\\project3" \
this is required because we are using "." for models
command to run the application will look like this
```powershell
D:\FastAPI\project3> pytest
D:\FastAPI\project3> uvicorn ToDoApp.main:app --reload
```


# How to use alembic tool for data migration and keep woth with db changes
following are the popular commands for using alembic

```powershell
# initializes a new generic env
alembic int <folder_name>
# creates a new revision of message
alembic revision -m <message>
# Run our upgrade migration to our database
alembic upgrade <revision number>
#you can also do a downgrade
# run our downgrade migration to our database
alembic downgrade -1
```
these are the files that will be created\
.ini
