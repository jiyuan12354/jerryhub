'use strict';

import React from 'react';
import './SimpleComponent.scss'

class Welcome extends React.Component {
    render() {
        var content = this.props.children.split('').reverse().join('');
        return <h1>{content}</h1>;
    }
}

export default Welcome