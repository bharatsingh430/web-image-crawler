from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import os
import os.path
import sys
import signal, time
from multiprocessing import Pool
import gc
import socks
import socket
import urllib
import random
import argparse


def getimg(args):
    try:
        lnk = args[0]
        output_loc = args[1]
        wstr = args[2]
        ct = args[3]
        urllib.urlretrieve(lnk, output_loc + "/" + wstr + "/" + str(ct))
    except:
        return


def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

def getlinks(driver, query_string, output_loc, tid, profileport, waittime):
    # Create a new instance of the Firefox driver
    query_string = query_string.replace('`','')
    query_string = query_string.replace('@','')
    query_string = query_string.replace('#','')
    query_string = query_string.replace('^','')
    query_string = query_string.replace('~','')
    query_string = query_string.replace('{','')
    query_string = query_string.replace('}','')
    query_string = query_string.replace('|','')
    query_string = query_string.replace('>','')
    query_string = query_string.replace('<','')
    idx = query_string.find('=')

    if idx >= 0:
        if idx > 0:
            query_string = query_string.replace(query_string[idx-1], '')
        query_string = query_string.replace('=','')
    

    query_string = query_string.replace('&','and')
    query_string = query_string.replace(';','%20')
    query_string = query_string.replace('/','%20')
    query_string = query_string.replace(')','%20')
    query_string = query_string.replace('(','%20')
    query_string = query_string.replace('!','')
    query_string = query_string.replace('%20%20','%20')
    query_string = query_string.replace('%20%20','%20')
    query_string = query_string.replace('%20%20','%20')
    query_string = query_string.replace('-','%20')
    query_string = query_string.replace('_','%20')
    words = query_string.split('%20')
    wlen = len(words)

    wstr = ''
    for i in range(wlen):
        if i < wlen - 1:
            wstr = wstr + words[i] + '_' 
        else:
            wstr = wstr + words[i]

    if os.path.exists(output_loc + tid + '/' + wstr + '.zip') == True:
        return False

    if query_string.find('/') >= 0:
        return False
    
    try:
        print 'mkdir -p ' + output_loc + wstr
        os.system('mkdir -p ' + output_loc + wstr)
        t0 = time.clock()

        print("fetching " + query_string + " " + profileport)
        driver.get("https://www.google.com/search?tbm=isch&tbs=itp:photo&q=" + query_string)
        t1 = time.clock()        
        for ctr in range(1,10):
            val = float(ctr)/10
            driver.execute_script("window.scrollTo(0, " + str(val) + "*document.body.scrollHeight);")
            time.sleep(waittime)

        driver.execute_script("layer = document.getElementById('rg_s');links = [];var count = 0;for (var i = 0; i < layer.childElementCount; i++) {td = layer.children[i];if (td.childElementCount > 1) {lk2 = td.getElementsByTagName('a')[0].children[0].src;ext = JSON.parse(td.children[1].innerHTML)['ity']; if ((ext == 'jpg' || ext == 'png' || ext == 'JPG' || ext == 'PNG' || ext == 'gif' || ext == 'jpeg' || ext == 'JPEG') ) {links[count] = lk2; count = count + 1; } } } document.getElementsByTagName('html')[0].innerHTML = ''; var newdiv = document.createElement('div'); var divIdName = 'links'; innertext = links[0]; for (var j = 1; j < links.length; j++) { innertext = innertext + \"  \" + links[j]; } newdiv.setAttribute('id',divIdName); newdiv.innerHTML = innertext; document.body.appendChild(newdiv);")

	html_source_links = driver.page_source

        links = html_source_links.split('links">')[1].split('</div>')[0].split('  ')
        ct = 1;

        args = []

        for link in links:
             args.append([link, output_loc, wstr, str(ct)])
             ct = ct + 1

        t2 = time.clock()

        p = Pool(4)
        p.map(getimg, args)
        p.close()
        p.join()

        t3 = time.clock()

        files = os.popen('ls ' + output_loc + wstr + '/').read().split()
        numfiles = len(files)
        print numfiles, (t1-t0)*100, (t2-t1)*100, (t3-t2)*100
        
        #os.system('mv ' + output_loc + wstr + '.zip ' + output_loc + tid + '/')

        if numfiles > 150:
            os.system('zip -r -0 ' + output_loc + wstr + '.zip ' + output_loc + wstr + ' >/dev/null')
            os.system('rm -rf ' + output_loc + wstr)
        else:
            print wstr + ' ' + str(numfiles) + ' ' + profileport
            os.system('echo ' + '"' + wstr + ' ' + str(numfiles) + ' ' + profileport + '" >> low.txt')

        return True
    except:
        print "false " + wstr + " " + profileport
        os.system('echo ' + '"false ' + wstr + ' ' + profileport + '" >> errors.txt')
        return False

def main():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("network.http.use-cache", False)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--query_file', dest='query_file',
                    default='sample.txt', type=str,
                    help='name of query file')
    parser.add_argument('--dir_name', dest='dir_name',
                    default='tmp/', type=str,
                    help='name of output directory, include a / at the end')
    parser.add_argument('--tid', dest='tid',
                    default=1, type=int,
                    help='if using multiple instances, this should be unique')
    parser.add_argument('--socks_flag', dest='socks_flag',
                    default=0, type=int,
                    help='if using socks forwarding, set this to 1')
    parser.add_argument('--port', dest='port',
                    default=8081, type=int,
                    help='if using socks forwarding, use the port')
    parser.add_argument('--wait_time', dest='wait_time',
                    default=0.25, type=float,
                    help='time to wait before issuing a scroll, reduce it to make it faster, but you may end up getting less images')


    args = parser.parse_args()
    port = args.port

    # code for socks forwarding, if you need to route your query via a remote server
    # only needed if you need to make a lot of queries
    if args.socks_flag == 1:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1", port,True)
        socket.socket = socks.socksocket
        socket.socket = socks.socksocket
        socket.create_connection = create_connection

        profile.set_preference("network.proxy.type", 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', port)
        profile.set_preference("network.proxy.socks_version", 5)


    driver = webdriver.Firefox(profile)
    driver.set_page_load_timeout(30)
    query_file = args.query_file
    output_dir = args.dir_name
    tid = args.tid
    
    queries = open(args.query_file, 'r')
    lines = queries.read().split('\n')

    for query in lines:
        if query != '':            
            getlinks(driver, query, args.dir_name, str(tid), str(port), args.wait_time)
    driver.close()

if __name__ == "__main__":
    main()
