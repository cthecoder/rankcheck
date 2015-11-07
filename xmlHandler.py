#!/usr/bin/env python3



__author__ = 'Christoph'

"""
...
"""
from xml.dom.minidom import *

dateiname = "data/book.xml"
# Aufruf mit komplettem Pfad
def read(dateiname):
    fullnamelist = []
    titlelist = []
    formatlist = []
    isbnlist = []
    booklist = []

    # parse erledigt die umwandlung in ein xml object
    content = parse(dateiname)

    # Erzeugung der Listen aus den XML Nodes
    for lastname in content.getElementsByTagName("author_name"):
        fullnamelist.append(lastname.firstChild.data)

    for title in content.getElementsByTagName("title"):
        titlelist.append(title.firstChild.data)

    for format in content.getElementsByTagName("format"):
        formatlist.append(format.firstChild.data)

    for isbn_number in content.getElementsByTagName("url_isbn"):
        isbnlist.append(isbn_number.firstChild.data)

    # Erzeugung der gepaarten Namensliste

    listlength = len(fullnamelist)
    for i in range(listlength):
        dataset = [fullnamelist[i], titlelist[i], formatlist[i], isbnlist[i]]
        booklist.append(dataset)
        dataset = []
    return booklist

def write(booklist):

    # erstelle das XML Dokument
    doc = Document()
    # root-Element
    data = doc.createElement('data')
    doc.appendChild(data)

    # Erstelle XML-Struktur und Inhalte; item[0] = domainanme, item[1] = zugehörige settings
    for book in booklist:

        # Elementknoten 'set' für jedes Domain-Setting-Paar
        book_e = doc.createElement('book')
        data.appendChild(book_e)

        # Elementknoten und Textknoten dazu
        author_name_e_node = doc.createElement('author_name')
        book_e.appendChild(author_name_e_node)
        author_name_t_node = doc.createTextNode(book[0])
        author_name_e_node.appendChild(author_name_t_node)

        title_e_node = doc.createElement('title')
        book_e.appendChild(title_e_node)
        title_t_node = doc.createTextNode(book[1])
        title_e_node.appendChild(title_t_node)

        format_e_node = doc.createElement('format')
        book_e.appendChild(format_e_node)
        format_t_node = doc.createTextNode(book[2])
        format_e_node.appendChild(format_t_node)

        isbn_e_node = doc.createElement('url_isbn')
        book_e.appendChild(isbn_e_node)
        isbn_t_node = doc.createTextNode(str(book[3]))
        isbn_e_node.appendChild(isbn_t_node)


    #print(doc.toprettyxml())

    # neues XML in Datei speichern mit minidom methode / falls Datei nicht existiert, wird sie erzeugt
    # enconding in windowscp1252 (auch diese datei), da bei UTF8 die umlaute/sonderzeichen nicht korrekt ins
    # xml geschrieben werden (warum auch immer -??
    doc.writexml(open("data/books.xml", 'w'),
                 indent = "  ",
                 addindent = "  ",
                 newl = '\n',
                 encoding = 'cp1252',
                )