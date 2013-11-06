#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                __ __    __
#               / / \ \   \ \
#              / /   \ \   \ \
#             / /     \ \___\ \
#            / /______ \_______\
#           /  ____  / / /   / /
#          / /    / / / /   / /
#         / /____/ / / /___/ /
#        /________/ /_______/
#
#                 E621 IMAGE DOWNLOADER
#
#                          10/10/2013
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
#   ~~~~~ Modules ~~~~~
 
import re
import os
import urllib
import urllib2
import string
import argparse

#   ~~~~~ Setup Command Line Arguments ~~~~~

parser = argparse.ArgumentParser(description='Downloads images from e621.net', prog='e621-downloader')

parser.add_argument('--query', dest='query', action='store',
                   help='Search Query (Exactly what you\'d put in the Search Box)')
parser.add_argument('--query', dest='query', action='store',
                   help='Search Query (Exactly what you\'d put in the Search Box)')
parser.add_argument('--query', dest='query', action='store',
                   help='Search Query (Exactly what you\'d put in the Search Box)')

args = parser.parse_args()

#arguments = OptionParser()
#arguments.add_option("-q", "--query", dest="query",
#                  help="Search Query (Exactly what you\'d put in the Search Box)")
#arguments.add_option("-p", "--path", dest="path",
#                  help="Path to store downloaded images (Must include trailing slash")
#arguments.add_option("-i", "--interactive", dest="interactive",
#				  help="Run script interactively")

(options, args) = arguments.parse_args()

#   ~~~~~ Config ~~~~~
 
enable_proxy = 0 # 1 = Enable; 0 = Disable
proxy_protocol = 'socks5' # 'http', 'socks4', 'socks5'
proxy_addr = 'localhost' # Example: '119.97.151.151'
proxy_port = 9050 # Example: 8080

 
#   ~~~~~ Variables ~~~~~
 
page_num = 1
loop = 1
query.replace(' ', '+')
url = 'https://e621.net/post?tags='+query+'&searchDefault=Search'
scan_for = '"https://static1.e621.net/data/preview/.*?"'
query = raw_input('Search Query (Exactly what you\'d put in the Search Box): ') # terms (exactly what you'd put in the search box)
path = raw_input('Path to image storage directory (Needs Trailing Slash): ') # Needs Trailing Slash
 
#   ~~~~~ Functions ~~~~~
 
def intro():
        print("""
       
           __ __    __
          / / \\ \\   \ \\
         / /   \\ \\   \ \\
        / /     \\ \\___\ \\
       / /______ \\_______\\
      /  ____  / / /   / /
     / /    / / / /   / /
    / /____/ / / /___/ /
   /________/ /_______/
       
       
   E621 IMAGE DOWNLOADER
       
       """)
       
def verify():
        print('')
        print('Downloading ALL images containing search term(s): '+ query)
        print('')
        print('Downloading to folder: '+ path)
        print('')
        correct = raw_input("\tIs this correct? [y/n]: ")
        while correct not in ['y', 'n']:
                correct = raw_input("\tInvalid Input. Are the Above Correct? [y/n]: ")
        if correct == 'n':
                loop = 0
                print('')
                print("Script Stopped by User")
                print('')
                quit()
 
def next_page():
        global page_num
        page_num += 1
        global url
        url = url+'&page='+str(page_num)
       
def file_exists(name):
        if os.path.isfile(path+name):
                return 1
        else:
                return 0
               
def download_image(img, name):
        try:
                urllib2.urlopen('https://e621.net/'+img)
        except urllib2.HTTPError, err:
                try:
                        img = img.replace('jpg', 'png')
                        name = name.replace('jpg', 'png')
                        urllib2.urlopen('https://e621.net/'+img)
                except urllib2.HTTPError, err:
                        try:
                                img = img.replace('png', 'gif')
                                name = name.replace('png', 'gif')
                                urllib2.urlopen('https://e621.net/'+img)
                        except urllib2.HTTPError, err:
                                print('\tERROR: Could not download. See failed.txt')
                                fail_log = open('failed.txt', "a")
                                fail_log.write('https://e621.net/'+img+'\n')
                                fail_log.close()
                        else:
                                if file_exists(name):
                                        print('\tSkipping: File Already Exists')
                                else:
                                        file = urllib2.urlopen('https://e621.net/'+img)
                                        output = open(path+name,'wb')
                                        output.write(file.read())
                                        output.close()
                else:
                        if file_exists(name):
                                print('\tSkipping: File Already Exists')
                        else:
                                file = urllib2.urlopen('https://e621.net/'+img)
                                output = open(path+name,'wb')
                                output.write(file.read())
                                output.close()
        else:
                if file_exists(name):
                        print('\tSkipping: File Already Exists')
                else:
                        file = urllib2.urlopen('https://e621.net/'+img)
                        output = open(path+name,'wb')
                        output.write(file.read())
                        output.close()
               
def check_dir():
        if not os.path.exists(path):
                print('')
                print('Directory Not Found. Creating Folder...')
                os.makedirs(path)
 
def open_page(url):
        return urllib2.urlopen(url).read()
 
def image_list(page):
        return re.findall(scan_for, page)
       
def get_link(img):
        return img.replace('preview/', '').replace('"', '').replace('https://static1.e621.net', '')
       
def get_name(link):
        return link[-36:]
 
#       ~~~~~ Do Things ~~~~~
 
intro()
verify()
check_dir()
 
if enable_proxy == 1:
        if proxy_protocol == 'socks5':
                import socks
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_addr, int(proxy_port))
                socket.socket = socks.socksocket
        elif proxy_protocol == 'socks4':
                import socks
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, proxy_addr, int(proxy_port))
                socket.socket = socks.socksocket
        elif proxy_protocol == 'http':
                opener = urllib2.build_opener(
                                urllib2.HTTPHandler(),
                                urllib2.HTTPSHandler(),
                                urllib2.ProxyHandler({proxy_protocol:proxy_protocol+'://'+proxy_addr+':'+str(proxy_port)}))
                urllib2.install_opener(opener)
 
try:
        urllib2.urlopen('http://www.google.com')
except:
        loop = 0
        print('')
        print('\tProxy not working. Check Config')
        print('')
       
while loop:
        print('')
        print("Downloading Page...")
        page = open_page(url)
        print('')
        print("Parsing Page...")
        imgs = image_list(page)
        print('')
        print('\t'+str(len(imgs))+' Images Found on Page '+str(page_num))
        print('')
        if page.count('No posts matched your search.') == 0:
                for img in imgs:
                        print('Downloading: '+get_link(img))
                        download_image(get_link(img), get_name(get_link(img)))
        else:
                loop = 0
                print('')
                print('\tNo Images Found on Page. Downloads Complete.')
                print('')
                raw_input('Press ENTER to Exit');
                quit()
        del page
        print('')
        print('Moving to next page...')
        next_page()
 
raw_input('Press ENTER to Exit');
quit()