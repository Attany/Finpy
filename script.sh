#!/bin/bash

#Atualização
apt-get -y update

#Instalação do pip
apt-get -y install python3-pip

#Instalação da versão 1.7.7 do django
pip3 install Django==1.7.7

#Instalação dos demais módulos
apt-get install python3-psycopg2
pip3 install django-bootstrap3==6.2.2
pip3 install django-foundation
pip3 install django-zurb-foundation

#Instalação do github
apt-get install -y git

#Clonagem do repositório EqLibra
mkdir Eqlibra
cd Eqlibra
git clone https://github.com/DAS1-2016/Finpy.git