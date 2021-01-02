import React, { Component } from 'react';
import Nav from './components/Nav';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import './App.css';

//bootstrap react
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayed_form: '',
      logged_in: localStorage.getItem('token') ? true : false,
      username: '',
      error: ''
    };
  }

  componentDidMount() {
    if (this.state.logged_in) {
      fetch('http://localhost:8000/core/current_user/', {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(json => {
          this.setState({ username: json.username });
        });
    }
  }

  handle_login = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/core/loginuser/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        console.log(json);
        if(json.token) {
          localStorage.setItem('token', json.token);
          this.setState({
            logged_in: true,
            displayed_form: '',
            username: json.user[0].username
          });
        }
        this.setState({
          error: json
        })
      });
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/core/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        localStorage.setItem('token', json.token);
        this.setState({
          logged_in: true,
          displayed_form: '',
          username: json.username
        });
      });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({ logged_in: false, username: '', error: '' });
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
    let form;
    switch (this.state.displayed_form) {
      case 'login':
        form = <LoginForm handle_login={this.handle_login} />;
        break;
      case 'signup':
        form = <SignupForm handle_signup={this.handle_signup} />;
        break;
      default:
        form = null;
    }

    return (
      <div className="App">
        <Container>
          <Nav
            logged_in={this.state.logged_in}
            display_form={this.display_form}
            handle_logout={this.handle_logout}
          />
          {form}
          <h3>
            {this.state.logged_in
              ? `Hello, ${this.state.username}`
              : `${this.state.error}`}
          </h3>
        </Container>
      </div>
    );
  }
}

export default App;