
import subprocess
from subprocess import check_output
import sys
import os
import requests
import fileinput

def install_docker(user):
    subprocess.run(['sudo apt update'], shell=True, check=True)
    #Instalar algunos pre-requisitos para usar los paquetes por HTTPS:
    subprocess.run(['sudo apt install apt-transport-https ca-certificates curl software-properties-common'], shell=True, check=True)
    #Agregar la GPG key para el repositorio oficial de Docker al sistema:
    subprocess.run(['curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -'], shell=True, check=True)
    #Agregar el repositorio de Docker a APT sources:
    subprocess.run(['sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"'], shell=True, check=True)
    #Update
    subprocess.run(['sudo apt update'], shell=True, check=True)
    #Finalmente se instala Docker
    subprocess.run(['sudo apt install docker-ce'], shell=True, check=True)
    #Para evitar escribir sudo cada que se utilice docker agrega el username al docker group
    subprocess.run(['sudo usermod -aG docker ' + user], shell=True, check=True)
    print('Instalacion docker OKAY')
    # subprocess.run(['su - ' + user], shell=True, check=True)
    # print('8')
    # subprocess.run(['id -nG'], shell=True, check=True)
    # print('9')

def install_compose():
    #Checar la ultima versión y actualizar el comando
    subprocess.run(['sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose'], shell=True, check=True)
    #Checar la ultima versión y actualizar el comando
    subprocess.run(['sudo chmod +x /usr/local/bin/docker-compose'], shell=True, check=True)
    #Agregar permisos de docker
    subprocess.run(['docker-compose --version'], shell=True, check=True)
    print('Instalacion Docker-Compose OKAY')

def get_ip():
    subprocess.run(['sudo pip install requests'], shell=True, check=True)
    r = requests.get(r'http://jsonip.com')
    ip= r.json()['ip']
    print(ip)
    return(ip)
    #result = subprocess.run(['curl https://ipinfo.io/ip'], shell=True, check=True, capture_output=True)
    #process = subprocess.run(['curl https://ipinfo.io/ip'], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #output = subprocess.check_output('curl https://ipinfo.io/ip', shell=True)

def replace_file():
    ip = get_ip()
    with fileinput.FileInput("nginx.conf", inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace("__ip__", ip), end='')
    print('---- ip has been replaced correctly -----')

def move_files():
    #get path and introduce files to docker container
    path = os.getcwd()
    subprocess.run(['docker cp %s/html wordpress:/var/www'%path], shell=True, check=True)
    subprocess.run(['docker cp %s/standardDB.sql db:/'%path], shell=True, check=True)
    print('---- html and db files have been replaced -----')

def docker_compose():
    #Crea contenedores de docker
    subprocess.run(['docker-compose up -d'], shell=True, check=True)
    #Estatus de docker
    subprocess.run(['docker-compose ps'], shell=True, check=True)
    print('---- docker containers have been set -----')

def run_dumpsql():
    subprocess.run(['docker exec -t -i db /bin/bash'], shell=True, check=True)
    subprocess.run(['mysql -u admin -p wordpress < standardDB.sql'], shell=True, check=True)
    print("already imported")


def main(argv):
    user = sys.argv[1]
    install_docker(user)
    install_compose()
    replace_file()
    docker_compose()
    move_files()
    run_dumpsql()

if __name__ == "__main__":
    main(sys.argv)
