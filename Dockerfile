FROM python:3.12

WORKDIR /usr/local/app

copy . ./py-git

CMD [sh ./py-git/your_program.sh]  
