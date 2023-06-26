import { Box, Heading } from '@chakra-ui/react';
import LoginForm from '../components/LoginForm';

const LoginPage = () => {
  const handleLogin = (event) => {
    event.preventDefault();
    // Handle login logic
  };

  return (
    <Box p={4}>
      <Heading as="h1" size="xl" mb={4}>
        Login Page
      </Heading>
      <LoginForm handleLogin={handleLogin} />
    </Box>
  );
};

export default LoginPage;