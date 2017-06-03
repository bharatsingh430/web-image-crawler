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

def getimg(args):
    try:
        lnk = args[0]
        output_loc = args[1]
        wstr = args[2]
        ct = args[3]
        urllib.urlretrieve(lnk, output_loc + "/" + wstr + "/" + str(ct))
    except:
        return

def getlinks(driver, output_loc, tid):
    wstr = str(tid)
    print 'mkdir -p ' + output_loc + "/" + wstr
    os.system('mkdir -p ' + output_loc + "/" + wstr)
    t1 = time.clock()

    driver.get("https://www.google.com/search?tbm=isch&tbs=itp:photo")
        
    input('Press 0 after doing action in browser ')
        
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

    files = os.popen('ls ' + output_loc + '/' + wstr + '/').read().split()
    numfiles = len(files)
    print numfiles, (t2-t1)*3600, (t3-t2)*3600
        
    if numfiles > 150:
        os.system('zip -r -0 ' + output_loc + wstr + '.zip ' + output_loc + wstr + ' >/dev/null')
        os.system('rm -rf ' + output_loc + wstr)
    else:
        print wstr + ' ' + str(numfiles)
        os.system('echo ' + '"' + wstr + ' ' + str(numfiles) + '" >> low.txt')

def main():
    gc.enable()
    path = os.popen('pwd').read().split()[0]
    tid = 0
    while True:
        tid = tid + 1
        output_loc = path + '/interactive'

        while True:
            try:
                driver = webdriver.Firefox()
                driver.set_page_load_timeout(30)
                break
            except:
                time.sleep(2)
                print "trying again to open driver " + str(profileport)
                try:
                    driver.quit()
                except:
                    continue

        getlinks(driver, output_loc, str(tid))



if __name__ == "__main__":
    main()
