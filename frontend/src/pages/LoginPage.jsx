import { useState } from 'react';
import { Box, Heading } from '@chakra-ui/react';
import { useHistory } from 'react-router-dom';
import LoginForm from '../components/LoginForm';

const LoginPage = () => {
  const history = useHistory();
  const [loginError, setLoginError] = useState(null);

  const handleLogin = async (event, formData) => {
    event.preventDefault();

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        const { message, user_id } = data;
        // Redirect to homepage with success message and user ID
        history.push(`/home?user_id=${user_id}&message=${message}`);
      } else {
        const data = await response.json();
        const { message } = data;
        setLoginError(message);
      }
    } catch (error) {
      console.error('Error:', error);
      setLoginError('An error occurred. Please try again later.');
    }
  };

  return (
    <Box p={4}>
      <Heading as="h1" size="xl" mb={4}>
        Login Page
      </Heading>
      <LoginForm handleLogin={handleLogin} loginError={loginError} />
    </Box>
  );
};

export default LoginPage;
