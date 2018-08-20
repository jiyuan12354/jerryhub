import requests,json,xlwt,getopt,sys


root_node_id = ''
tcprefix = ''
g_tree = {}
all_leaf = []
session_id = ''
username = 'guest'
password = '123456'

def get_session_id():
    global username,password,session_id
    data = {
        'reqURI':'',
        'destination':'',
        'tl_login':username,
        'tl_password':password,
        'login_submit':'Login'
    }
    req = requests.post('http://10.3.196.2:8081/login.php',data=data)
    session_id = req.headers['Set-Cookie'].split('PHPSESSID=')[-1].split(';')[0]


def get_data(node_id,tcprefix):
    global all_leaf
    url = 'http://10.3.196.2:8081/lib/ajax/gettprojectnodes.php?root_node='+str(node_id)+'&tcprefix='+tcprefix
    cookies = dict(PHPSESSID=session_id)
    try:
        req =requests.get(url,cookies=cookies)
        data = json.loads(req.content)
        tree = {}
        for node in data:
            if not node['leaf']:
                tree[node['text']] = get_data(node['id'],tcprefix)
            else:
                tree[node['text']] = node['id']
                all_leaf.append(node['text'])
        return tree
    except Exception as e:
        return 'error:'+str(node_id)


if __name__=='__main__':
    tcprefix = input('请输入测试用例标识：')
    root_node_id = input('请输入根节点id：')
    if input('是否有PHPSESSID，如果有请输入，如果没有，则输入n：')=='n':
        get_session_id()
    g_tree = get_data(root_node_id,tcprefix)
    f = open('result.json','w+')
    f.write(json.dumps(g_tree,ensure_ascii=False,indent=2))
    f.close()
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    title = ['用例', '详情地址', '测试情况']
    for col in range(len(title)):
        sheet.write(0, col, title[col])
    for index,test_title in enumerate(all_leaf):
        sheet.write(index+1, 0, test_title)
        sheet.write(index+1, 1, xlwt.Formula('HYPERLINK("'+'http://10.3.196.2:8081/linkto.php?tprojectPrefix='+tcprefix.replace('--','-')+'&item=testcase&id='+test_title.split(':')[0]+'";"详情")'))
    book.save('test.xls')

    
