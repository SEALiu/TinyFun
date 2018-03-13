#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import re
import os
import urllib.error
#
from httplite import HttpLite


def fixfile(file):
    for r in ('\n', ':', ','):
        file = file.split(r, 1)[0]
    for r in ('\n', ':', '\"', '\\', '/', '*', '?', '<', '>', '|'):
        file = file.replace(r, '_')
    return file


def fixpath(path):
    for r in ('\n', ':', '\"', '\\', '/', '*', '?', '<', '>', '|'):
        path = path.replace(r, '_')
    return path


def downloadris(root, urls):

    myHttp = HttpLite()

    # flog = codecs.open(root + ".err", "w", "utf8")

    count = len(urls)
    for (i, url) in enumerate(urls):

        path = root + '/'
        if not os.path.exists(path):
            os.makedirs(path)

        again = 10
        while again > 0:
            try:
                print("@processing '%s' [%d/%d]" % (url[0], i + 1, count))

                myHttp.download(
                    url[0],
                    '{0}{1} {2}.ris'.format(path, i + 1, fixfile(url[1])))

            except:
                info = sys.exc_info()
                print('!!! %s, %s' % (info[0], info[1]))
                again = again - 1
            else:
                break

        # if again == 0:
        #    flog.write('{0} \r\n'.format(url))

    # flog.close()
    return '200'


def downloadpdf(root, urls):

    myHttp = HttpLite()

    count = len(urls)
    for (i, (url, tit)) in enumerate(urls):

        path = root + '/'
        if not os.path.exists(path):
            os.makedirs(path)

        again = 10
        while again > 0:
            try:
                print("@processing '%s' [%d/%d]" % (url, i + 1, count))
                proctime = time.clock()

                myHttp.download(
                    url, path + '{0} {1}.pdf'.format(i + 1, fixfile(tit)))

                proctime = time.clock() - proctime
                if proctime < 10:
                    time.sleep(10 - proctime)

            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return '404'
            except:
                info = sys.exc_info()
                print('!!! %s, %s' % (info[0], info[1]))
                again = again - 1
            else:
                break

    return '200'


def downloadacm(root, urls):

    myHttp = HttpLite()

    # flog = codecs.open(root + ".err", "w", "utf8")
    # fabs = codecs.open(root + ".txt", "w", "utf8")

    count = len(urls)
    for (i, url) in enumerate(urls):

        path = root + '/'
        if not os.path.exists(path):
            os.makedirs(path)

        again = 10
        while again > 0:
            try:
                print("@processing '%s' [%d/%d]" % (url, i + 1, count))
                proctime = time.clock()

                # abstract = get_acm_abstract(url)

                content = myHttp.get(url)

                m = re.match(
                    r'[\w|\W]*?<title>([\w|\W]*?)</title>[\w|\W]*?'
                    '"FullText PDF" href="([\w|\W]*?)"[\w|\W]*?',
                    content)

                if m is None:
                    print('No pdf found!')
                    break

                v = re.match(
                    r'[\w|\W]*?&CFID=(\d*)&CFTOKEN=(\d*)[\w|\W]*?', m.group(2))

                print('CFID=%s, CFTOKEN=%s' % (v.group(1), v.group(2)))

                myHttp.download(
                    'https://dl.acm.org/' + m.group(2),
                    path + '{0} {1}.pdf'.format(i + 1, fixfile(m.group(1))))

                '''
                z = re.match(r'[\w|\W]*?/\d*\.\d*/(\d*)\.(\d*)', url)

                myHttp.download(
                    'https://dl.acm.org/downformats.cfm?id={0}&parent_id={1}&'
                    'expformat=endnotes&CFID={2}&CFTOKEN={3}'.format(
                        z.group(2), z.group(1), v.group(1), v.group(2)),
                    path + fixpath('%d %s.enw' % (i + 1, m.group(1))))
                '''

                # fabs.write('{} \r\n'.format(m.group(1)))
                # fabs.write('Abstract: {} \r\n'.format(abstract))
                # fabs.write('\r\n')

                proctime = time.clock() - proctime
                if proctime < 10:
                    time.sleep(10 - proctime)

            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return '404'
            except:
                info = sys.exc_info()
                print('!!! %s, %s' % (info[0], info[1]))
                again = again - 1
            else:
                break

        # if again == 0:
        #    flog.write('{0} \r\n'.format(url))

    # flog.close()
    # fabs.close()
    return '200'


def downloaddoi(root, urls):

    myHttp = HttpLite()
    myHttp.addCookiejar()

    # flog = codecs.open(root + ".err", "w", "utf8")

    count = len(urls)
    for (i, url) in enumerate(urls):

        path = root + '/'
        if not os.path.exists(path):
            os.makedirs(path)

        again = 10
        while again > 0:
            try:
                print("@processing '%s' [%d/%d]" % (url, i + 1, count))
                proctime = time.clock()

                content = myHttp.get(url)
                # flog.write(content)
                m = re.search(
                    r'"formulaStrippedArticleTitle":"([\w|\W]*?)"', content)
                # n = re.search(r'"abstract":"([\w|\W]*?)"', content)
                v = re.search(
                    r'"pdfPath":"/\w*/(\d*)/(\d*)/(\d*)\.pdf"', content)
                print('TPNO={0}, ISNO={1}, ARNO={2}'.format(
                    v.group(1), v.group(2), v.group(3)))

                '''
                fabs = path + '{0} {1}.txt'.format(i + 1, fixpath(m.group(1)))
                with open(fabs, 'w') as f:
                    f.write(n.group(1))
                '''

                myHttp.download(
                    'https://ieeexplore.ieee.org/ielx7/{0}/{1}/{2}.pdf?'
                    'tp=&arnumber={2}&isnumber={1}'.format(
                        v.group(1), v.group(2), v.group(3)),
                    path + '{0} {1}.pdf'.format(i + 1, fixfile(m.group(1))))

                proctime = time.clock() - proctime
                if proctime < 10:
                    time.sleep(10 - proctime)

            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return '404'
            except:
                info = sys.exc_info()
                print('!!! %s, %s' % (info[0], info[1]))
                again = again - 1
            else:
                break

        # if again == 0:
        #    flog.write('{0} \r\n'.format(url))

    # flog.close()
    return '200'


def downloadindex(root, urls):

    elist = ['404']

    myHttp = HttpLite()

    count = len(urls)
    for (i, (idx, url)) in enumerate(urls):

        # flog = codecs.open(root + fixpath(idx) + ".err", "w", "utf8")

        path = root + fixpath(idx) + '/'
        if not os.path.exists(path):
            os.makedirs(path)

        again = 10
        while again > 0:
            try:
                print("@processing index '%s' [%d/%d]" % (url, i + 1, count))

                content = myHttp.get(url)

                """
                p = re.findall(
                    r'<li><a href="(http://dblp\.uni-trier\.de/rec/ris/conf/'
                    '[a-zA-Z0-9]*/[a-zA-Z0-9]*\.ris)"[\w|\W]*?'
                    '<span class="title" itemprop="name">'
                    '([\w|\W]*?)\.?</span>', content)

                if len(p) != 0:
                    downloadris(path + 'ris', p)
                """

                m = re.findall(
                    r'<header><h2>([\w|\s|,|:|\.]*?)</h2></header>\s*'
                    '<ul class="publ-list">([\w|\W]*?)</ul>\s', content)

                n = re.findall(
                    r'<header><h3>([\w|\s|,|:|\.]*?)</h3></header>\s*'
                    '<ul class="publ-list">([\w|\W]*?)</ul>\s', content)

                if len(m + n) > 0:

                    print('>> indexing [{}]'.format(len(m + n)))

                    for (mi, mu) in m + n:

                        print('>> indexing "{0}" as "{1}"'.format(
                            mi, fixpath(mi)))

                        mm = re.findall(
                            r'<li><a href="(https://doi\.org/[\w|\W]*?)"'
                            '[\w|\W]*?>electronic edition via DOI</a></li>',
                            mu)

                        if len(mm) != 0:
                            if downloaddoi(path + fixpath(mi), mm) not in elist:
                                continue
                            else:
                                print('404 switching source')

                        mm = re.findall(
                            r'<li><a href="(http://\w*\.ieee\.org/[\w|\W]*?)"'
                            '[\w|\W]*?>electronic edition @ ieee\.org</a></li>', mu)

                        if len(mm) != 0:
                            if downloaddoi(path + fixpath(mi), mm) not in elist:
                                continue

                        mm = re.findall(
                            r'<li><a href="(http://\w*\.acm\.org/[\w|\W]*?)"'
                            '[\w|\W]*?>electronic edition @ acm.org</a></li>',
                            mu)

                        if len(mm) != 0:
                            # print("@@'" + fixpath(mi) + "'")
                            # print(mm)
                            if downloadacm(path + fixpath(mi), mm) not in elist:
                                continue

                        mm = re.findall(
                            r'<li><a href="(http://dx\.doi\.org/[\w|\W]*?)"'
                            '[\w|\W]*?>electronic edition via DOI</a></li>', mu)

                        if len(mm) != 0:
                            if downloaddoi(path + fixpath(mi), mm) not in elist:
                                continue

                        print('!! source_not_found [{0}] \r\n'.format(fixpath(mi)))

                else:

                    mm = re.findall(
                        r'<li><a href="(https://doi\.org/[\w|\W]*?)"'
                        '[\w|\W]*?>electronic edition via DOI</a></li>',
                        content)

                    if len(mm) != 0:
                        if downloaddoi(path + fixpath('all'), mm) not in elist:
                            break
                        else:
                            print('404 switching source')

                    mm = re.findall(
                        r'<li><a href="(http://\w*\.ieee\.org/[\w|\W]*?)"'
                        '[\w|\W]*?>electronic edition @ ieee\.org</a></li>',
                        content)

                    if len(mm) != 0:
                        if downloaddoi(path + fixpath('all'), mm) not in elist:
                            break
                        else:
                            print('404 switching source')

                    mm = re.findall(
                        r'<li><a href="(http://\w*\.acm\.org/[\w|\W]*?)"'
                        '[\w|\W]*?>electronic edition @ acm.org</a></li>',
                        content)

                    if len(mm) != 0:
                        # print("@@'" + fixpath(mi) + "'")
                        # print(mm)
                        if downloadacm(path + fixpath('all'), mm) not in elist:
                            break
                        else:
                            print('404 switching source')

                    mm = re.findall(
                        r'<li><a href="(http://dx\.doi\.org/[\w|\W]*?)"'
                        '[\w|\W]*?>electronic edition via DOI</a></li>',
                        content)

                    if len(mm) != 0:
                        if downloaddoi(path + fixpath('all'), mm) not in elist:
                            break
                        else:
                            print('404 switching source')

                    mm = re.findall(
                        r'<li><a href='
                        '"(http://ceur-ws\.org/Vol-\d*/[\w|-]*\.pdf)"'
                        '[\w|\W]*?>electronic edition @ ceur-ws\.org</a></li>'
                        '[\w|\W]*?<span class="title" itemprop="name">'
                        '([\w|\W]*?)</span>', content)

                    if len(mm) != 0:
                        downloadpdf(path + fixpath('all'), mm)
                        break

                    print('!! source_not_found \r\n')

            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                info = sys.exc_info()
                print('!!! %s, %s' % (info[0], info[1]))
                again = again - 1
            else:
                break

        # if again == 0:
        #    flog.write('{0} {1} \r\n'.format(idx, url))

        # flog.close()
    pass


if __name__ == '__main__':
    downloadindex('./', [
        #MSR
        ('MSR 2015', 'http://dblp.org/db/conf/msr/msr2015.html'),
        ('MSR 2014', 'http://dblp.org/db/conf/msr/msr2014.html'),
        ('MSR 2013', 'http://dblp.org/db/conf/msr/msr2013.html'),
        ('MSR 2012', 'http://dblp.org/db/conf/msr/msr2012.html'),
        ('MSR 2011', 'http://dblp.org/db/conf/msr/msr2011.html'),
        ('MSR 2010', 'http://dblp.org/db/conf/msr/msr2010.html'),
        ('MSR 2009', 'http://dblp.org/db/conf/msr/msr2009.html'),
        ('MSR 2008', 'http://dblp.org/db/conf/msr/msr2008.html'),
        ('MSR 2007', 'http://dblp.org/db/conf/msr/msr2007.html'),
        ('MSR 2006', 'http://dblp.org/db/conf/msr/msr2006.html'),
        ('MSR 2005', 'http://dblp.org/db/conf/msr/msr2005.html')
        # ICSE
        # ('ICSE 2017', 'http://dblp.uni-trier.de/db/conf/icse/icse2017.html'),
        # ('ICSE 2017c',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2017c.html'),
        # ('ICSE 2017 NIER',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2017nier.html'),
        # ('ICSE 2017 SEET',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2017seet.html'),
        # ('ICSE 2017 SEIP',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2017seip.html'),
        # ('ICSE 2017 SEIS',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2017seis.html'),  # Missing-source
        # ('ICSE 2016',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2016.html'),
        # ('ICSE 2016c',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2016c.html'),
        # ('ICSE ICSSP 2016',
        # 'http://dblp.uni-trier.de/db/conf/ispw/icssp2016.html'),
        # ('ICSE 2015-1',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2015-1.html'),
        # ('ICSE 2015-2',
        # 'http://dblp.uni-trier.de/db/conf/icse/icse2015-2.html'),
        # ('ICSE COUFLESS 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/coufless2015.html'),
        # ('ICSE CSD 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/csd2015.html'),
        # ('ICSE GAS 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/gas2015.html'),
        # ('ICSE GREENS 2015',
        # 'http://dblp.uni-trier.de/db/conf/greens/greens2015.html'),
        # ('ICSE GTSE 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/gtse2015.html'),
        # ('ICSE PLEASE 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/please2015.html'),
        # ('ICSE RAISE 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/raise2015.html'),
        # ('ICSE RELENG 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/releng2015.html'),
        # ('ICSE RET 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/ret2015.html'),
        # ('ICSE SAM 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/sam2015.html'),
        # ('ICSE SE4HPCS 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/se4hpcs2015.html'),
        # ('ICSE SEMS 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/sems2015.html'),
        # ('ICSE SESOS 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/sesos2015.html'),
        # ('ICSE SPRO 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/spro2015.html'),
        # ('ICSE SST 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/sst2015.html'),
        # ('ICSE TELERISE 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/telerise2015.html'),
        # ('ICSE TWINPEAKS 2015',
        # 'http://dblp.uni-trier.de/db/conf/icse/twinpeaks2015.html'),
        # ASE
        # ('ASE 2016', 'http://dblp.uni-trier.de/db/conf/kbse/ase2016.html'),
        # ('ASE SWMI 2016',
        # 'http://dblp.uni-trier.de/db/conf/kbse/swmi2016.html'),
        # ('ASE FORMABS 2016',
        # 'http://dblp.uni-trier.de/db/conf/kbse/formabs2016.html'),
        # ('ASE IWOR 2016',
        # 'http://dblp.uni-trier.de/db/conf/kbse/iwor2016.html'),
        # ('ASE SCTDCP 2016',
        # 'http://dblp.uni-trier.de/db/conf/kbse/sctdcp2016.html'),
        # ('ASE 2015', 'http://dblp.uni-trier.de/db/conf/kbse/ase2015.html'),
        # ('ASE 2015 Workshops',
        # 'http://dblp.uni-trier.de/db/conf/kbse/ase2015w.html'),
        # ('ASE 2014', 'http://dblp.uni-trier.de/db/conf/kbse/ase2014.html'),
        # ('ASE WISE 2014',
        # 'http://dblp.uni-trier.de/db/conf/kbse/wise2014.html'),
        # ISSTA
        # ('ISSTA 2017',
        # 'http://dblp.uni-trier.de/db/conf/issta/issta2017.html'),
        # ('ISSTA 2016',
        # 'http://dblp.uni-trier.de/db/conf/issta/issta2016.html'),
        # ('ISSTA CSTVA 2016',
        # 'http://dblp.uni-trier.de/db/conf/issta/cstva2016.html'),
        # ('ISSTA QUDOS 2016',
        # 'http://dblp.uni-trier.de/db/conf/issta/qudos2016.html'),
        # ('ISSTA 2015',
        # 'http://dblp.uni-trier.de/db/conf/issta/issta2015.html'),
        # ('ISSTA CHESE 2015',
        # 'http://dblp.uni-trier.de/db/conf/issta/chese2015.html'),#
        # ESEM
        # ('ESEM 2016', 'http://dblp.uni-trier.de/db/conf/esem/esem2016.html'),
        # ('ESEM MEGSUS 2016',
        # 'http://dblp.uni-trier.de/db/conf/esem/megsus2016.html'),
        # ('ESEM 2015', 'http://dblp.uni-trier.de/db/conf/esem/esem2015.html'),
        # ('ESEM 2014', 'http://dblp.uni-trier.de/db/conf/esem/esem2014.html'),
        # SEKE
        # ('SEKE 2016', 'http://dblp.uni-trier.de/db/conf/seke/seke2016.html'),
        # ('SEKE 2015', 'http://dblp.uni-trier.de/db/conf/seke/seke2015.html'),
        # ('SEKE 2014',
        # 'http://dblp.uni-trier.de/db/conf/seke/seke2014.html'),    # No-source
    ])
