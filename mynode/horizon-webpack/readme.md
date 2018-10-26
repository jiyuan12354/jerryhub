一: horizon那边要做的改动
1.环境上要有django-webpack-loader这个pip包(206.18controller4上已经有了)
2.修改setting.py文件加入
# Webpack configuration
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(ROOT_PATH, 'webpack/webpack-stats-local.json')
    }
}

INSTALLED_APPS += ('webpack_loader', )
3.这样子horizon这边就配置好了.引入js方法是:
在某个html页面中,加入
{% load render_bundle from webpack_loader %}
然后用render_bundle去加载js
{% render_bundle 'main' %}
(参考目录下的example.html,直接把里面的内容复制到
openstack_dashboard/dashboards/compute/instance_tags/templates/instance_tags/ngindex.html
打开 计算->主机标签 就能看到效果了)

二: horizon-webpack的配置
这个工程是运行在自己机器上的,它会产生一个webpack-stats-local.json文件,
利用stfp的watcher去自动监听这个文件的变化然后自动上传,上传的路径要和setting中配置好的路径一致
horizon的webpack-loader发现这个文件改变了,就会重新获取js

先准备好nodejs和npm

1.先把 webpack/webpack.config.base.js 里面的local_ip改为自己电脑的ip
2.配置sftp,加入watcher属性
    "watcher": {
        "files": "webpack/webpack-stats-local.json",
        "autoUpload": true,
        "autoDelete": false
    },
3.全局安装cnpm(有个node-sass这个包用npm安装会失败)
sudo npm install -g cnpm
4.用cnpm安装package.json中声明的包
cnpm install
5.启动服务
npm run webpack-dev-server
