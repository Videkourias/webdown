# Contains methods to write data to various text formats
from ebooklib import epub


# Method for epub creation
def createEpub(bodies, titles, info):
    book = epub.EpubBook()

    # set metadata
    # book.set_identifier('id123456')
    book.set_title(info['title'])
    book.set_language('en')
    book.add_metadata('DC', 'description', info['desc'])
    book.add_author(info['author'])

    # Create blank TOC and a spine
    book.toc = []
    book.spine = ['nav']

    # create chapters
    for i in range(len(bodies)):
        chapter = epub.EpubHtml(title=titles[i], file_name='chap_{}.xhtml'.format(i + 1), lang='en')
        chapter.content = bodies[i]

        # add chapter
        book.add_item(chapter)

        # add chapter to table of contents and spine
        book.toc.append(epub.Link('chap_{}.xhtml'.format(i + 1), '{}'.format(titles[i]), '{}'.format(i + 1)))

        book.spine.append(chapter)

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file
    book.add_item(nav_css)

    # write to the file
    epub.write_epub('files/' + info['title'] + '.epub', book, {})


def createTxt():
    pass
