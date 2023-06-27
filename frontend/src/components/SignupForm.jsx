import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, Button } from '@chakra-ui/react';

const SignupForm = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    setErrorMessage('');
    setSuccessMessage('');
  }, [email, username, password1, password2]);

  const navigate = useNavigate();

  const handleSignup = async () => {
	const data = {
	  email,
	  username,
	  password1,
	  password2,
	};
  
	try {
	  const response = await fetch('http://localhost:5000/sign-up', {
		method: 'POST',
		headers: {
		  'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	  });
  
	  if (response.ok) {
		const responseData = await response.json();
		if (responseData.user_id) {
		  // Signup successful
		  setSuccessMessage('Account created successfully!');
  
		  // Redirect to the homepage after a short delay
      const { user_id, message } = responseData;
		  setTimeout(() => {
        navigate(`/home/${user_id}?message=${message}`);
		  }, 2000);
		} else {
		  // Signup failed, handle the error
		  setErrorMessage(responseData.message);
		}
	  } else {
		const errorData = await response.json();
		setErrorMessage(errorData.message);
	  }
	} catch (error) {
	  console.error('An error occurred:', error);
	  setErrorMessage('An error occurred. Please try again later.');
	}
  };
  
  return (
    <div>
      <Input
	    id="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        mb={2}
		autocomplete="email"
      />
      <Input
	    id="username"
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
        mb={2}
		autocomplete="username"
      />
      <Input
	    id="password1"
        placeholder="Enter Password"
        type="password"
        value={password1}
        onChange={e => setPassword1(e.target.value)}
        mb={2}
		autocomplete="on"
      />
      <Input
	    id="password2"
        placeholder="Confirm Password"
        type="password"
        value={password2}
        onChange={e => setPassword2(e.target.value)}
        mb={2}
		autocomplete="on"
      />
      <Button colorScheme="blue" onClick={handleSignup}>
        Sign Up
      </Button>
      {errorMessage && (
        <p style={{ color: 'red' }}>{errorMessage}</p>
      )}
      {successMessage && (
        <p style={{ color: 'green' }}>{successMessage}</p>
      )}
    </div>
  );
};

export default SignupForm;
