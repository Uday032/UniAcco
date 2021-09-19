import React, { Component } from 'react'

import {Form} from 'react-bootstrap'

export default class AfterLogin extends Component { 
    constructor(props) {
        super(props);
        this.state = {
            count : 0
        }
    }

    showFile = async (e) => {
        e.preventDefault()
        const reader = new FileReader()
        reader.onload = async (e) => { 
            const text = (e.target.result)
            var split_array = text.split(" ").join("")
            this.setState({
                count: split_array.length,
            })
        }
        reader.readAsText(e.target.files[0]);
    }
    render() {
        
        return (
            <div>
                <h3>Hello, {this.props.username}</h3>

                <div className="pt-4">
                    <Form>
                        <Form.Label>Default file input example</Form.Label>
                        <Form.Control type="file" onChange={(e) => this.showFile(e)}/>    
                        <div className="pt-4">
                        </div>
                        <div>Words: {this.state.count}</div>
                    </Form>
                </div>
            </div>
        )
    }
}
