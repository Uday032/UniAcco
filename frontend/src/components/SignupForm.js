import React from 'react';
import PropTypes from 'prop-types';

import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

class SignupForm extends React.Component {
  state = {
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    email: ''
  };

  handle_change = e => {
    const name = e.target.name;
    const value = e.target.value;
    this.setState(prevstate => {
      const newState = { ...prevstate };
      newState[name] = value;
      return newState;
    });
  };

  render() {
    return (
        <Form onSubmit={e => this.props.handle_signup(e, this.state)}>
            <h3 className="text-center">Sign Up</h3>
            <Row className="mt-5 justify-content-md-center">
            
            <Col xs={4} md={6}>

                <Form.Row>
                    <Form.Group as={Col}>
                        <Form.Label>FirstName</Form.Label>
                        <Form.Control
                        type="text" 
                        size="lg"
                        name="first_name"
                        value={this.state.first_name}
                        onChange={this.handle_change}
                        placeholder="FirstName" 
                        required
                        />
                    </Form.Group>

                    <Form.Group as={Col}>
                        <Form.Label>LastName</Form.Label>
                        <Form.Control
                        type="text" 
                        size="lg"
                        name="last_name"
                        value={this.state.last_name}
                        onChange={this.handle_change}
                        placeholder="LastName" 
                        required
                        />
                    </Form.Group>
                </Form.Row>

                
                <Form.Group>
                    <Form.Label>UserName</Form.Label>
                    <Form.Control
                    type="text" 
                    size="lg"
                    name="username"
                    value={this.state.username}
                    onChange={this.handle_change}
                    placeholder="Username" 
                    required
                    />
                </Form.Group>

                <Form.Group>
                <Form.Label>Email address</Form.Label>
                <Form.Control 
                    type="text"
                    size="lg"
                    name="email"
                    value={this.state.email}
                    onChange={this.handle_change}
                    placeholder="Enter Email" 
                    required
                />
                <Form.Text className="text-muted">
                    We'll never share your email with anyone else.
                </Form.Text>
                </Form.Group>

                <Form.Row>
                <Form.Group as={Col}>
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                    type="password" 
                    size="lg"
                    name="password"
                    value={this.state.password}
                    onChange={this.handle_change}
                    placeholder="Password" 
                    required
                    />
                </Form.Group>

                {/* <Form.Group as={Col}>
                    <Form.Label>Confirm Password</Form.Label>
                    <Form.Control
                    type="password" 
                    size="lg"
                    name="confirmpassword"
                    value={this.state.confirmpassword}
                    onChange={this.handle_change}
                    placeholder="Password" 
                    />
                </Form.Group> */}
                </Form.Row>

                <Button variant="primary" type="submit">
                Sign Up
                </Button>
            </Col>
            </Row>
        </Form>

    );
  }
}

export default SignupForm;

SignupForm.propTypes = {
  handle_signup: PropTypes.func.isRequired
};