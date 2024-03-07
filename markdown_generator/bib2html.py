# a python script to turn a bib file into html files

from pybtex.database.input import bibtex
import pybtex.database.input.bibtex 
import math 
import os


html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


def e(text):
    return( text!="");


def get( b, mess, key ):
    out = ""
    try : 
        out = b[key]
    except:
        mess = mess + " missing " + key
    return out, mess


def get_title( b, mess ):
    pub_title = ""
    try:
        pub_title = html_escape(b["title"].replace("{", "").replace("}","").replace("\\","")) 
    except:
        mess = mess + " missing title"
    return pub_title, mess


def get_journal( b, mess ):
    pub_journal = ""
    try:
        pub_journal = b["journal"].replace("{", "").replace("}","")
    except:
        mess = mess + " missing journal"
    return pub_journal, mess    
    

def get_names( b, mess, key ):
    out = ""
    try:
        for dude in b.persons[key]:
            out = out + " " + dude.first_names[0] + " " + dude.last_names[0]+", "
    except:
        mess = mess + " missing " + key
    return out, mess


def populate_header( nm, f, unique_years, unique_types):
    f.write('\n---');
    f.write('\nlayout: archive');
    f.write('\ntitle: "' + str(nm) + '"');
    f.write('\npermalink: ' + str(nm) + '/');
    f.write('\nauthor_profile: true');
    f.write('\n---');
    f.write('\n');

    f.write('\n<center>')
    f.write('\n<a href="complete-bibliography.md"><button type="button" class="btn" style="outline:none"> all </button></a>')
    for typ in unique_types:
        f.write('\n<a href="' + typ + '.md"><button type="button" class="btn" style="outline:none"> ' + typ + '</button></a>')
    f.write('\n</center>')

    f.write("\n<br><br>")
    f.write('\n<center>')

    i=0
    for year in unique_years:
        if i==math.ceil( len(unique_years)/3 ) :
            f.write("<br><br>")
            i=0
        f.write('\n<a href="' + year + '.md"><button type="button" class="btn" style="outline:none"> ' + year + '</button></a>')
        i=i+1
    f.write("\n<br><br>")
    f.write('\n</center>')

    f.write('\n<ol id = "reverse_numbering">')



def write_item( f, item ):
    f.write("\n<li>")
    f.write('\n' + item)
    f.write("\n</li>")
    f.write("\n<br>")


def populate_footer( f ):
    f.write('\n</ol>')
    f.write('\n<script type="text/javascript">');
    f.write("\nvar reverse=document.getElementById('reverse_numbering');");
    f.write("\nreverse.style.listStyle='none';");
    f.write("\nreverse.style.textIndent='-23px';");
    f.write("\nvar li=reverse.getElementsByTagName('li');");
    f.write("\nfor(var i=0; i<li.length; i++){");
    f.write("\nli[i].insertBefore(document.createTextNode(li.length-i+'. '), li[i].firstChild);}");
    f.write("\n</script>");

    f.write("\n<u><b>Disclaimer:</b></u><br><br>");
    f.write("\n<p><em>");
    f.write("""\nThis material is presented to ensure timely dissemination of scholarly and 
        technical work. Copyright and all rights therein are retained by authors or by other copyright holders.
        All person copying this information are expected to adhere to the terms and constraints invoked by each 
        author's copyright. In most cases, these works may not be reposted without the explicit permission of 
        the copyright holder.""");
    f.write("\n</em></p>\n<p><em>");
    f.write("""\nSome of these documents are (c) IEEE. Personal use of this material is permitted. However, 
        permission to reprint/republish this material for advertising or promotional purposes or for creating 
        new collective works for resale or redistribution to servers or lists, or to reuse any copyrighted
        component of this work in other works must be obtained from the IEEE.""");
    f.write("""\nOther documents are (c) SPIE. These documents are made available as an electronic reprint with 
        permission of SPIE. One print or electronic copy may be made for personal use only. Systematic or multiple 
        reproduction, distribution to multiple locations via electronic or other means, duplication of any material 
        in this paper for a fee or for commercial purposes, or modification of the content of the paper are prohibited""")
    f.write("\n</em></p>");
    f.write('\n</body>')
    f.write('\n</html>')


def main():

    fname = '.github/workflows/kreucher.bib';
    parser = bibtex.Parser()
    bibdata = parser.parse_file(fname)


    entries = list()
    all_years = list()
    all_types = list()


    for bib_id in bibdata.entries:
        
        article_type = bibdata.entries[bib_id].type;
        b = bibdata.entries[bib_id].fields
        ba = bibdata.entries[bib_id]
        mess = "";

        if article_type.upper() == "JOURNAL":

            auth, mess      = get_names(ba, mess, "author")
            title, mess     = get_title(b, mess)
            journal, mess   = get_journal(b, mess)
            volume, mess    = get(b, mess, "volume")
            number, mess    = get(b, mess, "number")
            pages, mess     = get(b, mess, "pages")
            month, mess     = get(b, mess, "month")
            year, mess      = get(b, mess, "year")
            www, mess       = get(b, mess, "url")
            pdf, mess       = get(b, mess, "pdf")

            out_string = auth + '<b>' + title + '</b>. <em>' + journal + '</em>, ' + volume + \
                '(' + number + '): ' + pages + ', ' + month + ' ' + year + '. ' 
            if not (www==""): out_string = out_string + '[<a href = "http://' + www + '">WWW</a>] '
            out_string = out_string + '[<a href="' + pdf + '">PDF</a>]'

            entries.append( out_string )
            all_years.append(year)
            all_types.append(article_type)

            if e(mess):
                print("\n" + str(bib_id) + "  " + mess, end="" );


        elif article_type.upper() == "CONFERENCE":
            auth, mess      = get_names(ba, mess, "author")
            title, mess     = get_title(b, mess)
            month, mess     = get(b, mess, "month")
            year, mess      = get(b, mess, "year")
            booktitle, mess = get(b, mess, "booktitle")
            www, mess       = get(b, mess, "url")
            pdf, mess       = get(b, mess, "pdf")
            pages, mess     = get(b, mess, "pages")
            location, mess  = get(b, mess, "location")

            out_string = auth + '<b>' + title + '</b>. <em>' + booktitle + \
                    '</em>, Pages ' + pages + ', ' + month + ' ' + year + '. ' 
            if not (www==""): out_string = out_string + '[<a href = "http://' + www + '">WWW</a>] '
            if not (pdf==""): out_string = out_string + '[<a href="' + pdf + '">PDF</a>]'
            
            entries.append( out_string )
            all_years.append(year)
            all_types.append(article_type)

            if e(mess):
                print("\n" + str(bib_id) + "  " + mess, end="" );                


        elif article_type.upper() == "BOOKCHAPTER":
            auth, mess      = get_names(ba, mess, "author")
            title, mess     = get_title(b, mess)
            editors, mess   = get_names(ba, mess, "editor")
            booktitle, mess = get(b, mess, "booktitle")
            chapter, mess   = get(b, mess, "chapter")
            pages, mess     = get(b, mess, "pages")
            publisher, mess = get(b, mess, "publisher")
            month, mess     = get(b, mess, "month")
            year, mess      = get(b, mess, "year")
            www, mess       = get(b, mess, "url")
            pdf, mess       = get(b, mess, "pdf")

            out_string = auth + '<b>' + title + '</b>.' + editors + 'editors, <em>' + \
                    booktitle + '</em>, Chapter ' + chapter + ', Pages ' + pages + \
                    '. ' + publisher + ', ' + month + ' ' + year + '. '
            if not (www==""): out_string = out_string + '[<a href = "http://' + www + '">WWW</a>] '
            out_string = out_string + '[<a href="' + pdf + '">PDF</a>]'

            entries.append( out_string )
            all_years.append(year)
            all_types.append(article_type)

            if e(mess):
                print("\n" + str(bib_id) + "  " + mess, end="" );


        elif article_type.upper() == "THESIS":
            auth, mess      = get_names(ba, mess, "author");
            title, mess     = get_title(b, mess);
            month, mess     = get(b, mess, "month")
            year, mess      = get(b, mess, "year")
            www, mess       = get(b, mess, "url")
            pdf, mess       = get(b, mess, "pdf")
            school, mess    = get(b, mess, "school");
            typ, mess       = get(b, mess, "type");

            out_string = auth + '<b>' + title + '</b> ' + typ + ' ' \
                    + school + ' ' +  month + ' ' + year + '. '
            if not (www==""): out_string = out_string + '[<a href = "http://' + www + '">WWW</a>] '
            out_string = out_string + '[<a href="' + pdf + '">PDF</a>]'

            entries.append( out_string )
            all_years.append(year)
            all_types.append(article_type)

            if e(mess):
                print("\n" + str(bib_id) + "  " + mess, end="" );
        else:
            print( article_type + " is not known");


    # get the unique types and years
    all_years.sort()
    list_set = set( all_years )
    unique_years = (list(list_set))
    unique_years.sort(reverse=True)
  
    list_set = set( all_types )
    unique_types = (list(list_set))
    unique_types.sort()


    # write the entire bibliography
    fname_html = '_pages/complete-bibliography.md'
    all_html = open(fname_html,'w')
    populate_header('complete-bibliography', all_html, unique_years, unique_types)
    for i in range(0,len(entries)):        
        write_item(all_html, entries[i])
    populate_footer( all_html )
    all_html.close()


    # write individual per-year htmls
    for year in unique_years:
        fname = './_pages/' + str(year)+'.md'        
        year_html = open( fname ,'w' )
        populate_header(str(year), year_html, unique_years, unique_types)

        for i in range(0,len(all_years)):
            if( all_years[i] == year): write_item( year_html, entries[i])

        populate_footer( year_html )
        year_html.close()



    # write individual per-type htmls
    for typ in unique_types:
        fname = "./_pages/" + str(typ) + ".md"       
        typ_html = open( fname ,'w' )
        populate_header(str(typ), typ_html, unique_years, unique_types)

        for i in range(0,len(all_types)):
            if( all_types[i] == typ): write_item( typ_html, entries[i])

        populate_footer( typ_html )
        typ_html.close()




if __name__ == '__main__':
  main();
  
