###		Latex for 42School .PDF

## Base image Ubuntu 14.04
FROM ubuntu:14.04

MAINTAINER Jean-Jacques MOIROUX <jjmoiroux@gmail.com>

RUN apt-get update
RUN apt-get install texlive-latex-base

# Probleme de package langue
RUN apt-get install texlive-lang-french

# ! LaTeX Error: File `xcolor.sty' not found.
RUN apt-get install latex-xcolor texlive-fonts-recommended

# ! LaTeX Error: File `ifplatform.sty' not found.
RUN apt-get install texlive-latex-extra

#! Package minted Error: You must have `pygmentize' installed to use this package.
RUN apt-get install python-pygmen

# Clean up APT when done.
RUN apt-get clean ; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## install RVM && ruby 2.1.2
RUN /bin/bash -l -c  "command curl -sSL https://rvm.io/mpapis.asc | gpg --import -"
RUN \curl -sSL https://get.rvm.io | bash -s stable
RUN /bin/bash -l -c "rvm requirements"
RUN /bin/bash -l -c "rvm install 2.1.2"
RUN /bin/bash -l -c "gem install bundler"
RUN /bin/bash -l -c "rvm use 2.1.2 --default"
