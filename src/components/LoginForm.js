import React from 'react';
import PropTypes from 'prop-types';

import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import GoogleLogin from 'react-google-login';


class LoginForm extends React.Component {
  state = {
    username: '',
    password: ''
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
        <>
            <Form onSubmit={e => this.props.handle_login(e, this.state)}>
                <h3 className="text-center">Log In</h3>
                <Row className="mt-5 justify-content-md-center">
                
                <Col xs={4} md={6}>
                    <Form.Group controlId="formBasicEmail">
                        <Form.Label>Email address</Form.Label>
                        <Form.Control 
                        type="text"
                        size="lg"
                        name="username"
                        value={this.state.username}
                        onChange={this.handle_change} 
                        placeholder="Enter Email" 
                        required
                        />
                        <Form.Text className="text-muted">
                        We'll never share your email with anyone else.
                        </Form.Text>
                    </Form.Group>

                    <Form.Group controlId="formBasicPassword">
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

                    <Button variant="primary" className="mt-3" type="submit">
                      Login
                    </Button>

                    <hr />
                    <div className="text-center">
                      <GoogleLogin
                        clientId="708748930922-t75kjse8g80eavl6v4vfd39b0oumt7tn.apps.googleusercontent.com"
                        buttonText="LOGIN WITH GOOGLE"
                        onSuccess={this.props.responseSuccessGoogle}
                        onFailure={this.props.responseFailureGoogle}
                      />
                    </div>
                </Col>
                </Row>
            </Form>
        </>
    );
  }
}

export default LoginForm;

LoginForm.propTypes = {
  handle_login: PropTypes.func.isRequired
};