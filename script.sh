#!/bin/bash

#Atualização
apt-get -y update

#Instalação do pip
apt-get install python3-pip

#Instalação da versão 1.7.7 do django
DJANGO_VERSION=1.7.7
pip3 install Django==$DJANGO_VERSION

#Instalação e configuração do banco de dados (PostgreSQL)
apt-get install postgresql postgresql-contrib
-i -u postgres
createuser -drlP kanjam
psql
create database kanjam with owner kanjam;

#Instalação dos demais módulos
apt-get install python3-psycopg2
pip3 install django-bootstrap3==6.2.2
pip3 install django-foundation
pip3 install django-zurb-foundation

#Instalação do github e sublimetext
apt-get install -y git
add-apt-repository ppa:webupd8team/sublime-text-3
apt-get update
apt-get install sublime-text-installer

#Clonagem do repositório EqLibra
mkdir Eqlibra
cd Eqlibra
git clone https://github.com/DAS1-2016/Finpy.git