'use strict';

import React from 'react';
import Reverse from './components/SimpleComponent';
import './app.scss';

function App() {
    return (
        <div className="App">
            <h1 className="AppHeader">Hello</h1>
            <p className="AppContent">This is a Django + React + Webpack + npm + Sass + babel project.</p>
            <h1>特性</h1>
            <p>与django结合</p>
            <p>保存js页面自动刷新aaabbb</p>
            <p>js编译，将更高版本的js(es6以上)编译为es5</p>
            <p>使用模块语法编写</p>
            <p>下面是一个简单的组件，把元素内的字符串反转</p>
            <Reverse>This text should be reversed.</Reverse>
            <Reverse>And this text too.</Reverse>
        </div>
    )
}

export default App;